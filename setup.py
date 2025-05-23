# setup.py
from cx_Freeze import setup, Executable
import sys
import os
from pathlib import Path

# ===== Конфигурация проекта =====
PROJECT_NAME = "trafik_SVKR"
VERSION = "0.1.0"
MAIN_SCRIPT = "main.py"  # Главный скрипт
README_FILE = "Readme.md"
CONFIG_FILE = "config.py"  # Файл с настройками

# ===== Создаем папку data_in =====
# Путь к папке в собранном проекте
build_dir = "build"  # или другой каталог сборки
# data_in_path = os.path.join(build_dir, f"exe.{sys.platform}-{sys.version_info.major}.{sys.version_info.minor}", "data_in")

# Создаем папку, если её нет
# Path(data_in_path).mkdir(parents=True, exist_ok=True)

# ===== Настройки сборки =====
build_exe_options = {
    "excludes": [
        "tkinter", "unittest", "http", "PyQt5.QtOpenGL",
        "pydoc_data", "email", "sqlite3", "test",
    ],
    "optimize": 1,
    "include_files": [
        (README_FILE, 'Readme.md'),
        (CONFIG_FILE, 'config.py'),
        # Добавляем пустую папку data_in
        ("", "data_in"),  # Пустая строка создаст папку
    ],
}

# ===== Настройки запуска =====
# Для Windows: оставляем консоль открытой (base=None)
base = None  # Оставляем None для отображения консоли

# Если нужно GUI приложение с консолью для отладки:
if sys.platform == "win32":
    # base = "Win32GUI"  # Закомментировано для отображения консоли
    pass

setup(
    name=PROJECT_NAME,
    version=VERSION,
    description="Traffic Analyzer for SVKR",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            MAIN_SCRIPT,
            target_name=PROJECT_NAME,
            base=base,  # None сохраняет консоль
            # icon="icon.ico"
        )
    ],
)

# Дополнительное создание папки после сборки
def post_build():
    final_data_in = os.path.join(build_dir, "data_in")
    Path(final_data_in).mkdir(exist_ok=True)

# Вызываем post-обработку
post_build()