import subprocess
import sys
import time


def main():
    print("🚀 Запускаем full-stack приложение...")

    print("⏳ Поднимаю Python FastAPI (бэкенд)...")
    backend_process = subprocess.Popen([sys.executable, "launcher.py"])

    print("⏳ Поднимаю Angular (фронтенд)...")
    frontend_process = subprocess.Popen("npm run start", cwd="frontend", shell=True)

    try:
        print("\n✅ Все сервисы запущены!")
        print("💡 Для остановки нажми Ctrl+C в этом окне\n")

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\n🛑 Получен сигнал остановки (Ctrl+C). Закрываю процессы...")

        backend_process.terminate()
        frontend_process.terminate()

        print("👋 Серверы успешно остановлены.")


if __name__ == "__main__":
    main()
