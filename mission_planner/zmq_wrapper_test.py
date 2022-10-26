from time import sleep
from zmq_wrapper_lib import Publisher, Subscriber, Service, Client
import msgs


def main():
    # topic = "topic"
    # frequency = 1

    ip = "192.168.0.127"
    port = "8100"

    # service = Service(ip, port)
    client = Client(ip, port)
    print("HERE")
    # # initialize client data to send
    msg = msgs.Mission()
    for i in range(10):
        ms = msgs.GeoPoint(i*1, i*1, i*4)
        msg.mission_waypoints.append(ms)
    print("HERE 1")

    client.data_to_send = msg.toJSON()

    # initialize server data to send
    # service.data_to_send = "PONG"

    # service.makeThead()
    print("HERE 2")

    while True:
        sleep(1)
        client.startClient()
        print("SENDED")


if __name__ == "__main__":
    main()
