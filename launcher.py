import threading
import time

import uvicorn


def run_server():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, log_level="error")


if __name__ == "__main__":
    print("Running...")

    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    time.sleep(1.5)

    try:
        print("Server works. To stop use Ctrl+C.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping...")
