#!/bin/bash

# Скрипт для создания venv и настройки VSCode в существующем проекте

# Чистим старое окружение
echo "Cleaning previous venv..."
SCRIPT_DIR="$(dirname "$(realpath "$0")")"
VENV_DIR="$SCRIPT_DIR/.venv"
rm -rf "$VENV_DIR"

# Создаем виртуальное окружение
python -m venv .venv

# Активируем venv
source .venv/Scripts/activate


if [ ! -f "requirements.txt" ]; then
    echo "❌ Файл requirements.txt не найден. Убедитесь, что вы в корне проекта."
    exit 1
fi

check_internet() {
    # Определяем "чёрную дыру" для вывода
    if [[ "$OS" == "Windows_NT" && -z "$BASH_VERSION" ]]; then
        # cmd.exe или PowerShell
        NULL_DEV="nul"
    else
        # bash (Linux, macOS, Git Bash, WSL и т.д.)
        NULL_DEV="/dev/null"
    fi

    if [[ "$OS" == "Windows_NT" ]]; then
        ping -n 2 -w 3000 8.8.8.8 >"$NULL_DEV" 2>&1
    else
        ping -q -c 2 -W 3 8.8.8.8 >"$NULL_DEV" 2>&1
    fi
    return $?
}

# Устанавливаем зависимости
if check_internet; then
    echo "Интернет соединение доступно, устанавливаем зависимости из интернета"
    python.exe -m pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "Интернет соединение недоступно, устанавливаем зависимости локально"
    pip install -r requirements.txt --no-index -f d:\\temp\\python_Library
fi

echo "✅ Виртуальное окружение создано в .venv"