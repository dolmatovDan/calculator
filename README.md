# Веб-калькулятор с базой данных

Простой веб-калькулятор, построенный на FastAPI, который позволяет выполнять вычисления и сохранять их в базе данных SQLite.

## 🚀 Возможности

- **API для вычислений** - Отправляйте строки для обработки через REST API
- **Сохранение в базе данных** - Все вычисления автоматически сохраняются в SQLite
- **Управление данными** - Возможность просмотра и удаления всех записей
- **Автоматическая документация** - Swagger UI для тестирования API
- **Конфигурация через YAML** - Легкая настройка через файл конфигурации

## 📁 Структура проекта

```
calculator/
├── .gitignore                    # Игнорируемые файлы Git
├── Makefile                      # Команды для сборки и запуска
├── config.yaml                   # Конфигурация приложения
├── README.md                     # Документация проекта
└── backend/
    ├── main.py                   # Основной файл приложения
    ├── requirements.txt          # Зависимости Python
    ├── database/                 # Модули для работы с базой данных
    │   ├── __init__.py
    │   ├── database.py           # Функции работы с БД
    │   └── view_database.py      # Скрипт для просмотра БД
    ├── storage/                  # Хранилище файлов базы данных
    │   └── calculations.db       # SQLite база данных
    └── endpoints/                # API эндпоинты
        ├── __init__.py
        ├── echo.py               # Эндпоинт для обработки строк
        └── delete.py             # Эндпоинт для удаления данных
```

## 🛠 Установка и запуск

### Предварительные требования

- Python 3.8+
- pip или pip3

### Быстрый старт

1. **Клонируйте репозиторий:**
   ```bash
   git clone <repository-url>
   cd calculator
   ```

2. **Создайте виртуальное окружение:**
   ```bash
   make setup
   ```

3. **Активируйте виртуальное окружение:**
   ```bash
   source venv/bin/activate
   ```

4. **Установите зависимости:**
   ```bash
   make install
   ```

5. **Запустите сервер:**
   ```bash
   make run-dev
   ```

Сервер будет доступен по адресу: `http://localhost:8000`

## 📚 API Документация

### Доступные эндпоинты

#### 1. Обработка строк
- **URL:** `POST /echo`
- **Описание:** Принимает строку и сохраняет её в базе данных
- **Тело запроса:**
  ```json
  {
    "text": "Ваша строка для обработки"
  }
  ```
- **Ответ:**
  ```json
  {
    "output": "Ваша строка для обработки",
    "id": 1
  }
  ```

#### 2. Удаление всех записей
- **URL:** `DELETE /delete/all`
- **Описание:** Удаляет все записи из базы данных
- **Ответ:**
  ```json
  {
    "message": "Successfully deleted 5 records from the database",
    "deleted_count": 5
  }
  ```

### Интерактивная документация

После запуска сервера доступна автоматическая документация API:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## 🗄 Работа с базой данных

### Просмотр данных

Используйте встроенный скрипт для просмотра содержимого базы данных:

```bash
python backend/database/view_database.py
```

### Прямое подключение к SQLite

```bash
cd backend/storage
sqlite3 calculations.db
SELECT * FROM echo_strings;
.quit
```

### Структура таблицы

```sql
CREATE TABLE echo_strings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## ⚙️ Конфигурация

Настройки приложения находятся в файле `config.yaml`:

```yaml
server:
  host: "0.0.0.0"    # Хост сервера
  port: 8000         # Порт сервера
  reload: true       # Автоперезагрузка для разработки

app:
  title: "Simple Calculator API"
  description: "A simple FastAPI server"
  version: "1.0.0"
```

## 🔧 Команды Makefile

- `make setup` - Создание виртуального окружения
- `make install` - Установка зависимостей
- `make run` - Запуск сервера (без автоперезагрузки)
- `make run-dev` - Запуск сервера с автоперезагрузкой (рекомендуется)
- `make clean` - Удаление виртуального окружения
- `make help` - Показать все доступные команды

## 🧪 Тестирование API

### Использование curl

```bash
# Отправка строки для обработки
curl -X POST http://localhost:8000/echo \
  -H "Content-Type: application/json" \
  -d '{"text": "Тестовая строка"}'

# Удаление всех записей
curl -X DELETE http://localhost:8000/delete/all
```

### Использование Python requests

```python
import requests

# Отправка данных
response = requests.post(
    "http://localhost:8000/echo",
    json={"text": "Привет из Python!"}
)
print(response.json())

# Удаление всех записей
response = requests.delete("http://localhost:8000/delete/all")
print(response.json())
```

## 📦 Зависимости

- **FastAPI** - Современный веб-фреймворк для создания API
- **Uvicorn** - ASGI сервер для запуска FastAPI
- **PyYAML** - Парсинг YAML конфигурационных файлов
- **SQLite3** - Встроенная база данных (входит в Python)

## 🔮 Планы развития

- [ ] Добавление математических операций
- [ ] Аутентификация пользователей
- [ ] Веб-интерфейс для калькулятора
- [ ] Экспорт данных в различные форматы
- [ ] API для получения истории вычислений
- [ ] Поддержка различных типов вычислений

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции (`git checkout -b feature/AmazingFeature`)
3. Зафиксируйте изменения (`git commit -m 'Add some AmazingFeature'`)
4. Отправьте в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. См. файл `LICENSE` для получения дополнительной информации.

## 📞 Поддержка

Если у вас есть вопросы или предложения, создайте issue в репозитории или свяжитесь с разработчиками.

---

**Примечание:** Этот проект создан в образовательных целях и демонстрирует основы создания REST API с использованием FastAPI и SQLite.