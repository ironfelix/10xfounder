# 🔗 Интеграция в 10xfounder.ru/comparator

Руководство по размещению сервиса на **10xfounder.ru/comparator** вместо поддомена.

## 🎯 Результат

Сервис будет доступен по адресу:
```
https://10xfounder.ru/comparator
```

---

## Вариант 1: Nginx Reverse Proxy (Рекомендуется)

### Если у вас уже есть сайт на 10xfounder.ru

1. **Задеплойте сервис на Render/Railway/VPS** (получите URL, например: `https://contacts-comparator.onrender.com`)

2. **Настройте Nginx на вашем основном сервере**

Отредактируйте конфигурацию Nginx для 10xfounder.ru:

```nginx
server {
    listen 443 ssl http2;
    server_name 10xfounder.ru www.10xfounder.ru;

    # SSL настройки
    ssl_certificate /etc/letsencrypt/live/10xfounder.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/10xfounder.ru/privkey.pem;

    # Основной сайт
    location / {
        # Ваш основной сайт (статика или другое приложение)
        root /var/www/10xfounder.ru;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # Сервис сравнения контактов
    location /comparator {
        proxy_pass https://contacts-comparator.onrender.com/comparator;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Для загрузки файлов
        client_max_body_size 20M;
    }
}
```

3. **Перезагрузите Nginx**
```bash
sudo nginx -t
sudo systemctl reload nginx
```

### Готово! 🎉
Сервис доступен на: **https://10xfounder.ru/comparator**

---

## Вариант 2: Полный деплой на одном сервере

Если весь сайт 10xfounder.ru на вашем VPS:

### 1. Клонируйте проект

```bash
cd /var/www
sudo git clone https://github.com/ironfelix/10xfounder.git comparator
cd comparator
sudo git checkout contacts-comparator-web
```

### 2. Настройте окружение

```bash
sudo python3 -m venv venv
sudo venv/bin/pip install -r requirements.txt
sudo venv/bin/pip install gunicorn
```

### 3. Создайте systemd сервис

Файл `/etc/systemd/system/comparator.service`:

```ini
[Unit]
Description=Contacts Comparator Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/comparator
Environment="PATH=/var/www/comparator/venv/bin"
ExecStart=/var/www/comparator/venv/bin/gunicorn -w 4 -b 127.0.0.1:5001 app:app

[Install]
WantedBy=multi-user.target
```

### 4. Запустите сервис

```bash
sudo systemctl daemon-reload
sudo systemctl start comparator
sudo systemctl enable comparator
```

### 5. Настройте Nginx

В конфигурации 10xfounder.ru добавьте:

```nginx
location /comparator {
    proxy_pass http://127.0.0.1:5001/comparator;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    client_max_body_size 20M;
}
```

### 6. Перезагрузите Nginx

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

## Вариант 3: GitHub Pages + Cloudflare Workers

Если основной сайт на GitHub Pages:

### 1. Деплой сервиса на Render.com

Следуйте инструкции из `DEPLOY_10XFOUNDER.md`, получите URL:
```
https://contacts-comparator.onrender.com
```

### 2. Настройте Cloudflare Worker

В Cloudflare Dashboard создайте Worker с кодом:

```javascript
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const url = new URL(request.url)
  
  // Если путь начинается с /comparator, проксируем на Render
  if (url.pathname.startsWith('/comparator')) {
    const renderUrl = 'https://contacts-comparator.onrender.com' + url.pathname + url.search
    
    const modifiedRequest = new Request(renderUrl, {
      method: request.method,
      headers: request.headers,
      body: request.body
    })
    
    return fetch(modifiedRequest)
  }
  
  // Остальные запросы идут на основной сайт
  return fetch(request)
}
```

### 3. Добавьте Route

В настройках Worker добавьте route:
```
10xfounder.ru/comparator*
```

---

## Тестирование

После настройки проверьте:

```bash
# Основная страница
curl https://10xfounder.ru/comparator

# API health check
curl https://10xfounder.ru/comparator/health

# Должен вернуть: {"status":"ok","timestamp":"..."}
```

---

## Добавление ссылки на основной сайт

На главной странице **10xfounder.ru** добавьте ссылку:

```html
<a href="/comparator" class="service-link">
    🔍 Сравнить базы контактов
</a>
```

Или в меню навигации:

```html
<nav>
    <a href="/">Главная</a>
    <a href="/services">Услуги</a>
    <a href="/comparator">Сравнение контактов</a>
    <a href="/contact">Контакты</a>
</nav>
```

---

## Структура URL

После интеграции:

```
https://10xfounder.ru/                 - Основной сайт
https://10xfounder.ru/comparator       - Сервис сравнения
https://10xfounder.ru/comparator/upload       - API загрузки
https://10xfounder.ru/comparator/download/... - Скачивание результатов
```

---

## Обновление кода

Когда нужно обновить сервис:

```bash
cd /var/www/comparator
sudo git pull origin contacts-comparator-web
sudo systemctl restart comparator
```

---

## Troubleshooting

### Ошибка 404 на /comparator
Проверьте:
1. Nginx конфигурация правильная
2. Сервис запущен: `sudo systemctl status comparator`
3. Proxy pass URL правильный

### Ошибка загрузки файлов
Увеличьте `client_max_body_size` в Nginx:
```nginx
client_max_body_size 50M;
```

### Не работает после обновления
Перезапустите сервис:
```bash
sudo systemctl restart comparator
sudo systemctl reload nginx
```

---

## Мониторинг

Логи сервиса:
```bash
sudo journalctl -u comparator -f
```

Логи Nginx:
```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

---

## 🎉 Готово!

Теперь ваш сервис доступен на:
**https://10xfounder.ru/comparator**

И интегрирован с основным сайтом! 🚀
