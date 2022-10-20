from time import sleep
from zmq_wrapper_lib import Publisher, Subscriber, Service, Client
import msgs


def main():
    # topic = "topic"
    # frequency = 1

    ip = "192.168.88.229"
    port = "8100"

    service = Service(ip, port)
    client = Client(ip, port)

    # # initialize client data to send
    msg = msgs.Mission()
    for i in range(10):
        ms = msgs.GeoPoint(i, i*2, i*3)
        msg.mission_waypoints.append(ms)

    msg = msg.toJSON()

    client.data_to_send = msg

    # initialize server data to send
    service.data_to_send = "PONG"

    service.makeThead()

    while True:
        sleep(1)
        client.startClient()


if __name__ == "__main__":
    main()
