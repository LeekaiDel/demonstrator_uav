from zmq_wrapper_lib import Client, Server

IP_HOST = ""
IP_TARGET = ""

PORT_HOST = ""
PORT_TARGET = ""


def main():
    client1 = Client(IP_TARGET, PORT_TARGET)
    server1 = Server(IP_HOST, PORT_HOST)
    while True:
        print()
        print()



if __name__ == "__main__":
    main()