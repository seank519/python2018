import contextlib
import http.server
import os
import socketserver
import threading
import time
import webbrowser
from pathlib import Path

PORT = 8000
ROOT = Path(__file__).resolve().parent


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress default request logs for a cleaner console.
        pass


def serve():
    os.chdir(str(ROOT))
    handler = QuietHandler
    with contextlib.ExitStack() as stack:
        httpd = socketserver.TCPServer(("127.0.0.1", PORT), handler, bind_and_activate=False)
        httpd.allow_reuse_address = True
        httpd.server_bind()
        httpd.server_activate()
        stack.enter_context(httpd)

        def _serve():
            httpd.serve_forever()

        thread = threading.Thread(target=_serve, daemon=True)
        thread.start()

        url = f"http://127.0.0.1:{PORT}/index.html"
        print("로컬 서버를 시작했습니다.")
        print(f"브라우저에서 {url} 로 접속하세요.")
        try:
            webbrowser.open(url)
        except Exception:
            pass

        try:
            while thread.is_alive():
                time.sleep(0.2)
        except KeyboardInterrupt:
            print("\n서버를 종료합니다...")


if __name__ == "__main__":
    serve()
