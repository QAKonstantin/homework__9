# Краткое описание работы скрипта

1. В файле server.py функция '**parse_request_line**' формирует корректный ответ из запроса клиента в формате словаря.
2. В файле server.py функция '**parse_url**' анализирует отправленный клиентом статус:
- если в запросе **/?status=404** - ответ будет с кодом 404 Not Found
- на все остальные статусы (валидные/невалидные) - ответ с кодом 200 OK
## Пример использования
```sh
1. Запустить server.py
2. Подставить в client.py порт, который прослушивает сервер
3. Запустить client.py
4. Ввести curl запрос вида:
- curl GET 127.0.0.1:21312
- curl GET 127.0.0.1:21312 -H "Host: 127.0.0.1, Header_name: header_value"
- curl -X GET 127.0.0.1:21312/?status=200 -H "Host: 127.0.0.1"
- curl --http1.1 -X GET 127.0.0.1:21312/?status=404 -H "Host: 127.0.0.1"
- curl --http1.1 -X GET 127.0.0.1:21312/qweqwrq -H "Host: 127.0.0.1"
- curl GET 127.0.0.1:21312/?status=fwefweg -H "Host: 127.0.0.1, Header_name: header_value"
5. Получен ответ в формате строки со следующей структурой:
Request Method: GET/POST/DELETE/HEAD/PUT
Request Source: (HOST, PORT)
Response Status: STATUS_CODE
header-name: header-value
header-name: header-value
6. Можно повторно отправить другой curl запрос, либо закрыть соединение, написав 'close' в инпут
```

