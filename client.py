import json
import socket

HOST = '127.0.0.1'
PORT = 58711
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print(f"Connecting to {HOST}:{PORT}")
    s.connect((HOST, PORT))

    while True:
        data_to_send = input("Lets send curl request: \n")

        if data_to_send == '':
            print("Close connection")
            break

        s.send(bytes(data_to_send.strip(), "utf-8"))
        data = s.recv(1024)

        print('Received back:', json.dumps(data.decode("utf-8"), indent=4))
