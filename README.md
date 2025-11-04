# Monitoring Battery

**Monitoring Battery** — это REST API для мониторинга батарей и устройств с функционалом регистрации пользователей, аутентификации, управления батареями и устройствами.

API полностью соответствует спецификации OpenAPI 3.1.0 и поддерживает JWT аутентификацию.

## Основные возможности

### Auth

- `POST /api/v1/auth/register` — регистрация нового пользователя
    
- `POST /api/v1/auth/login` — вход с генерацией access и refresh токенов
    
- `POST /api/v1/auth/refresh` — обновление токена
    
- `GET /api/v1/auth/me` — информация о текущем пользователе
    

### Battery

- `GET /api/v1/battery` — список батарей (пагинация через offset и limit)
    
- `POST /api/v1/battery` — создание батареи
    
- `GET /api/v1/battery/{id}` — получение конкретной батареи
    
- `PUT /api/v1/battery/{battery_id}` — обновление батареи
    
- `DELETE /api/v1/battery/{battery_id}` — удаление батареи
    

### Devices

- `GET /api/v1/categories` — список устройств (пагинация через offset и limit)
    
- `POST /api/v1/categories` — создание устройства
    
- `GET /api/v1/categories/{slug}/posts` — получение конкретного устройства
    
- `PUT /api/v1/categories/{category_id}` — обновление устройства
    
- `DELETE /api/v1/categories/{category_id}` — удаление устройства

- `POST /api/v1/devices/{device_id}/battaries` — добавление батарей к устройству

- `DELETE /api/v1/devices/{device_id}/battaries/{battery_id}` — удаление батареи из устройства
    

### Users

- `GET /api/v1/users` — список пользователей
    
- `PUT /api/v1/users/{user_id}/role` — установка роли пользователя (`USER` или `ADMIN`)
    
## Запуск через Docker Compose

1. Создать файл `.env` в папке "back/app/" или взять тестотвый из папки "env_file":
    
    ```bash
    cp env_file/.env.example back/app/.env
    ```

    #### Параметры окружения env

    | Переменная                    | Описание                                           | Пример                             |
    | ----------------------------- | -------------------------------------------------- | ---------------------------------- |
    | `PROJECT_NAME`                | Название проекта                                   | `Backend Blog`                     |
    | `DEBUG`                       | Режим отладки (`True`/`False`)                     | `False`                            |
    | `DATABASE_URL`                | URL подключения к базе данных SQLite               | `sqlite+aiosqlite:///./db.sqlite3` |
    | `POSTGRES_USER`               | Пользователь PostgreSQL (если используется Docker) | `postgres`                         |
    | `POSTGRES_PASSWORD`           | Пароль пользователя PostgreSQL                     | `postgres`                         |
    | `POSTGRES_HOST`               | Хост базы данных PostgreSQL                        | `db`                               |
    | `POSTGRES_PORT`               | Порт базы данных PostgreSQL                        | `5432`                             |
    | `POSTGRES_DB`                 | Имя базы данных PostgreSQL                         | `postgres`                         |
    | `JWT_SECRET_KEY`              | Секретный ключ для генерации JWT токенов           | `your_secret_key`                  |
    | `JWT_ALGORITHM`               | Алгоритм для JWT                                   | `HS256`                            |
    | `ACCESS_TOKEN_EXPIRE_MINUTES` | Время жизни access токена (минуты)                 | `30`                               |
    | `REFRESH_TOKEN_EXPIRE_DAYS`   | Время жизни refresh токена (дни)                   | `7`                                |
    | `PREFERRED_HASH`              | Алгоритм хеширования паролей                       | `argon2`                           |


2. Запустить команду docker-compose 

    ```bash
    docker-compose up --build
    ```

#### После сборки сервисов API будет доступен по адресу:
- API будет доступен по адресу: `http://127.0.0.1:8000`  
- Swagger документация: `http://127.0.0.1:8000/docs`
- Redoc документация: `http://127.0.0.1:8000/redoc`
- UI доступен по адресу: `http://127.0.0.1:3000`

#### Тестовый пользователь:
- Email: `admin@admin.com`
- password: `1`

