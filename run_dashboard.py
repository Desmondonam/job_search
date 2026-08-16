import argparse
import os
import signal
import subprocess
import sys
import time


def find_free_port(start_port: int = 8501, max_tries: int = 20) -> int:
    import socket

    for port in range(start_port, start_port + max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise RuntimeError(f"No free port found between {start_port} and {start_port + max_tries - 1}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the local job dashboard with a fallback port.")
    parser.add_argument("--port", type=int, default=8501)
    args = parser.parse_args()

    port = args.port
    try:
        import socket

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            probe.bind(("127.0.0.1", port))
    except OSError:
        port = find_free_port(args.port)
        print(f"Port {args.port} is busy; using port {port} instead.")

    env = os.environ.copy()
    env["STREAMLIT_SERVER_HEADLESS"] = "true"
    env["STREAMLIT_SERVER_ADDRESS"] = "127.0.0.1"
    env["STREAMLIT_SERVER_PORT"] = str(port)

    cmd = [sys.executable, "-m", "streamlit", "run", "src/job_search_app/dashboard.py"]
    process = subprocess.Popen(cmd, env=env)

    def _shutdown(signum, frame):
        process.terminate()
        raise SystemExit(0)

    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    try:
        while True:
            time.sleep(1)
            if process.poll() is not None:
                return process.returncode
    except SystemExit:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
