# 🚀 Деплой на 10xfounder.ru

## Вариант 1: Render.com → Поддомен (Рекомендуется)

### Шаг 1: Деплой на Render.com

1. Перейдите на https://render.com
2. Войдите через GitHub
3. Нажмите **New** → **Web Service**
4. Выберите репозиторий `ironfelix/10xfounder`
5. Выберите ветку `contacts-comparator-web`

**Настройки:**
```
Name: contacts-comparator
Region: Frankfurt (ближайший к России)
Branch: contacts-comparator-web
Root Directory: (оставить пустым)
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

6. Выберите **Free** план
7. Нажмите **Create Web Service**
8. Дождитесь окончания деплоя (2-3 минуты)

### Шаг 2: Получите URL от Render

После деплоя вы получите URL вида:
```
https://contacts-comparator.onrender.com
```

### Шаг 3: Добавьте Custom Domain в Render

1. В панели вашего сервиса на Render
2. Перейдите в **Settings** → **Custom Domains**
3. Нажмите **Add Custom Domain**
4. Введите: `contacts.10xfounder.ru`
5. Render покажет инструкцию по настройке DNS

### Шаг 4: Настройте DNS для 10xfounder.ru

Зайдите в панель управления вашего регистратора домена (где куплен 10xfounder.ru):

**Добавьте CNAME запись:**
```
Тип: CNAME
Имя: contacts
Значение: contacts-comparator.onrender.com
TTL: 3600
```

Или если Render даст другие инструкции, следуйте им.

### Шаг 5: Дождитесь распространения DNS

Обычно занимает 5-60 минут. Проверить можно командой:
```bash
dig contacts.10xfounder.ru
```

### Готово! 🎉

Ваш сервис будет доступен по адресу:
```
https://contacts.10xfounder.ru
```

---

## Вариант 2: VPS с Nginx (если у вас свой сервер)

### Требования
- VPS с Ubuntu/Debian
- Домен 10xfounder.ru уже настроен на ваш VPS
- SSH доступ к серверу

### Шаг 1: Подключитесь к серверу

```bash
ssh root@your-server-ip
```

### Шаг 2: Установите зависимости

```bash
# Обновите систему
sudo apt update && sudo apt upgrade -y

# Установите Python и Nginx
sudo apt install python3-pip python3-venv nginx -y
```

### Шаг 3: Клонируйте проект

```bash
cd /var/www
sudo git clone https://github.com/ironfelix/10xfounder.git contacts-comparator
cd contacts-comparator
sudo git checkout contacts-comparator-web
```

### Шаг 4: Настройте виртуальное окружение

```bash
sudo python3 -m venv venv
sudo venv/bin/pip install -r requirements.txt
sudo venv/bin/pip install gunicorn
```

### Шаг 5: Создайте systemd сервис

Создайте файл `/etc/systemd/system/contacts-comparator.service`:

```ini
[Unit]
Description=Contacts Comparator Web Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/contacts-comparator
Environment="PATH=/var/www/contacts-comparator/venv/bin"
Environment="SECRET_KEY=измените-это-на-случайную-строку"
ExecStart=/var/www/contacts-comparator/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

### Шаг 6: Запустите сервис

```bash
sudo systemctl daemon-reload
sudo systemctl start contacts-comparator
sudo systemctl enable contacts-comparator
sudo systemctl status contacts-comparator
```

### Шаг 7: Настройте Nginx

Создайте файл `/etc/nginx/sites-available/contacts.10xfounder.ru`:

```nginx
server {
    listen 80;
    server_name contacts.10xfounder.ru;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Увеличиваем лимит для загрузки файлов
        client_max_body_size 20M;
    }

    location /static {
        alias /var/www/contacts-comparator/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### Шаг 8: Активируйте конфигурацию

```bash
sudo ln -s /etc/nginx/sites-available/contacts.10xfounder.ru /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Шаг 9: Установите SSL (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d contacts.10xfounder.ru
```

Certbot автоматически настроит HTTPS и перенаправление с HTTP.

### Шаг 10: Настройте DNS

В панели управления доменом добавьте A-запись:

```
Тип: A
Имя: contacts
Значение: IP-адрес-вашего-сервера
TTL: 3600
```

### Готово! 🎉

Ваш сервис доступен по адресу:
```
https://contacts.10xfounder.ru
```

---

## Вариант 3: GitHub Pages (только для статики)

**НЕ ПОДХОДИТ** для этого проекта, так как GitHub Pages не поддерживает серверные приложения (Flask).

---

## Вариант 4: Railway.app

1. Зайдите на https://railway.app
2. Войдите через GitHub
3. New Project → Deploy from GitHub repo
4. Выберите `ironfelix/10xfounder`, ветка `contacts-comparator-web`
5. Railway автоматически задеплоит
6. В настройках добавьте Custom Domain: `contacts.10xfounder.ru`
7. Настройте CNAME в DNS:
   ```
   contacts.10xfounder.ru → your-app.up.railway.app
   ```

---

## Сравнение вариантов

| Вариант       | Сложность | Стоимость      | Скорость деплоя | SSL | Производительность |
|---------------|-----------|----------------|-----------------|-----|-------------------|
| Render.com    | ⭐        | Бесплатно*     | 2 минуты        | ✅   | ⭐⭐⭐            |
| Railway       | ⭐⭐      | Бесплатно*     | 2 минуты        | ✅   | ⭐⭐⭐⭐          |
| VPS + Nginx   | ⭐⭐⭐⭐  | ~$5-10/месяц   | 30 минут        | ✅   | ⭐⭐⭐⭐⭐        |

*Бесплатный план имеет ограничения (сервис засыпает при неактивности)

---

## 🎯 Рекомендация

Для начала используйте **Render.com**:
- ✅ Проще всего настроить
- ✅ Бесплатно
- ✅ Автоматический SSL
- ✅ Легко обновлять (git push)
- ⚠️ Засыпает после 15 мин неактивности (первый запрос медленный)

Если нужна высокая производительность → переходите на VPS.

---

## 📝 Чеклист после деплоя

- [ ] Проверьте работу по URL
- [ ] Загрузите тестовые файлы
- [ ] Проверьте скачивание результатов
- [ ] Настройте мониторинг (если на VPS)
- [ ] Добавьте ссылку на главный сайт 10xfounder.ru

---

## 🆘 Troubleshooting

### Render.com не деплоится
- Проверьте, что выбрана правильная ветка `contacts-comparator-web`
- Проверьте логи в Render Dashboard

### DNS не распространяется
- Подождите до 24 часов (обычно 1-2 часа)
- Проверьте через https://dnschecker.org

### Ошибка 502 Bad Gateway (VPS)
```bash
sudo systemctl status contacts-comparator
sudo journalctl -u contacts-comparator -n 50
```

---

Нужна помощь? Создайте issue: https://github.com/ironfelix/10xfounder/issues
