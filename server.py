import socket
import random
import logging
from http import HTTPStatus

logging.basicConfig(level=logging.DEBUG)

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
            data = data.decode("utf-8")
            resp = parse_request_line(data, dict_resp)
            str = ''
            for key, value in resp.items():
                str += key + f':{value}\n'
            conn.send(str.encode("utf-8"))
            logging.info(f"Sent '{data}' to {addr}")
