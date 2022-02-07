import socket
import random
from http import HTTPStatus

HOST = "127.0.0.1"
PORT = random.randint(10000, 20000)
resp = []
dict_resp = {'Request Method': '', 'Request Source': '', 'Response Status': ''}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print(f"Binding server on {HOST}:{PORT}")
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()

    with conn:
        while True:

            def parse_request_line(data, dict_resp):
                if data.split(' ')[0] != 'curl':
                    words = data.split('\r\n')
                    i = words[0].split(' ')
                    for k in range(len(i)):
                        if i[k] not in ['GET', 'POST', 'DELETE', 'PUT', 'HEAD']:
                            words.remove(i[k])
                        else:
                            break
                    dict_resp['Request Method'] = i[k]
                    dict_resp['Response Status'] = parse_url(words[1])
                    dict_resp['Request Source'] = addr
                    for i in range(2, len(words) - 2):
                        dict_resp[f'{words[i].split(": ")[0]}'] = words[i].split(": ")[1]
                    return dict_resp
                elif data.split(' ')[0] == 'curl':
                    words = data.split()
                    i = words[0]
                    while i not in ['GET', 'POST', 'DELETE', 'PUT', 'HEAD']:
                        words.remove(i)
                        i = words[0]
                    dict_resp['Request Method'] = words[0]
                    dict_resp['Response Status'] = parse_url(words[1])
                    dict_resp['Request Source'] = addr
                    for i in range(0, len(words) - 3, 2):
                        dict_resp[f'{words[i + 3].replace(":", "")}'] = words[i + 4]
                    return dict_resp


            def parse_url(url):
                if (len(url.split('=')) > 1 and url.split('=')[1] == '404'):
                    url = HTTPStatus.NOT_FOUND.value
                    return f'{url} ' + HTTPStatus.NOT_FOUND.phrase
                else:
                    url = HTTPStatus.OK.value
                    return f'{url} ' + HTTPStatus.OK.phrase


            data = conn.recv(1024)
            print("Received", data, "from", addr)
            if not data or data == b"close":
                print("Got termination signal", data, "and closed connection")
                conn.close()
                break
            data = data.decode("utf-8")
            resp = parse_request_line(data, dict_resp)
            str = ''
            for key, value in resp.items():
                str += key + f':{value}\n'
            conn.send(str.encode("utf-8"))
            print(f'sent response:\n{str}')
