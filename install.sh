if [ "$(id -u)" -ne 0 ]; then
  echo "Этот скрипт должен запускаться с правами root" >&2
  exit 1
fi

apt-get update
apt-get install -y python3 python3-pip python3-venv git nginx

python3 -m venv /opt/web-server-auto/venv
source /opt/web-server-auto/venv/bin/activate

pip install -r /opt/web-server-auto/requirements.txt

# запуск скрипта
python3 /opt/web-server-auto/deploy.py

echo "Установка завершена! Веб-сервер доступен по адресу http://localhost"
