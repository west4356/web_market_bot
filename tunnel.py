import re
import subprocess
import time
import os
import sys
import threading
import logging
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import config

logger = logging.getLogger(__name__)

CLOUDFLARED_PATH = Path(__file__).resolve().parent / "cloudflared.exe"

class CloudflareTunnel:
    def __init__(self, port: int = 8080):
        self.port = port
        self.process = None
        self.public_url = None
        self._thread = None
        self._stop_event = threading.Event()

    def start(self, timeout: int = 25) -> str:
        if not CLOUDFLARED_PATH.exists():
            raise FileNotFoundError(f"cloudflared.exe not found at {CLOUDFLARED_PATH}")

        cmd = [str(CLOUDFLARED_PATH), "tunnel", "--url", f"http://127.0.0.1:{self.port}", "--no-autoupdate"]
        
        # Start subprocess
        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        )

        url_found = threading.Event()

        def _monitor():
            pattern = re.compile(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com")
            while not self._stop_event.is_set():
                line = self.process.stdout.readline()
                if not line:
                    break
                match = pattern.search(line)
                if match and not self.public_url:
                    self.public_url = match.group(0)
                    config.WEBAPP_URL = self.public_url
                    url_found.set()

        self._thread = threading.Thread(target=_monitor, daemon=True)
        self._thread.start()

        if url_found.wait(timeout=timeout):
            return self.public_url
        else:
            return None

    def stop(self):
        self._stop_event.set()
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=3)
            except Exception:
                self.process.kill()

if __name__ == "__main__":
    t = CloudflareTunnel(8080)
    print("Starting Cloudflare tunnel on port 8080...")
    url = t.start()
    print("Tunnel URL:", url)
    if url:
        print("Press Ctrl+C to exit")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            t.stop()
