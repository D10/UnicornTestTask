# Тестовое задание для Unicorn

*С ТЗ можно ознакомиться в одноименном файле "ТЗ.txt"*

Развернуть микросервис можно докером. Как пример:

```
docker build --build-arg PERIOD=1 --build-arg EUR=100 --build-arg DEBUG=y --build-arg USD=150 --build-arg RUB=1000 . -f dockerfile -t test-service
docker run -p 8080:8080 test-service
```

### Из дополнительного:
1. Прикрутил выше указанный докер
2. Покрыл эндпоинты небольшими тестами
3. Добавил кастомных исключений и миддлварку для их обработки


### Примечания:
1. Такой странный способ извлечения json'а из ответа в от ЦБ РФ оправдан тем, что методом "await response.json()"
не работает из-за другого content-type в ответе
2. В качестве хранения данных воспользовался csv, т.к поднимать БД для тестового проекта не посчитал нужным, да и данных маловато. Но если что,
могу переписать и под PostgreSQL + asyncpg
