import socket
import select
import json
import itertools

port = 8001
ip_server = "145.24.222.103"
json_file = '{"studentnr": "0964758", "classname": "INF2C", "clientid": 1, "teamname": "TeamUno", "ip": "84.80.42.132", "secret": None, "status": None}'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def client1():
    s.connect((ip_server, port))
    print(s.recv(500))
    s.send(bytes(json_file, encoding='utf8'))
    print("message sent")
    print(s.recv(1024))
    # new_json_file = (s.recv(500)
    s.close()
    s.connect(("127.0.0.1", port))
    # s.send(new_json_file)


def client2():
    # own server that listens for client1
    s.bind(('', port))
    s.listen(5)
    # all inputs including inputs from server
    inputs = [s]
    # list of all ip addresses
    client_ip_list = []
    while True:
        # unify all inputs and outputs and make the program not wait for input or output
        inputs_outputs = select.select(inputs, [], [])
        to_process_list = list(itertools.chain(*inputs_outputs))
        # iterate through all inputs and outputs
        for io in to_process_list:
            # if it is the turn of the server, accept possible connection requests
            if io == s:
                client_socket, client_address = s.accept()
                inputs.append(client_socket)
                client_ip_list.append(client_address)
            # if it is not the turn of the server, then it is a client
            # receive the message (json string format), turn it into a dictionary and change the message
            # then send it to the main server
            else:
                data = s.recv(1024)
                json_to_dict = json.loads(data)["secret"]
                if json_to_dict is not None:
                    json_to_dict["clientid"] = 2
                    json_to_dict["ip"] = client_ip_list[0]
                    s.connect((ip_server, port))
                    s.recv(500)
                    s.send(bytes(json.dumps(json_to_dict), encoding='utf-8'))
                    print(s.recv(1024))
                else:
                    inputs.remove(io)
                    io.close()


client = input("This program needs 2 computers, but runs the same programs. Select client 1 or client2.")
if client == "1":
    client1()
elif client == "2":
    client2()
else:
    print("Invalid input, please rerun the program and try again.")
