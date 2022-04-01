import socket
from http import HTTPStatus
from helper import get_open_port

address = ('127.0.0.1', get_open_port())
dict_resp = {'Request Method': '', 'Request Source': '', 'Response Status': ''}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print(f"Binding server on {address}")
    s.bind(address)
    s.listen(1)

    while True:
        conn, addr = s.accept()


        def parse_headers(data, status_line, dict_resp):
            try:
                headers = data[1:]
                dict_resp['Request Method'] = data[0].split(' ')[0]
                dict_resp['Response Status'] = status_line.split(' ')[1] + ' ' + status_line.split(' ')[2]
                dict_resp['Request Source'] = addr
                for i in range(len(headers) - 2):
                    dict_resp[f'{headers[i].split(": ")[0]}'] = headers[i].split(": ")[1]
                return dict_resp
            except:
                print("Incorrect url")
                return None


        def parse_resp_status(status_line):
            try:
                status_code = int(status_line[1].split('=')[1])
                return f'{HTTPStatus(status_code).value} {HTTPStatus(status_code).name}'
            except (ValueError, IndexError):
                return f'{HTTPStatus.OK.value} {HTTPStatus.OK.name}'


        def parse_status_line(status_line):
            if len(status_line) == 3:
                temp = status_line[2] + ' ' + parse_resp_status(status_line)
                return temp
            else:
                return None


        while True:
            data = conn.recv(1024)
            text = data.decode("utf-8")
            if text:
                print("Received", text, "\nfrom", addr)
                status_line = parse_status_line(text.split('\r\n')[0].split(' '))
                if status_line is not None:
                    headers = parse_headers(text.split('\r\n'), status_line, dict_resp)
                    body = text.split('\r\n\r\n')[1]
                    status_line += '\n'
                    for key, value in headers.items():
                        status_line += key + f':{value}\n'
                    if body != '':
                        status_line += '\n' + body
                    conn.send(status_line.encode("utf-8"))
                    print(f'Response:\n{status_line}')
                    break
                else:
                    conn.send(f'Incorrect request: {text}'.encode("utf-8"))
                    print(f'Incorrect request:\n{text}')
            else:
                print(f'no data from {addr}')
                break
        conn.close()
