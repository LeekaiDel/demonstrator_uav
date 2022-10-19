from time import sleep
import zmq
from struct import *
import threading
import msgs


class Subscriber:
    def __init__(self, topic):
        '''
        Create subscriber to read data
        '''

        context = zmq.Context()
        self.subscriber = context.socket(zmq.SUB)
        self.subscriber.bind("ipc://"+ topic)
        self.subscriber.setsockopt(zmq.SUBSCRIBE, b'')
        self.msg = None
        
        threading.Thread(target=self.startSubscription).start()


    def startSubscription(self):
        while True:
            self.msg = self.subscriber.recv_pyobj()
            print(self.msg)


class Publisher:
    def __init__(self, topic, frequency):
        '''
        Create publisher to publish data
        '''
        self.frequency = 1.0 / float(frequency)

        context = zmq.Context()
        self.publisher = context.socket(zmq.PUB)
        self.publisher.connect("ipc://"+ topic)

        self.msg = None
        threading.Thread(target=self.startPublisher).start()


    def startPublisher(self):
        while True:     
            self.publisher.send_pyobj(self.msg)
            sleep(self.frequency)
            
