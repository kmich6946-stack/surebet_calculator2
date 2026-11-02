import subprocess
import sys
import time
import urllib.error
import urllib.request
import webbrowser
from pathlib import Path


APP_DIR = Path(__file__).resolve().parent
URL = "http://127.0.0.1:8765/"
EXPECTED_TITLE = b"<title>Surebet Calculator"


def is_running():
    try:
        with urllib.request.urlopen(URL, timeout=1) as response:
            page = response.read(16 * 1024)
            return response.status == 200 and EXPECTED_TITLE in page
    except (OSError, urllib.error.URLError):
        return False


def open_browser():
    print(f"Calculator ready at {URL}")
    if not webbrowser.open(URL):
        print("Open the address above in your browser.")


def main():
    if not (APP_DIR / "app.py").is_file():
        raise SystemExit("Could not find app.py in the calculator folder.")

    if is_running():
        print("Calculator server is already running.")
        open_browser()
        return

    server = subprocess.Popen(
        [sys.executable, str(APP_DIR / "app.py")],
        cwd=APP_DIR,
    )
    try:
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            if server.poll() is not None:
                raise SystemExit(
                    "The calculator server stopped during startup. "
                    "Check the error shown above."
                )
            if is_running():
                open_browser()
                server.wait()
                return
            time.sleep(0.25)
        server.terminate()
        server.wait(timeout=5)
        raise SystemExit(
            "The calculator did not become ready within 30 seconds. "
            "Check the server output above."
        )
    except KeyboardInterrupt:
        if server.poll() is None:
            server.terminate()
            server.wait(timeout=5)


if __name__ == "__main__":
    main()
