# Coursework 7

## Kickstart

```bash
git clone https://github.com/IldarGaleevSkyProHomeworks/coursework_7.git
cd coursework_7
poetry install
cp .env.template .env
code .env
```
```bash
poetry shell
python manage.py migrate
```

## Переменные окружения

Шаблон файла `.env` - [.env.template](./.env.template)

| Переменная                        | Описание                                                                                             |
|-----------------------------------|------------------------------------------------------------------------------------------------------|
| `DEBUG`                           | Включить отладку                                                                                     |
| `ALLOWED_HOSTS`                   |                                                                                                      |
| `CORS_ALLOWED_ORIGINS`            |                                                                                                      |
| `CSRF_TRUSTED_ORIGINS`            |                                                                                                      |
| `APPLICATION_SCHEME`              | Схема приложения (`http`/`https`) (так же влияет на `CORS_ALLOWED_ORIGINS` и `CSRF_TRUSTED_ORIGINS`) |
| `APPLICATION_HOSTNAME`            | Hostname приложения (так же влияет на `ALLOWED_HOSTS`,`CORS_ALLOWED_ORIGINS`,`CSRF_TRUSTED_ORIGINS`) |
| `TELEGRAM_USE_POLL`               | Использовать long-poll для получения сообщений от Telegram (рекомендуется только для отладки)        |
| `TELEGRAM_BOT_TOKEN`              | Токен Telegram бота                                                                                  |
| `TELEGRAM_POLL_INTERVAL`          | Таймаут (сек.) long-poll для Telegram                                                                |
| `CELERY_TASK_TRACK_STARTED`       |                                                                                                      |
| `CELERY_TASK_TIME_LIMIT`          |                                                                                                      |
| `CELERY_BROKER_URL`               | Строка подключения к брокеру сообщений                                                               |
| `CELERY_RESULT_BACKEND`           | Строка подключения к брокеру сообщений                                                               |
| `MAX_OAUTH_TIMEOUT`               | Время жизни токена OAuth                                                                             |
| `DB_ENGINE`                       | Провайдер базы данных                                                                                |
| `DB_NAME`                         |                                                                                                      |
| `DB_USER`                         |                                                                                                      |
| `DB_PASSWORD`                     |                                                                                                      |
| `DB_HOST`                         |                                                                                                      |
| `DB_PORT`                         |                                                                                                      |

## Команды Django

### `telegramwebhookinit`

Регистрирует веб-хук для получения сообщений от Telegram.

#### Флаги и аргументы

| Аргумент         | Описание                           |
|------------------|------------------------------------|
| `-d`, `--delete` | Флаг - удаляет веб-хук если указан |

> [!NOTE]
> Перед запуском команды необходимо задать переменные окружения:
> - `TELEGRAM_USE_POLL` = `False`
> - `TELEGRAM_BOT_TOKEN`
> - `APPLICATION_SCHEME`
> - `APPLICATION_HOSTNAME`

### `telegrampoll`

Запускает задачу для получения сообщений от Telegram (только для режима long-poll)

### `grantrights`

Настройка прав пользователей

#### Флаги и аргументы

| Аргумент           | Описание                                                                   |
|--------------------|----------------------------------------------------------------------------|
| `-u`,`--superuser` | Флаг - выдает права суперпользователя                                      |
| `-s`, `--staff`    | Флаг -выдает права персонала                                               |
| `--username`       | Аргумент для поиска учетной записи по логину                               |
| `--telegramid`     | Аргумент для поиска учетной записи по идентификатору пользователя Telegram |

## Настройка Telegram бота

> [!NOTE]
> Для корректной работы webhook и авторизации при помощи Telegram
> необходимо указать публичный адрес или воспользоваться прокси сервером,
> например `ngrok`

1. При помощи [BotFather](https://t.me/BotFather) создайте и настройте бота.
2. Получите токен и пропишите его в переменную окружения `TELEGRAM_BOT_TOKEN`
3. Далее (необязательно, нужно только для функционирования виджета "Войти через Telegram") идем в настройки: Bot
   Settings > Domain > Edit Domain и прописываем наш публичный адрес (такой же как в `APPLICATION_HOSTNAME`. Получаем
   его например в `ngrok`)

## Запуск бота

1. Прописать токен, схему и hostname приложения.
2. Запустить Django приложение (для обработки webhook запросов и аутентификации через виджет Telegram)
3. Настроить и запустить брокер сообщений (`Redis`). Запустить обработчик фоновых задач для отправки сообщений:
   ```powershell
   celery -A config worker -l INFO -P eventlet
   ```
4. Командой `telegrampoll` запустить поллинг сообщений от Telegram (если используется longpoll-mode)

## Команды Telegram бота

| Команда   | Описание                                                 |
|-----------|----------------------------------------------------------|
| `start`   | Начало работы с ботом                                    |
| `link`    | Привязать аккаунт Telegram к существующей учетной записи |
| `genpass` | Сгенерировать пароль для привязанной учетной записи      |
| `getjwt`  | Получить JWT токен для доступа к API                     |
| `cancel`  | Остановить выполнение команды                            |

## Создание учетной записи администратора

1. Используя стандартную команду `createsuperuser`
    1. Далее используя команду `/link` в Telegram связать аккаунты, указав логин и пароль
2. На странице `/accounts/login/` нажать кнопку "Войти через Telegram" создастся новый аккаунт и сразу свяжется с
   учетной записью в Telegram, в чат придет сообщение с логином и паролем
    1. Теперь, используя логин или id аккаунта Telegram, можно выдать права суперпользователя при помощи
       команды `grantrights` в терминале:
       ```powershell
       python .\manage.py grantrights -u --username yourUsername 
       ```

## Создание уведомлений

По пути `/api/habits` создать `POST` запросом привычку

По пути `/api/habits/{id}/start/` отправить `POST` запрос с json, 
содержащим информацию о часовом поясе вида `Europe/Moscow` в поле `timezone`, чтобы подписаться на уведомления. При успешной подписке придет уведомление.

По пути `/api/habits/{id}/start/` отправить `DELETE` запрос, 
чтобы отписаться от уведомлений. При успешной отписке придет уведомление.

## Запуск приложения:

Менеджер задач:
```powershell
celery -A config worker -l INFO -P eventlet
```

Планировщик:
```powershell
celery -A config beat -l INFO -S django
```

Django сервер
```powershell
python .\manage.py runserver
```

## Docker

Мнимимальная настройка для успешного развертывания контейнеров:
1. Создайте файл `.env.docker` с указанными переменными ([шаблон файла](.env.docker.template)):
   - `TELEGRAM_BOT_TOKEN` - токен для Telegram бота
   - `APPLICATION_HOSTNAME` - внешний адрес приложения. Используется для задания `ALLOWED_HOSTS`,`CORS_ALLOWED_ORIGINS`,`CSRF_TRUSTED_ORIGINS`
   - `APPLICATION_SCHEME` (не обязательно) - по умолчанию `https`, при локальном запуске обычно не требуется.
   - `TELEGRAM_USE_POLL` - Влияет на автоматическую регистрацию вебхука для Telegram бота
2. В сервисе `web`
   - Создайте [учетную запись администратора](#создание-учетной-записи-администратора)
   - Настройте [Telegram бота](#настройка-telegram-бота)

Приложение имеет два профиля:
1. long-poll
   ```bash
   docker compose --profile tg_poll up
   ```
   этот профиль так же запускает дополнительный сервис для получения сообщений от Telegram API


2. webhook (по умолчанию - не требует указания профиля)
   ```bash
   docker compose up
   ```
   в этой конфигурации для получения сообщений от Telegram API используется webhook