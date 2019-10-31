import socket
import json

port_host = 8001
ip_server = "145.24.222.103"
client2_ip = None
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

send_message = bool(int(input("Press 1 if you want to send a message, 0 to accept incoming messages")))

while True:

    if not send_message:
        client_socket, client_address = socket_client.accept()
        print("Accepted connection")
        client_socket.send(bytes("Client 2 says: Connection accepted", "utf-8"))

        # code doesn't run after this
        data = client_socket.recv(1024).decode("utf-8")
        print("Message received")
        client_socket.send(bytes("Client 2 says: Message received", "utf-8"))
        json_to_dict = json.loads(data)
        if json_to_dict["status"] == "waiting for message 2":
            this_client.id = 2
            json_to_dict["clientid"] = this_client.id
            json_to_dict["ip"] = socket.gethostbyname(socket.gethostname())
            this_client.alter_message(json_to_dict)
            socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            response = this_client.send_to(socket_server, ip_server, port_host)()
            this_client.alter_message(json.loads(response))

    # send message code
    else:
        if len(this_client.message) == 0 and send_message:
            this_client.alter_json(client1_id, client1_ip)
            socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            response = this_client.send_to(socket_server, ip_server, port_host)()
            this_client.alter_message(json.loads(response))

            socket_client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            response = this_client.send_to(socket_client2, input("Please enter client 2 ip"), port_host)()

        elif this_client.message["status"] == "waiting for message 2" and send_message:
            pass

