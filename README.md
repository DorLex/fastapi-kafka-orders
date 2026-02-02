## Приложение для асинхронной обработки заказов.

### Описание:

- `App` - REST-API для работы пользователей, регистрации, авторизации; взаимодействие с заказами; админ-панель.
- `Order Worker` - сервис-обработчик заказов, связан с `App` через `Kafka`.

### Стек:

- `FastAPI`
- `AioKafka`
- `Sqlalchemy`, `Alembic`
- `PostgreSQL`
- `Apache Kafka`
- `SqlAdmin`
- `Pytest`
- `Docker`

### Установка зависимостей:

1. Создать окружение через `uv`.
   TODO: дописать подробнее...

2. Установить только основные зависимости, необходимые для запуска:
   ```shell
   uv sync --no-group dev --no-group test
   ```

3. Установить все зависимости, включая `dev`/`test` (+linter, +pre-commit и т.д.):
    ```shell
    uv sync --all-groups
    ```

### Pre-commit, Linter, Formatter:

- Установить `pre-commit` хуки:
    ```shell
    pre-commit install
    ```

- Ручной запуск линтера и форматера:
    ```shell
    ruff check && ruff format
    ```

### Запуск:

1. Создать файл `./docker/.env` по примеру `./docker/example.env`.

2. Основные команды запуска в `Makefile`:
    ```shell
    make up
    ```
3. URL's:
    - `Swagger`: `/docs`
    - `Админ-панель`: `/admin`

### Примечания:

1. `Alembic` был сконфигурирован для коннекшена через `asyncpg` следующим образом:
    ```shell
    alembic init -t async src/app/infrastructure/migrations
    ```
