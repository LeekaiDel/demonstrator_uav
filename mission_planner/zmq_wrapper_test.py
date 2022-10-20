from time import sleep
from zmq_wrapper_lib import Publisher, Subscriber, Service, Client


def main():
    # topic = "topic"
    # frequency = 1

    ip = "192.168.88.229"
    port = "8100"

    service = Service(ip, port)
    client = Client(ip, port)

    # initialize client data to send
    client.data_to_send = "PING"

    # initialize server data to send
    service.data_to_send = "PONG"

    service.makeThead()

    while True:
        sleep(1)
        client.startClient()
        # print(client.recieved_data + " " + service.recieved_data)


if __name__ == "__main__":
    main()
