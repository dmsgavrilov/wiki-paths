# wiki-paths

Приложение для поиска кратчайшего пути между статьями в Википедии


### Схема работы

Есть веб-сервис с двумя путями: ```/``` и ```/tasks```. 
По первому пути можно сделать запрос на поиск, по второму - посмотреть результат выполнения.
При выполнении запроса он кладется в очередь. Из очереди его извлекает воркер и сохраняет его в ```storage```


### Запуск приложения

Запускаем redis в docker: \
```docker run --name redis-server -d redis -p 127.0.0.1:6379:6379```

Затем запускаем сервер и воркера: \
```pip3 install -r requirements.txt``` \
```python3 web_app.py``` \
```python3 worker.py```


### Реализованные пункты задачи
1, 2 пункты готовы полностью 3 не полностью
