# 🚀 Руководство по деплою

Подробная инструкция по развертыванию Contacts Comparator Web на различных платформах.

## 📋 Содержание

- [Локальный запуск](#локальный-запуск)
- [Heroku](#heroku)
- [Render.com](#rendercom)
- [Railway](#railway)
- [VPS/DigitalOcean](#vpsdigitalocean)
- [Docker](#docker)

---

## Локальный запуск

### Требования
- Python 3.7+
- pip

### Установка

```bash
# Клонируйте репозиторий
git clone https://github.com/ivanilin/contacts-comparator-web.git
cd contacts-comparator-web

# Создайте виртуальное окружение
python3 -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate

# Установите зависимости
pip install -r requirements.txt

# Запустите приложение
python app.py
```

Откройте http://localhost:5000

---

## Heroku

### Один клик деплой

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### Ручной деплой

1. Установите Heroku CLI
```bash
brew install heroku  # macOS
# или скачайте с https://devcenter.heroku.com/articles/heroku-cli
```

2. Войдите в Heroku
```bash
heroku login
```

3. Создайте приложение
```bash
heroku create your-app-name
```

4. Деплой
```bash
git push heroku main
```

5. Откройте приложение
```bash
heroku open
```

### Настройка

Установите переменные окружения:
```bash
heroku config:set SECRET_KEY="your-secret-key"
```

---

## Render.com

### Через веб-интерфейс

1. Зайдите на [Render.com](https://render.com)
2. Нажмите "New +" → "Web Service"
3. Подключите GitHub репозиторий
4. Настройки:
   - **Name**: contacts-comparator
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Нажмите "Create Web Service"

### Через Blueprint

Создайте `render.yaml`:
```yaml
services:
  - type: web
    name: contacts-comparator
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: SECRET_KEY
        generateValue: true
```

Затем деплой через Dashboard → "New" → "Blueprint"

---

## Railway

1. Зайдите на [Railway.app](https://railway.app)
2. Нажмите "New Project" → "Deploy from GitHub repo"
3. Выберите репозиторий
4. Railway автоматически определит Python и запустит приложение
5. Добавьте переменные окружения в Settings

---

## VPS/DigitalOcean

### Требования
- Ubuntu 20.04+ или Debian 10+
- Nginx
- Python 3.7+

### Установка на сервер

```bash
# Обновите систему
sudo apt update && sudo apt upgrade -y

# Установите зависимости
sudo apt install python3-pip python3-venv nginx -y

# Клонируйте репозиторий
cd /var/www
sudo git clone https://github.com/ivanilin/contacts-comparator-web.git
cd contacts-comparator-web

# Создайте виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt
pip install gunicorn
```

### Настройка Systemd

Создайте `/etc/systemd/system/contacts-comparator.service`:

```ini
[Unit]
Description=Contacts Comparator Web Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/contacts-comparator-web
Environment="PATH=/var/www/contacts-comparator-web/venv/bin"
ExecStart=/var/www/contacts-comparator-web/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

Запустите сервис:
```bash
sudo systemctl daemon-reload
sudo systemctl start contacts-comparator
sudo systemctl enable contacts-comparator
```

### Настройка Nginx

Создайте `/etc/nginx/sites-available/contacts-comparator`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        client_max_body_size 20M;
    }
}
```

Активируйте конфигурацию:
```bash
sudo ln -s /etc/nginx/sites-available/contacts-comparator /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### SSL с Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

---

## Docker

### Создайте Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Создайте docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./uploads:/app/uploads
      - ./results:/app/results
    environment:
      - SECRET_KEY=${SECRET_KEY}
    restart: unless-stopped
```

### Запуск

```bash
# Сборка образа
docker build -t contacts-comparator .

# Запуск контейнера
docker run -p 5000:5000 contacts-comparator

# Или с docker-compose
docker-compose up -d
```

---

## Переменные окружения

Создайте `.env` файл:

```env
SECRET_KEY=your-super-secret-key-change-this
FLASK_ENV=production
MAX_FILE_SIZE=16777216
```

Загрузите в приложение:
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## Мониторинг

### Логи

**Heroku:**
```bash
heroku logs --tail
```

**Systemd:**
```bash
sudo journalctl -u contacts-comparator -f
```

**Docker:**
```bash
docker logs -f container-name
```

---

## Troubleshooting

### Ошибка импорта модулей
Убедитесь, что `contacts_comparator.py` находится в корне проекта

### Ошибка 502 Bad Gateway
Проверьте, что Gunicorn запущен:
```bash
sudo systemctl status contacts-comparator
```

### Файлы не загружаются
Проверьте права доступа к папкам uploads и results:
```bash
sudo chown -R www-data:www-data uploads results
```

---

## 🎉 Готово!

Ваш сервис теперь доступен онлайн!

Не забудьте:
- [ ] Изменить SECRET_KEY
- [ ] Настроить домен
- [ ] Установить SSL сертификат
- [ ] Настроить бэкапы
- [ ] Мониторинг логов

---

Если возникли проблемы, создайте [Issue на GitHub](https://github.com/ivanilin/contacts-comparator-web/issues)
