import socket
import select
import json
import itertools

port = 8001
ip_server = "145.24.222.103"
json_file = {}
socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def client1():
    json_file["studentnr"] = "0964758"
    json_file["classname"] = "INF2C"
    json_file["clientid"] = 1
    json_file["teamname"] = "TeamUno"
    json_file["ip"] = '127.0.0.1'
    json_file["secret"] = None
    json_file["status"] = None
    socket_server.connect((ip_server, port))
    print(socket_server.recv(500).decode("utf-8"))
    socket_server.send(bytes(json.dumps(json_file), "utf-8"))
    print("message sent")

    response_server = socket_server.recv(1024).decode("utf-8")
    print(response_server.decode("utf-8"))
    socket_server.close()

    socket_target_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_target_client.connect(("127.0.0.1", port))
    socket_target_client.send(json.dumps(response_server))


def client2():
    # own server that listens for client1
    socket_server.bind(('', port))
    socket_server.listen(5)
    # all inputs including inputs from server
    inputs = [socket_server]
    # list of all ip addresses
    client_ip_list = []
    while True:
        # unify all inputs and outputs and make the program not wait for input or output
        inputs_outputs = select.select(inputs, [], [])
        to_process_list = list(itertools.chain(*inputs_outputs))
        # iterate through all inputs and outputs
        for io in to_process_list:
            # if it is the turn of the server, accept possible connection requests
            if io == socket_server:
                client_socket, client_address = socket_server.accept()
                inputs.append(client_socket)
                client_ip_list.append(client_address)
            # if it is not the turn of the server, then it is a client
            # receive the message (json string format), turn it into a dictionary and change the message
            # then send it to the main server
            else:
                data = socket_server.recv(1024)
                json_to_dict = json.loads(data)["secret"]
                if json_to_dict is not None:
                    json_to_dict["clientid"] = 2
                    json_to_dict["ip"] = client_ip_list[0]
                    socket_server.connect((ip_server, port))
                    socket_server.recv(500)
                    socket_server.send(bytes(json.dumps(json_to_dict), encoding='utf-8'))
                    print(socket_server.recv(1024))
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
