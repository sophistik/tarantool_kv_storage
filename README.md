# tarantool_kv_storage
Тестовое задание для собеседования в команду Tarantool
#

## Задание:

1) скачать/собрать тарантул
2) запустить тестовое приложение
3) реализовать kv-хранилище доступное по http
4) выложить на гитхаб
5)* задеплоить где-нибудь в публичном облаке

API:
 - POST /kv body: {key: "test", "value": {SOME ARBITRARY JSON}} 
 - PUT kv/{id} body: {"value": {SOME ARBITRARY JSON}}
 - GET kv/{id} 
 - DELETE kv/{id}

 - POST  возвращает 409 если ключ уже существует, 
 - POST, PUT возвращают 400 если боди некорректное
 - PUT, GET, DELETE возвращает 404 если такого ключа нет
 - все операции логируются
#

## Установка приложения

Tarantool
```bash
$ tarantool
tarantool> box.cfg{listen = 3301}
tarantool> s = box.schema.space.create('KVStorage')
tarantool> s:format({  {name = 'key', type = 'string'}, {name = 'value', type = 'string'}  })
tarantool> s:create_index('primary', { type = 'hash', parts = {'key'}   })
tarantool> box.schema.user.grant('guest', 'read,write', 'universe')
```

Django app:

```bash
$ git clone https://github.com/sophistik/tarantool_kv_storage.git
$ cd tarantool_kv_storage/
$ python3 -mvenv venv
$ . venv/bin/activate
$ pip3 install -r requirements.txt
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py runserver
```
