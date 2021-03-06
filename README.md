# Решение задач на код
## 1. Установка и запуск приложения с помощью Docker Compose
Скопируйте проект и перейдите в рабочую директорию JBTest:
```
git clone https://github.com/DemXR/JBTest.git
cd JBTest
```

Перед запуском контейнеров убедитесь, что у Вас свободны порты
:80 для nginx; 
:8000 для django; 
:5672 для rabbitmq.

Запустите контейнеры командой:
```
docker-compose up
```

## 2. Документация по API
### 2.1 Запрос перечня упражнений
```
GET /api/exercise/
```
Пример ответа:
```
[
    {
        "id": 1,
        "title": "Упражнение №1",
        "body": "Посчитать сумму двух целых чисел.",
        "created_at": "2021-03-01T15:43:37.006000+03:00",
        "review": {}
    },
    ...
]
```
### 2.2 Отправка ответа на проверку
```
POST /api/exercise/<Идентификатор упражнения>/review/
```
Пример запроса:
```
{
    "reply": "print('Hello, world!')"
}
```
Пример ответа:
```
{
    "id": 4,
    "reply": {
        "reply_text": "print('Hello, world!')",
        "status": {
            "slug": "evaluation",
            "name": "На проверке"
        }
    }
}
```
### 2.3 Запрос перечня всех ответов по упражнению
```
GET /api/exercise/<Идентификатор упражнения>/review/
```
Пример ответа:
```
[
    {
        "id": 1,
        "reply": {
            "reply_text": "Hello, world",
            "status": {
                "slug": "wrong",
                "name": "Неверно"
            }
        }
    },
    ...
]
```
### 2.4 Запрос сведений о проверке 
```
GET /api/exercise/<Идентификатор упражнения>/review/<Идентификатор проверки>/
```
Пример ответа:
```
{
    "id": 4,
    "reply": {
        "reply_text": "print('Hello, world!')",
        "status": {
            "slug": "wrong",
            "name": "Неверный"
        }
    }
}
```

## 3. Работа с приложением
Приложение доступно по адресу: http://localhost/
<br />В тестовом примере предложено 6 упражнений. Выполнять упражнения можно в любой последовательности.
Результатом проверки упражнения является иконка справа от заголовка упражнения (галочка для 'correct' и крестик для 'wrong').
После обновления страницы данные не будут потеряны (данные привязаны к session_key).

## 4. Панель администратора
Панель доступна по адресу: http://localhost/admin/
<br />Для демонстрации заранее был создан пользователь:
```
login: admin
password: admin
```
**Важно!** *После авторизации сменится Ваша сессия (session_key), и вы перестаните видеть ранее введенные ответы в упражнениях. Чтобы решить эту проблему необходимо реализовать кастомную авторизацию, которая позволит связать данные сессий анонимных и авторизованных пользователей.*

Список решений доступен для просмотра в модели *Exercise reviews*.
Список упражнения доступен для редактирования в модели *Exercises*.

## 5. Особенности
Т.к. большинство отправленных решений от разных пользователей ожидается одинаковым, то целесообразно кэшировать результаты ответов. Для этого текст каждого решения кэшируется в отдельной сущности *ExerciseReply*. Если пользователь отправит на проверку текст который уже кто-то отправлял, то его решение примет соотетствующий статус из кэша. Это существенно снижает нагрузку на сторонний сервис и повышает скорость получения ответа.

Когда проверка решения задерживается в статусе 'evaluation', то фронтенд периодически запрашивает новый статус из кэша бэкэнда. Периодичность настраивается в файле: /frontend/src/store/index.js
```
state.exercises.checkReviewInterval: 3 // по умолчанию каждые 3 сек
```
Если в кэше бэкэнда есть решения в статусе 'evaluation', то бэкэнд периодически запрашивает новый статус для таких решений у стороннего сервиса.
Периодичность настраивается в файле: /backend/education/celery.py
```
app.conf.beat_schedule = {
    'check-review-results': {
        'task': 'exercises.tasks.check_review_status',
        'schedule': 3.0 # по умолчанию каждые 3 сек
    }
}
```
Это позволяет фронтенду не "задедосить" бэкэнд запросами на изменение статуса.

Так же дополнительно можно защитить бэкэнд от ddos на уровне nginx, например с помощью модуля [ngx_http_limit_req_module](https://nginx.org/ru/docs/http/ngx_http_limit_req_module.html).