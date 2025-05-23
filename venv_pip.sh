#!/bin/bash

# Скрипт для создания venv и настройки VSCode в существующем проекте

# Создаем виртуальное окружение
python -m venv .venv

sleep 2

python.exe -m pip install --upgrade pip

# Активируем venv
source .venv/Scripts/activate


if [ ! -f "requirements.txt" ]; then
    echo "❌ Файл requirements.txt не найден. Убедитесь, что вы в корне проекта."
    exit 1
fi

# Устанавливаем зависимости
pip install -r requirements.txt

# Создаем/обновляем файл настроек VSCode
# mkdir -p .vscode
# cat > .vscode/settings.json <<EOL
# {
#     "python.pythonPath": ".venv/bin/python",
#     "python.linting.enabled": true,
#     "python.linting.pylintEnabled": true,
#     "python.formatting.autopep8Path": ".venv/bin/autopep8",
#     "python.formatting.blackPath": ".venv/bin/black",
#     "python.formatting.yapfPath": ".venv/bin/yapf",
#     "python.linting.banditPath": ".venv/bin/bandit",
#     "python.linting.flake8Path": ".venv/bin/flake8",
#     "python.linting.mypyPath": ".venv/bin/mypy",
#     "python.linting.pycodestylePath": ".venv/bin/pycodestyle",
#     "python.linting.pydocstylePath": ".venv/bin/pydocstyle",
#     "python.linting.pylintPath": ".venv/bin/pylint"
# }
# EOL

# Активируем venv
source .venv/Scripts/activate

echo "✅ Виртуальное окружение создано в .venv"