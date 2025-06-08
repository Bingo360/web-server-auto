#!/bin/bash

# Проверка прав root
if [ "$(id -u)" -ne 0 ]; then
  echo "Этот скрипт должен запускаться с правами root" >&2
  exit 1
fi

# Установка зависимостей
apt-get update
apt-get install -y python3 python3-pip python3-venv git nginx

# Клонирование репозитория (если запускается не через git)
if [ ! -d "/opt/web-server-auto" ]; then
  git clone https://github.com/web-server-auto.git /opt/web-server-auto
fi

# Создание виртуального окружения
python3 -m venv /opt/web-server-auto/venv
source /opt/web-server-auto/venv/bin/activate

# Установка Python зависимостей
pip install -r /opt/web-server-auto/requirements.txt

# Запуск основного скрипта развертывания
python3 /opt/web-server-auto/deploy.py

echo "Установка завершена! Веб-сервер доступен по адресу http://ваш-сервер"
