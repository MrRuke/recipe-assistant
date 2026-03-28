import threading
import time
import webbrowser

import uvicorn

from main import app


def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")


if __name__ == "__main__":
    print("Запуск сервера рецептов...")

    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    time.sleep(1.5)

    try:
        print("Сервер работает. Для остановки нажми Ctrl+C в этой консоли.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nОстановка сервера...")
