import os
import subprocess
from pathlib import Path

class WebServerDeployer:
    def __init__(self):
        self.base_dir = Path("/opt/web-server-auto")
        self.config_dir = self.base_dir / "config"
        
    def run_command(self, cmd, sudo=False):
        # проверка на sudo
        if sudo:
            cmd = f"sudo {cmd}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Ошибка выполнения команды: {cmd}")
            print(result.stderr)
            exit(1)
        return result.stdout

    def configure_nginx(self):
        print("Настройка Nginx...")
       
        with open(self.config_dir / "nginx.conf", "r") as f:
            nginx_config = f.read()
       
        nginx_config = nginx_config.replace("${DOMAIN}", "test.com")
        
        with open("/etc/nginx/sites-available/webapp", "w") as f:
            f.write(nginx_config)
        
        # активируем сайт
        self.run_command("ln -sf /etc/nginx/sites-available/webapp /etc/nginx/sites-enabled/", sudo=True)
        self.run_command("nginx -t", sudo=True)
        self.run_command("systemctl reload nginx", sudo=True)

    def setup_systemd(self):
        print("Настройка systemd сервиса...")
        # шаблон
        with open(self.config_dir / "service.conf", "r") as f:
            service_config = f.read()
        
        with open("/etc/systemd/system/webapp.service", "w") as f:
            f.write(service_config)
        
        self.run_command("systemctl daemon-reload", sudo=True)
        self.run_command("systemctl enable --now webapp.service", sudo=True)

    def deploy(self):
        self.configure_nginx()
        self.setup_systemd()
        print("Веб-сервер успешно развернут!")

if __name__ == "__main__":
    deployer = WebServerDeployer()
    deployer.deploy()
