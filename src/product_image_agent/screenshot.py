from __future__ import annotations

import os
import platform
import shutil
import subprocess
from pathlib import Path


DEFAULT_WINDOW_SIZE = "1440,1200"


def candidate_browser_paths() -> list[str]:
    system = platform.system().lower()
    if system == "windows":
        program_files = [os.environ.get("PROGRAMFILES"), os.environ.get("PROGRAMFILES(X86)"), os.environ.get("LOCALAPPDATA")]
        roots = [Path(item) for item in program_files if item]
        candidates: list[str] = []
        for root in roots:
            candidates.extend(
                [
                    str(root / "Google" / "Chrome" / "Application" / "chrome.exe"),
                    str(root / "Microsoft" / "Edge" / "Application" / "msedge.exe"),
                ]
            )
        return candidates
    if system == "darwin":
        return [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
        ]
    return [
        "google-chrome",
        "google-chrome-stable",
        "chromium",
        "chromium-browser",
        "microsoft-edge",
    ]


def find_browser(explicit_browser: Path | None = None) -> Path | str:
    if explicit_browser is not None:
        if not explicit_browser.exists():
            raise FileNotFoundError(f"Browser executable not found: {explicit_browser}")
        return explicit_browser
    for candidate in candidate_browser_paths():
        path = Path(candidate)
        if path.exists():
            return path
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
    raise FileNotFoundError(
        "No Chrome/Chromium/Edge executable was found. Install Chrome/Chromium/Edge or pass --browser <path>."
    )


def build_screenshot_command(
    browser: Path | str,
    report_html: Path,
    output_png: Path,
    window_size: str = DEFAULT_WINDOW_SIZE,
) -> list[str]:
    report_uri = report_html.resolve().as_uri()
    return [
        str(browser),
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--window-size={window_size}",
        f"--screenshot={output_png.resolve()}",
        report_uri,
    ]


def capture_report_screenshot(
    report_html: Path,
    output_png: Path,
    browser: Path | None = None,
    window_size: str = DEFAULT_WINDOW_SIZE,
) -> Path:
    if not report_html.exists():
        raise FileNotFoundError(f"Report HTML not found: {report_html}")
    selected_browser = find_browser(browser)
    output_png.parent.mkdir(parents=True, exist_ok=True)
    command = build_screenshot_command(selected_browser, report_html, output_png, window_size)
    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError(
            "Browser screenshot command failed with exit code "
            f"{completed.returncode}.\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    if not output_png.exists():
        raise RuntimeError("Browser command finished but screenshot was not created: " + str(output_png))
    return output_png
