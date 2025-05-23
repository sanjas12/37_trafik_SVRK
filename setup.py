# setup.py
from cx_Freeze import setup, Executable
import os
from pathlib import Path

# ===== Конфигурация проекта =====
PROJECT_NAME = "trafik_SVKR"
VERSION = "0.1.0"
MAIN_SCRIPT = "main.py"
README_FILE = "Readme.md"
CONFIG_FILE = "config.py"

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
        # Создаем пустую папку data_in
        # (os.path.join("empty_dir_placeholder"), "data_in"),
    ],
}

# Создаем временную пустую папку для включения в сборку
empty_dir = Path("data_in")
empty_dir.mkdir(exist_ok=True)

# GUI/Console настройки
base = None  # Оставляем консоль открытой

setup(
    name=PROJECT_NAME,
    version=VERSION,
    description="Traffic Analyzer for SVKR",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            MAIN_SCRIPT,
            target_name=PROJECT_NAME,
            base=base,
        )
    ],
)
