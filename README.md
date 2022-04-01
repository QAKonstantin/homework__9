# Краткое описание работы скрипта

1. В файле server.py функция '**parse_headers**' формирует хедеры из запроса клиента в формате словаря
2. В файле server.py функция '**parse_resp_status**' анализирует отправленный клиентом статус. На невалидный статус
   ответ с кодом 200 OK
3. В файле server.py функция '**parse_status_line**' парсит первую строку для ответа

## Пример использования

```sh
1. Запустить server.py
2. Подставить в client.py порт, на котором слушает сервер
3. Запустить client.py
4. Отправить http запрос
5. Получен ответ в формате строки со следующей структурой:
Protocol/Version STATUS_CODE
Request Method: Method
Request Source: (HOST, PORT)
Response Status: STATUS_CODE
header-name: header-value
header-name: header-value

body (если есть)
6. Соединение не закрывается после отправки ответа, и можно повторно отправить http запрос
```

