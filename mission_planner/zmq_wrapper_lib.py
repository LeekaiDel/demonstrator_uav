from time import sleep
import zmq
from struct import *
import threading
import msgs


class Subscriber:
    def __init__(self, ip, port):
        '''
        Create subscriber to read data
        @ ip - cpecifies adress of curent machine in network
        @ port - cpecifies port from which data will be listened
        '''

        context = zmq.Context()
        self.subscriber = context.socket(zmq.SUB)
        adress = "tcp://" + ip + ":" + port
        self.subscriber.bind(adress)
        self.subscriber.setsockopt(zmq.SUBSCRIBE, b'')
        self.msg = None

        threading.Thread(target=self.startSubscription).start()

    def startSubscription(self):
        while True:
            self.msg = self.subscriber.recv_pyobj()
            print(self.msg)


class Publisher:
    def __init__(self, frequency, ip, port):
        '''
        Create publisher to publish data
        @ ip - cpecifies adress of machine to which topic should be broadcasted
        @ port - cpecifies port to which data will be published
        '''
        self.frequency = 1.0 / float(frequency)

        context = zmq.Context()
        self.publisher = context.socket(zmq.PUB)
        adress = "tcp://" + ip + ":" + port
        print(adress)
        self.publisher.connect(adress)

        self.msg = None
        threading.Thread(target=self.startPublisher).start()

    def startPublisher(self):
        while True:
            self.publisher.send_pyobj(self.msg)
            sleep(self.frequency)
