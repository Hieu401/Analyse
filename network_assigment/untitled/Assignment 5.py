import socket
import select
import json
import itertools

port_host = 8001
ip_server = "145.24.222.103"
client2_ip = "192.168.2.8"
client1_id = 1
client1_ip = socket.gethostbyname(socket.gethostname())


class Client:

    def __init__(self, client_id, message):
        self.client_id = client_id
        self.client_ip = socket.gethostbyname(socket.gethostname())
        self.message = message

    def alter_message(self, new_message):
        self.message = new_message

    def alter_json(self, id_client, ip):
        self.message["studentnr"] = "0964758"
        self.message["classname"] = "INF2C"
        self.message["clientid"] = id_client
        self.message["teamname"] = "TeamUno"
        self.message["ip"] = ip
        self.message["secret"] = None
        self.message["status"] = None
        return self.message

    def send_to(self, socket_target, ip, port):

        def send_to_target():
            # connect to target and receive welcoming message
            socket_target.connect((ip, port))
            print(socket_target.recv(500).decode("utf-8"))

            # send to target
            socket_target.send(bytes(json.dumps(self.message), "utf-8"))
            print("message sent")

            # receive
            response_server = socket_target.recv(1024).decode("utf-8")
            print(response_server)
            socket_target.close()
            return response_server

        return send_to_target


this_client = Client(1, {})

# own server that listens for client1
socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_client.bind((client1_ip, port_host))
socket_client.listen(5)

# all inputs including inputs from server
inputs = [socket_client]

# list of all ip addresses
client_ip_list = []
send_message = bool(int(input("Press 1 if you want to send a message, 0 to accept incoming messages")))

while True:

    if not send_message:
        # unify all inputs and outputs and make the program not wait for input or output
        # why won't it work
        inputs_outputs = select.select(inputs, [], [])
        to_process_list = list(itertools.chain(*inputs_outputs))
        # iterate through all inputs and outputs
        for io in to_process_list:
            # if it is the turn of the server, accept possible connection requests
            if io == socket_client:
                client_socket, client_address = socket_client.accept()
                print("Accepted connection")
                io.send(bytes("Client 2 says: Connection accepted", "utf-8"))
                inputs.append(client_socket)
                client_ip_list.append(client_address)

            # if it is not the turn of the server, then it is a client
            # receive the message (json string format), turn it into a dictionary and change the message
            # then send it to the main server
            else:
                data = io.recv(1024).decode("utf-8")
                print("Message received")
                io.send(bytes("Client 2 says: Message received", "utf-8"))
                json_to_dict = json.loads(data)
                if json_to_dict["status"] == "waiting for message 2":
                    this_client.id = 2
                    json_to_dict["clientid"] = this_client.id
                    json_to_dict["ip"] = socket.gethostbyname(socket.gethostname())
                    this_client.alter_message(json_to_dict)
                    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    response = this_client.send_to(socket_server, ip_server, port_host)()
                    this_client.alter_message(json.loads(response))
                else:
                    inputs.remove(io)
                    io.close()

    # send message code
    else:
        if len(this_client.message) == 0 and send_message:
            this_client.alter_json(client1_id, client1_ip)
            socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            response = this_client.send_to(socket_server, ip_server, port_host)()
            this_client.alter_message(json.loads(response))

            socket_client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            response = this_client.send_to(socket_client2, client2_ip, port_host)()

        elif this_client.message["status"] == "waiting for message 2" and send_message:
            pass

