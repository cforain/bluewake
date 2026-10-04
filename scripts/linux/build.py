#!/usr/bin/env python3
"""BlueWake Builder for Linux: turn your own game disc into your own game, on your PC.

    python scripts/linux/build.py DISC [--out build/linux] [options]

DISC is your own The Wind Waker (GameCube, USA GZLE01 revision 0) image, an
uncompressed .iso or .gcm. (Compressed Dolphin images are not converted here;
convert them to ISO in Dolphin first.)

The Linux counterpart of scripts/windows/build.py. It reads the bluewake
profile's pins (RecompCore, DolRecomp) and verified source digest, so every
builder translates the same code; docs/LINUX.md explains the port.

Steps, each logged under OUT/logs:
  1 tools        gcc, CMake 3.25+, Ninja, git, Python 3.10+
  2 dependencies the pinned RecompCore and DolRecomp sources (ref/recompcore)
  3 disc         check the disc id and revision (the disc is verified on extract)
  4 extract      main.dol and the 415 RELs from the disc
  5 translate    the game's PowerPC code to C (DolRecomp)
  6 generate     the composite source, compared with the verified digest
  7 mods         widescreen 16:9 and 16:10 and Better Wind Waker's options (--no-mods skips)
  8 compile      the game module, gGZLE01_recomp.so (the long step)
  9 app          bluewake, Aurora (Vulkan/OpenGL through Dawn), SDL3 and the DSP
 10 package      the app folder OUT/BlueWake, ready to run

The app folder contains code translated from YOUR disc and a copy of the disc:
it is yours alone. Never share or upload it. Your saves live in
~/.local/share/BlueWake, outside the build, so rebuilding never touches them.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
PROFILE = ROOT / "scripts/builder/profiles/bluewake.sh"
MODULE = "gGZLE01_recomp.so"
GC_MAGIC = 0xC2339F3D


class BuildError(Exception):
    pass


def die(message):
    raise BuildError(message)


def step(title):
    print(f"\n==> {title}", flush=True)


def default_jobs():
    """All cores, but no more parallel compiles than memory allows: the large
    translated chunks can take over a gigabyte each under gcc, and running out
    of commit kills the compiler."""
    cores = os.cpu_count() or 8
    try:
        with open("/proc/meminfo") as mem:
            for line in mem:
                if line.startswith("MemAvailable:"):
                    available = int(line.split()[1]) * 1024
                    return max(1, min(cores, int(available // (2.5 * 2**30))))
    except OSError:
        pass
    return cores


def profile_value(name):
    """A NAME=value pin from the bluewake profile, the builders' one source."""
    match = re.search(rf"^{name}=(\S+)$", PROFILE.read_text(), re.M)
    if not match:
        die(f"{PROFILE} has no {name}")
    return match.group(1)


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1 << 22), b""):
            digest.update(block)
    return digest.hexdigest()


def tree_digest(root):
    """scripts/ios/composite_manifest.py's digest of a generated tree.

    The manifest prints "<sha256>  <N> files"; only the hash identifies the tree.
    """
    out = subprocess.check_output(
        [sys.executable, str(ROOT / "scripts/ios/composite_manifest.py"), str(root)], text=True)
    return out.split()[0]


def sync_tree(new, current):
    """Copy a generated tree into place keeping unchanged files' timestamps."""
    if current.exists():
        shutil.rmtree(current)
    shutil.copytree(new, current)


class Builder:
    def __init__(self, args):
        self.args = args
        self.out = args.out
        self.logs = self.out / "logs"
        self.recompcore = ROOT / "ref/recompcore"
        self.iso = None

    # --- helpers -------------------------------------------------------
    def run(self, name, command, *, env=None, cwd=None, ninja=False):
        self.logs.mkdir(parents=True, exist_ok=True)
        log = self.logs / f"{name}.log"
        environment = dict(env or os.environ)
        if ninja:
            environment["NINJA_STATUS"] = "[%f/%t] "
        start = time.monotonic()
        print(f"  {name} (log: {log})", flush=True)
        with open(log, "wb") as stream:
            process = subprocess.Popen([str(c) for c in command], cwd=cwd or ROOT,
                                       stdout=stream, stderr=subprocess.STDOUT, env=environment)
            last = start
            while True:
                try:
                    status = process.wait(timeout=5)
                    break
                except subprocess.TimeoutExpired:
                    pass
                except KeyboardInterrupt:
                    process.terminate()
                    raise
                now = time.monotonic()
                if now - last >= 15:
                    last = now
                    detail = ""
                    try:
                        with open(log, "rb") as recent:
                            recent.seek(max(0, log.stat().st_size - 16384))
                            units = re.findall(rb"\[(\d+/\d+)\]", recent.read())
                        if units:
                            detail = f", {units[-1].decode()}"
                    except OSError:
                        pass
                    elapsed = int(now - start)
                    print(f"  {name}: {elapsed // 60}m {elapsed % 60:02d}s{detail}", flush=True)
        if status != 0:
            tail = log.read_bytes()[-4000:].decode(errors="replace")
            print(tail, file=sys.stderr)
            die(f"{name} failed (exit {status}); full log {log}")
        elapsed = int(time.monotonic() - start)
        if elapsed >= 60:
            print(f"  {name}: done in {elapsed // 60}m {elapsed % 60:02d}s", flush=True)
        return log

    def git(self, *args, cwd=None):
        return subprocess.check_output(["git", *args], cwd=cwd or ROOT, text=True,
                                       stderr=subprocess.DEVNULL).strip()

    # --- 1 tools -----------------------------------------------------
    def check_tools(self):
        if platform.system() != "Linux":
            die("this builder is for Linux; on Windows use scripts/windows/build.py")
        if platform.machine().lower() not in ("x86_64", "amd64"):
            die(f"an x86-64 Linux PC is required (this is {platform.machine()})")
        if sys.version_info < (3, 10):
            die("Python 3.10 or newer is required")
        for tool in ("git", "cmake", "ninja", "cc"):
            if shutil.which(tool) is None:
                die(f"missing {tool}: install Git, CMake 3.25+, Ninja and a C/C++ compiler "
                    "(sudo apt install build-essential cmake ninja-build)")
        # The host (Aurora) needs clang: it uses C++20 designated-initializer
        # field orders gcc rejects. The game module uses gcc (see compile_module).
        if shutil.which("clang") is None:
            die("missing clang: the host build needs it (sudo apt install clang)")
        version = subprocess.check_output(["cmake", "--version"], text=True).split()[2]
        if tuple(int(x) for x in version.split(".")[:2]) < (3, 25):
            die(f"CMake 3.25 or newer is required (found {version})")
        cc = shutil.which("cc")
        cc_version = subprocess.check_output([cc, "--version"], text=True).splitlines()[0]
        clang_version = subprocess.check_output(["clang", "--version"], text=True).splitlines()[0]
        print(f"{cc_version}; {clang_version}; cmake {version}; ninja "
              f"{subprocess.check_output(['ninja', '--version'], text=True).strip()}; "
              f"{self.args.jobs} jobs")

    # --- 2 dependencies ------------------------------------------------
    def dependencies(self):
        sha = profile_value("RECOMPCORE_SHA")
        dolrecomp_sha = profile_value("DOLRECOMP_SHA")
        url = profile_value("RECOMPCORE_URL")
        rc = self.recompcore
        if not (rc / ".git").exists():
            if rc.exists() and any(rc.iterdir()):
                die(f"{rc} exists but is not a git checkout: move it aside and rerun")
            rc.mkdir(parents=True, exist_ok=True)
            subprocess.check_call(["git", "init", "-q"], cwd=rc)
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=rc,
                              capture_output=True, text=True).stdout.strip()
        if head != sha:
            if self.git("status", "--porcelain", "--untracked-files=no", cwd=rc):
                die(f"{rc} has local changes and is not at {sha}: move it aside and rerun")
            print(f"fetching RecompCore {sha}")
            subprocess.run(["git", "remote", "remove", "bluewake"], cwd=rc, capture_output=True)
            subprocess.check_call(["git", "remote", "add", "bluewake", url], cwd=rc)
            self.run("recompcore-fetch", ["git", "-C", rc, "fetch", "--recurse-submodules=no",
                                          "--depth", "1", "bluewake", sha])
            subprocess.check_call(["git", "checkout", "-q", "--detach", "FETCH_HEAD"], cwd=rc)
        if self.git("rev-parse", "HEAD", cwd=rc) != sha:
            die(f"{rc} is not at {sha}")
        subprocess.check_call(["git", "submodule", "sync", "-q", "--", "DolRecomp"], cwd=rc)
        sub = rc / "DolRecomp"
        current = subprocess.run(["git", "rev-parse", "HEAD"], cwd=sub,
                                 capture_output=True, text=True).stdout.strip() \
            if (sub / ".git").exists() else ""
        if current != dolrecomp_sha:
            self.run("dolrecomp-fetch", ["git", "-C", rc, "submodule", "update", "--init",
                                         "--depth", "1", "--", "DolRecomp"])
        if self.git("rev-parse", "HEAD", cwd=sub) != dolrecomp_sha:
            die(f"{sub} is not at {dolrecomp_sha}")
        if self.git("status", "--porcelain", "--untracked-files=no", cwd=rc) or \
                self.git("status", "--porcelain", "--untracked-files=no", cwd=sub):
            die(f"{rc} has local changes; the build must use the pinned source exactly")
        print(f"RecompCore {sha}, DolRecomp {dolrecomp_sha}")

    # --- 3 disc ----------------------------------------------------------
    def disc(self):
        source = self.args.disc.resolve()
        if not source.is_file():
            die(f"disc image not found: {source}")
        if source.suffix.lower() not in (".iso", ".gcm"):
            die(f"this builder reads an uncompressed .iso or .gcm; convert {source.name} "
                "to ISO in Dolphin first (right-click the game, Convert File -> ISO)")
        with open(source, "rb") as disc:
            header = disc.read(0x20)
        if len(header) < 0x20 or int.from_bytes(header[0x1C:0x20], "big") != GC_MAGIC:
            die(f"{source} is not a GameCube disc image")
        if header[:6] != b"GZLE01":
            die(f"this is a GameCube disc, but not The Wind Waker (USA, GZLE01): its id is "
                f"{header[:6].decode(errors='replace')}")
        if header[7] != 0:
            die(f"this is GZLE01 revision {header[7]}; BlueWake supports revision 0 only")
        self.iso = source
        print(f"disc: {self.iso} (GZLE01 revision 0)")

    # --- tools built from source ---------------------------------------
    def build_dolrecomp(self):
        build = self.out / "dolrecomp"
        self.run("dolrecomp-configure", ["cmake", "-S", self.recompcore / "DolRecomp", "-B", build,
                                         "-G", "Ninja", "-DCMAKE_BUILD_TYPE=Release",
                                         "-DDOLRECOMP_WARNINGS_AS_ERRORS=OFF"])
        self.run("dolrecomp-build", ["cmake", "--build", build, "--target", "dolrecomp",
                                     "-j", self.args.jobs], ninja=True)
        return build / "dolrecomp"

    def configure_app(self):
        self.app_build = self.out / "app"
        self.run("app-configure", [
            "cmake", "-S", ROOT / "linux", "-B", self.app_build, "-G", "Ninja",
            "-DCMAKE_C_COMPILER=clang", "-DCMAKE_CXX_COMPILER=clang++",
            "-DCMAKE_BUILD_TYPE=Release", "-DBUILD_TESTING=OFF",
            "-DAURORA_DAWN_PROVIDER=package", "-DAURORA_DAWN_LINKAGE=static",
            "-DAURORA_SDL3_PROVIDER=vendor", "-DAURORA_SDL3_LINKAGE=static"])

    # --- 4 extract -------------------------------------------------------
    def extract(self, iso, game):
        self.run("disc-extract-build", ["cmake", "--build", self.app_build, "--target",
                                        "bluewake_disc_extract"], ninja=True)
        self.run("disc-extract", [self.app_build / "bluewake_disc_extract", iso, game])
        rels = len(list((game / "rels").glob("*.rel")))
        if rels != 415:
            die(f"expected 415 RELs in {game / 'rels'}, found {rels}")

    # --- 5 translate -------------------------------------------------------
    def translate(self, dol, out, rels=None, name="translate", sites=()):
        pending = out.with_name(out.name + ".new")
        shutil.rmtree(pending, ignore_errors=True)
        pending.mkdir(parents=True)
        self.run(f"{name}-dol", [self.dolrecomp, "--gamecube", "--backend", "c", "--cpu", "gekko",
                                 "--partition-instructions", "4096", *sites, dol, pending / "dol",
                                 "-j", self.args.jobs])
        if rels is not None:
            rels_arg = rels.as_posix().rstrip("/") + "/" if sites else rels
            self.run(f"{name}-rels", [self.dolrecomp, "--gamecube", "--backend", "c", "--cpu", "gekko",
                                      "--rel-base", "0xC0400000", *sites, rels_arg, pending / "rels",
                                      "-j", self.args.jobs])
        shutil.rmtree(out, ignore_errors=True)
        os.replace(pending, out)

    def composite(self, dol_dir, rels_dir, rels_bin, main_dol, out, name):
        shutil.rmtree(out, ignore_errors=True)
        self.run(name, [sys.executable, ROOT / "scripts/generate_composite.py", "--dol-dir", dol_dir,
                        "--rels-dir", rels_dir, "--rels-bin-dir", rels_bin, "--main-dol", main_dol,
                        "--output-dir", out])

    # --- 6 generate ------------------------------------------------------
    def generate(self):
        o = self.out
        new = o / "composite-src.new"
        self.composite(o / "translated/dol/generated", o / "translated/rels/generated/rels",
                       o / "game/rels", o / "game/main.dol", new, "composite-generate")
        expected = profile_value("COMPOSITE_DIGEST")
        digest = tree_digest(new)
        if digest == expected:
            print(f"composite source digest {digest}: the verified tree")
        elif self.args.accept_new_composite:
            print(f"composite source digest {digest} differs from the verified {expected} (accepted)")
        else:
            die(f"composite source digest {digest} differs from the verified {expected} "
                "(wrong disc revision or translator?); --accept-new-composite overrides")
        current = o / "composite-src"
        saved = (o / "composite-final.digest").read_text().strip() \
            if (o / "composite-final.digest").exists() else ""
        if current.exists() and saved and tree_digest(current) == saved:
            shutil.rmtree(new)
            print("the existing composite source is current")
            self.mods_pending = (o / "mods.done").read_text().strip() != "complete" \
                if (o / "mods.done").exists() else self.mods
        else:
            sync_tree(new, current)
            (o / "composite-src.digest").write_text(digest + "\n")
            (o / "composite-final.digest").write_text(digest + "\n")
            (o / "mods.done").write_text("pending\n")
            self.mods_pending = self.mods

    # --- 7 mods --------------------------------------------------------------
    def build_mods(self):
        self.run("mods", ["bash", ROOT / "scripts/mods/build_mods.sh", self.out, self.iso])
        o = self.out
        (o / "composite-final.digest").write_text(tree_digest(o / "composite-src") + "\n")
        (o / "mods.done").write_text("complete\n")

    # --- 8 compile -----------------------------------------------------------
    def compile_module(self):
        rc = self.recompcore
        build = self.out / "composite"
        self.run("composite-configure", [
            "cmake", "-S", ROOT / "cmake/composite", "-B", build, "-G", "Ninja",
            "-DCMAKE_C_COMPILER=gcc", "-DCMAKE_BUILD_TYPE=Release",
            f"-DCOMPOSITE_OPTIMIZATION_LEVEL={self.args.opt_level}",
            f"-DCOMPOSITE_DIR={self.out / 'composite-src'}",
            f"-DGXRUNTIME_DIR={rc / 'GXRuntime'}",
            f"-DABI_DIR={rc / 'Source/Core/Core/PowerPC/StaticRecomp'}"])
        self.run("composite-build", ["cmake", "--build", build, "-j", self.args.jobs], ninja=True)
        module = build / MODULE
        if not module.exists():
            die("the game module was not produced")
        return module

    # --- 9 app ---------------------------------------------------------------
    def build_app(self):
        self.run("app-build", ["cmake", "--build", self.app_build, "--target", "bluewake",
                               "-j", self.args.jobs], ninja=True)
        exe = self.app_build / "bluewake"
        if not exe.exists():
            die("bluewake was not produced")
        return exe

    # --- 10 package ----------------------------------------------------------
    def package(self, module):
        app = self.out / "BlueWake"
        (app / "game").mkdir(parents=True, exist_ok=True)
        (app / "dsp").mkdir(exist_ok=True)
        for f in sorted(self.app_build.iterdir()):
            if f.is_file() and f.name in ("bluewake", "bluewake_disc_extract"):
                shutil.copy2(f, app / f.name)
            elif f.is_file() and f.name == "initial_pipeline_cache.db":
                shutil.copy2(f, app / f.name)
            elif f.is_file() and (f.name.startswith("libSDL3") or f.name.startswith("libwebgpu_dawn")):
                shutil.copy2(f, app / f.name)
        shutil.copy2(module, app / MODULE)
        shutil.copy2(self.out / "game/main.dol", app / "game/main.dol")
        rels = app / "game/rels"
        shutil.rmtree(rels, ignore_errors=True)
        shutil.copytree(self.out / "game/rels", rels)
        for name in ("dsp_rom.bin", "dsp_coef.bin"):
            shutil.copy2(self.recompcore / "Data/Sys/GC" / name, app / "dsp" / name)
        self.place(self.iso, app / "game/GZLE01.iso")
        dirty = bool(self.git("status", "--porcelain"))
        provenance = {
            "profile": "bluewake-linux",
            "containsTranslatedGameCode": True,
            "source_commit": self.git("rev-parse", "HEAD"),
            "source_modified": dirty,
            "composite_digest": (self.out / "composite-src.digest").read_text().strip(),
            "mods": bool(self.mods),
            "compiler": "gcc",
            "module_sha256": sha256_file(app / MODULE),
            "built": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        (app / "BuilderProvenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
        (app / "README.txt").write_text(README)
        return app

    @staticmethod
    def place(source, target):
        if target.exists():
            if os.path.samefile(source, target) or \
                    (target.stat().st_size == source.stat().st_size and
                     target.stat().st_mtime_ns >= source.stat().st_mtime_ns):
                return
            target.unlink()
        try:
            os.link(source, target)
        except OSError:
            print(f"copying {source.name} into the app folder ({source.stat().st_size >> 20} MB)")
            shutil.copy2(source, target)

    # --- the pipeline ------------------------------------------------------------
    def build(self):
        args = self.args
        self.mods = not args.no_mods
        self.mods_pending = self.mods
        print(f"Building The Legend of Zelda: The Wind Waker (GameCube USA GZLE01 rev 0) "
              f"for Linux from {args.disc}")
        step("1/10 tools")
        self.check_tools()
        step("2/10 dependencies")
        self.dependencies()
        step("3/10 disc")
        self.disc()
        step("4/10 extract the game from the disc")
        self.dolrecomp = self.build_dolrecomp()
        self.configure_app()
        game = self.out / "game"
        stamp = self.out / "game.json"
        key = {"iso": str(self.iso), "size": self.iso.stat().st_size,
               "mtime": self.iso.stat().st_mtime_ns,
               "extractor": sha256_file(ROOT / "apple/ios/src/disc_import.c")}
        if (game / "main.dol").exists() and stamp.exists() and \
                json.loads(stamp.read_text()) == key:
            print(f"reusing main.dol and the RELs in {game}")
        else:
            self.extract(self.iso, game)
            stamp.write_text(json.dumps(key))
            print(f"main.dol and 415 RELs in {game}")
        step("5/10 translate")
        self.translate(game / "main.dol", self.out / "translated", game / "rels")
        chunks = len(list((self.out / "translated/dol/generated/chunks").glob("*.c")))
        print(f"translated: {chunks} DOL chunks and 415 RELs")
        step("6/10 generate the composite source")
        self.generate()
        if args.source_only:
            print(f"\nsource check passed: {self.out / 'composite-src'}. Rerun without "
                  "--source-only to compile and build the app.")
            return
        step("7/10 mods")
        if not self.mods:
            print("skipped")
        elif not self.mods_pending:
            print("mods already in the composite source")
        else:
            self.build_mods()
        step(f"8/10 compile the game module (-O{args.opt_level}; this is the long step)")
        start = time.monotonic()
        module = self.compile_module()
        print(f"game module: {module} ({int(time.monotonic() - start) // 60} min)")
        step("9/10 build the app")
        exe = self.build_app()
        print(f"app: {exe}")
        step("10/10 package")
        app = self.package(module)
        print(f"\nBlueWake: {app}")
        print(f"  run {app / 'bluewake'}")
        print("  It contains game code translated from your disc and a copy of the disc: keep it for yourself.")
        print("  Saves: ~/.local/share/BlueWake (outside the build).")


README = """BlueWake for Linux: The Legend of Zelda: The Wind Waker (GameCube USA),
statically recompiled from your own disc. See docs/LINUX.md in the source.

This folder is a personal build: gGZLE01_recomp.so is code translated from
your disc and game/ holds your disc image. Never share or upload it.

Run ./bluewake. Options (./bluewake --help lists them all):
  --widescreen    16:9 (--aspect 16:10 for 16:10)
  --smooth        Smooth Motion: 60 FPS with in-between frames
  --betterww      Better Wind Waker's settings (--options to change them)
  --fullscreen    start in fullscreen

Keyboard: arrows D-pad, J A, K B, U X, I Y, W/A/S/D control stick,
H/F/T/G C-stick, E/R L/R, Q Z, Return START. Game controllers work too.
Mouse: click the game and move the mouse to turn the camera; Esc releases it.
F11 fullscreen, F10 Smooth Motion, F9 frame rate.

Saves, settings and session logs: ~/.local/share/BlueWake
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("disc", type=Path, help="your GZLE01 revision 0 disc image (.iso or .gcm)")
    parser.add_argument("--out", type=Path, default=ROOT / "build/linux",
                        help="build directory (default build/linux; must be git-ignored inside the checkout)")
    parser.add_argument("--jobs", type=int, default=None,
                        help="parallel compile jobs (default: the cores, limited by free memory)")
    parser.add_argument("--opt-level", choices=("1", "2"), default="2",
                        help="game module optimization level")
    parser.add_argument("--no-mods", action="store_true",
                        help="skip the widescreen and Better Wind Waker variants")
    parser.add_argument("--accept-new-composite", action="store_true",
                        help="continue if the generated source differs from the verified one")
    parser.add_argument("--source-only", action="store_true",
                        help="stop after generating the source: checks tools, disc and translation in minutes")
    args = parser.parse_args()
    if args.jobs is None:
        args.jobs = default_jobs()
    if args.jobs < 1:
        parser.error("--jobs must be positive")
    args.out = args.out.resolve()
    try:
        rel = args.out.relative_to(ROOT)
    except ValueError:
        rel = None
    if rel is not None:
        if str(rel) == ".":
            parser.error("--out must not be the checkout itself; use build/linux")
        ignored = subprocess.run(["git", "check-ignore", "-q", str(args.out) + os.sep],
                                 cwd=ROOT).returncode == 0
        if not ignored:
            parser.error("--out inside this checkout must be git-ignored; use build/linux")
    args.out.mkdir(parents=True, exist_ok=True)
    try:
        Builder(args).build()
    except BuildError as error:
        print(f"\nbuilder: {error}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nbuilder: interrupted; rerun the same command to continue", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
