# 🔍 Contacts Comparator Web

Веб-сервис для сравнения баз контактов и поиска дубликатов между двумя файлами Excel или CSV.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Особенности

- ✅ **Простой веб-интерфейс** - загружайте файлы через браузер
- ✅ **Множественные форматы** - поддержка CSV, XLSX, XLS
- ✅ **Умный поиск** - находит дубликаты по email, телефону, имени
- ✅ **Нормализация данных** - автоматически приводит телефоны и email к единому формату
- ✅ **Мгновенные результаты** - получайте статистику и скачивайте отчеты
- ✅ **Безопасность** - автоматическое удаление старых файлов

## 🚀 Быстрый старт

### Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/YOUR_USERNAME/contacts-comparator-web.git
cd contacts-comparator-web
```

2. Создайте виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

### Запуск

Запустите сервер разработки:
```bash
python app.py
```

Откройте браузер и перейдите по адресу:
```
http://localhost:5000
```

## 📖 Использование

### Шаг 1: Загрузите файлы
- Нажмите на область "Файл 1" и выберите первый файл с контактами
- Нажмите на область "Файл 2" и выберите второй файл с контактами

### Шаг 2: Выберите критерий поиска
- **Все** - ищет по email, телефону и имени (рекомендуется)
- **Только Email** - самый надежный метод
- **Только Телефон** - с нормализацией формата
- **Только Имя** - поиск по ФИО

### Шаг 3: Получите результаты
- Нажмите "Сравнить файлы"
- Дождитесь обработки (обычно несколько секунд)
- Просмотрите статистику и примеры дубликатов
- Скачайте Excel файлы с результатами

## 📊 Что вы получите

### В интерфейсе:
- **Статистика**: количество контактов в каждом файле, дубликатов, уникальных записей
- **Примеры дубликатов**: первые 10 найденных совпадений
- **Кнопки скачивания**: для каждого типа результатов

### Файлы для скачивания:
1. **Сводный отчет** - все результаты в одном файле (несколько вкладок)
2. **Дубликаты** - только найденные совпадения
3. **Уникальные из файла 1** - контакты только в первом файле
4. **Уникальные из файла 2** - контакты только во втором файле

## 🏗️ Архитектура

```
contacts-comparator-web/
├── app.py                 # Flask приложение
├── templates/
│   └── index.html        # Веб-интерфейс
├── requirements.txt      # Зависимости
├── .gitignore           # Игнорируемые файлы
├── README.md            # Документация
├── uploads/             # Загруженные файлы (создается автоматически)
└── results/             # Результаты сравнения (создается автоматически)
```

## 🔧 API Endpoints

### `POST /upload`
Загружает и сравнивает два файла.

**Параметры:**
- `file1` - первый файл (multipart/form-data)
- `file2` - второй файл (multipart/form-data)
- `match_by` - критерий поиска: `all`, `email`, `phone`, `name`

**Ответ:**
```json
{
  "session_id": "uuid",
  "file1_name": "contacts1.csv",
  "file2_name": "contacts2.xlsx",
  "file1_count": 1000,
  "file2_count": 800,
  "duplicates_count": 150,
  "unique_file1_count": 850,
  "unique_file2_count": 650,
  "match_types": {
    "Email": 120,
    "Телефон": 20,
    "Имя": 10
  },
  "duplicates_sample": [...],
  "summary_file": "comparison_summary_20240101_120000.xlsx"
}
```

### `GET /download/<session_id>/<filename>`
Скачивает файл с результатами.

### `GET /health`
Проверка работоспособности сервиса.

## 🔐 Безопасность

- Максимальный размер файла: 16 MB
- Поддерживаемые форматы: только CSV, XLSX, XLS
- Автоматическое удаление файлов старше 24 часов
- Уникальные сессии для каждого пользователя
- Безопасные имена файлов (secure_filename)

## 🚢 Деплой

### Heroku

1. Создайте `Procfile`:
```
web: gunicorn app:app
```

2. Деплой:
```bash
heroku create your-app-name
git push heroku main
```

### Docker

1. Создайте `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
```

2. Соберите и запустите:
```bash
docker build -t contacts-comparator .
docker run -p 5000:5000 contacts-comparator
```

### VPS (Ubuntu/Debian)

1. Установите зависимости:
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx
```

2. Настройте Nginx:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

3. Запустите с Gunicorn:
```bash
gunicorn -w 4 -b 127.0.0.1:5000 app:app
```

## ⚙️ Настройка

В файле `app.py` можно изменить:

```python
# Секретный ключ (обязательно измените в продакшене!)
app.secret_key = 'your-secret-key-change-in-production'

# Максимальный размер файла
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# Время хранения файлов
cleanup_old_files(folder, max_age_hours=24)
```

## 🐛 Troubleshooting

### Ошибка "Файл слишком большой"
Увеличьте `MAX_FILE_SIZE` в `app.py`

### Ошибка загрузки файла
Проверьте формат файла (должен быть CSV, XLSX или XLS)

### Не находит дубликаты
Попробуйте разные критерии поиска или проверьте данные в файлах

## 📝 Требования к файлам

Файлы должны содержать хотя бы одну из колонок:
- **Имя**: "Имя", "Name", "ФИО", "Full Name"
- **Email**: "Email", "E-mail", "Почта"
- **Телефон**: "Телефон", "Phone", "Тел", "Mobile"

## 🤝 Вклад

Приветствуются Pull Request'ы! Для больших изменений сначала создайте Issue.

## 📄 Лицензия

MIT License - см. файл LICENSE

## 👨‍💻 Автор

Ваше имя - [@your_github](https://github.com/your_username)

## 🙏 Благодарности

- Flask за отличный фреймворк
- Pandas за мощную обработку данных
- Все контрибьюторы проекта

---

**Упростите работу с базами контактов уже сегодня! 🚀**
