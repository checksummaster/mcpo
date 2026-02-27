from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

import typer


@dataclass(frozen=True)
class PackagingTarget:
    pyinstaller_name: str
    binary_name: str
    description: str
    extra_args: tuple[str, ...] = ()


ROOT = Path(__file__).resolve().parents[2]
ENTRY_SCRIPT = ROOT / "scripts" / "mcpo_entry.py"
DATA_FILES = (
    (ROOT / "src" / "mcpo" / "utils" / "oauth_callback.html", "mcpo/utils"),
)
TARGETS: Mapping[str, PackagingTarget] = {
    "win32": PackagingTarget(
        pyinstaller_name="mcpo",
        binary_name="mcpo.exe",
        description="Windows x86_64 executable",
    ),
    "wsl": PackagingTarget(
        pyinstaller_name="mcpo",
        binary_name="mcpo",
        description="WSL/Linux x86_64 executable",
    ),
}
DEFAULT_BUILD_ROOT = ROOT / "build" / "pyinstaller"
DEFAULT_ARCHIVE_ROOT = ROOT / "build" / "packages"

app = typer.Typer(help="Bundle mcpo into standalone executables for Windows and WSL.")


def ensure_pyinstaller_available() -> None:
    if importlib.util.find_spec("PyInstaller") is None:
        raise typer.Exit(
            "PyInstaller is not installed. Run `uv sync --dev` to install development dependencies first.",
            code=1,
        )


def ensure_entry_script_exists() -> None:
    if not ENTRY_SCRIPT.exists():
        raise typer.Exit(
            f"Entry script missing ({ENTRY_SCRIPT}). Create scripts/mcpo_entry.py before packaging.",
            code=1,
        )


def format_data_arg(source: Path, destination: str) -> str:
    return f"{source}{os.pathsep}{destination}"


def run_pyinstaller(target_config: PackagingTarget, workspace: Path) -> Path:
    work_path = workspace / "build"
    release_path = workspace / "release"
    spec_path = workspace / "spec"
    for path in (work_path, release_path, spec_path):
        shutil.rmtree(path, ignore_errors=True)
        path.mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--clean",
        "--noconfirm",
        "--onefile",
        "--name",
        target_config.pyinstaller_name,
        "--workpath",
        str(work_path),
        "--distpath",
        str(release_path),
        "--specpath",
        str(spec_path),
    ]
    for data_source, data_dest in DATA_FILES:
        if data_source.exists():
            command.extend(["--add-data", format_data_arg(data_source, data_dest)])
    command.extend(target_config.extra_args)
    command.append(str(ENTRY_SCRIPT))
    typer.echo(
        "Running PyInstaller for %s: %s" % (target_config.description, " ".join(command))
    )
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as exc:
        raise typer.Exit(
            "PyInstaller failed for %s (exit code %s)." % (target_config.description, exc.returncode),
            code=exc.returncode,
        )
    binary_path = release_path / target_config.binary_name
    if not binary_path.exists():
        raise typer.Exit(
            f"PyInstaller did not create the expected binary at {binary_path}.",
            code=1,
        )
    return binary_path


def stage_release(target_name: str, binary_path: Path, archive_root: Path, workspace: Path) -> Path:
    staging = workspace / "staging"
    shutil.rmtree(staging, ignore_errors=True)
    staging.mkdir(parents=True, exist_ok=True)
    shutil.copy2(binary_path, staging / binary_path.name)
    for extra in (ROOT / "README.md", ROOT / "LICENSE"):
        if extra.exists():
            shutil.copy2(extra, staging / extra.name)
    archive_root.mkdir(parents=True, exist_ok=True)
    archive_base = archive_root / f"mcpo-{target_name}"
    archive_path = shutil.make_archive(str(archive_base), "zip", root_dir=staging)
    return Path(archive_path)


def package_target(
    target_key: str,
    build_root: Path,
    archive_root: Path,
    keep_build: bool,
) -> Path:
    ensure_pyinstaller_available()
    ensure_entry_script_exists()
    target_config = TARGETS[target_key]
    workspace = Path(build_root) / target_key
    workspace.mkdir(parents=True, exist_ok=True)
    binary_path = run_pyinstaller(target_config, workspace)
    archive_path = stage_release(target_key, binary_path, Path(archive_root), workspace)
    typer.echo("Packaged %s artifact at %s" % (target_key, archive_path))
    if not keep_build:
        shutil.rmtree(workspace, ignore_errors=True)
    return archive_path


@app.command()
def win32(
    build_root: Path = typer.Option(
        DEFAULT_BUILD_ROOT,
        help="Directory that holds the PyInstaller build workspace.",
    ),
    archive_root: Path = typer.Option(
        DEFAULT_ARCHIVE_ROOT,
        help="Directory that will contain the zipped artifacts.",
    ),
    keep_build: bool = typer.Option(
        False,
        "--keep-build",
        help="Retain the intermediate PyInstaller outputs for debugging.",
    ),
) -> None:
    package_target("win32", build_root, archive_root, keep_build)


@app.command()
def wsl(
    build_root: Path = typer.Option(
        DEFAULT_BUILD_ROOT,
        help="Directory that holds the PyInstaller build workspace.",
    ),
    archive_root: Path = typer.Option(
        DEFAULT_ARCHIVE_ROOT,
        help="Directory that will contain the zipped artifacts.",
    ),
    keep_build: bool = typer.Option(
        False,
        "--keep-build",
        help="Retain the intermediate PyInstaller outputs for debugging.",
    ),
) -> None:
    package_target("wsl", build_root, archive_root, keep_build)


@app.command(name="all")
def package_all(
    build_root: Path = typer.Option(
        DEFAULT_BUILD_ROOT,
        help="Directory that holds the PyInstaller build workspace.",
    ),
    archive_root: Path = typer.Option(
        DEFAULT_ARCHIVE_ROOT,
        help="Directory that will contain the zipped artifacts.",
    ),
    keep_build: bool = typer.Option(
        False,
        "--keep-build",
        help="Retain the intermediate PyInstaller outputs for debugging.",
    ),
) -> None:
    for target_key in TARGETS:
        package_target(target_key, build_root, archive_root, keep_build)


@app.command()
def clean(
    build_root: Path = typer.Option(
        DEFAULT_BUILD_ROOT,
        help="Directory that holds the PyInstaller build workspace.",
    ),
    archive_root: Path = typer.Option(
        DEFAULT_ARCHIVE_ROOT,
        help="Directory that will contain the zipped artifacts.",
    ),
) -> None:
    for path in (build_root, archive_root):
        if path.exists():
            shutil.rmtree(path, ignore_errors=True)
            typer.echo("Removed %s" % path)
        else:
            typer.echo("Nothing to clean at %s" % path)
