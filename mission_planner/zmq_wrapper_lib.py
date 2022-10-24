from time import sleep
import zmq
from struct import *
import threading
import json


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
    def __init__(self, ip, port):
        '''
        Create publisher to publish data
        @ ip - cpecifies adress of machine to which topic should be broadcasted
        @ port - cpecifies port to which data will be published
        '''

        context = zmq.Context()
        self.publisher = context.socket(zmq.PUB)
        adress = "tcp://" + ip + ":" + port
        print(adress)
        self.publisher.connect(adress)

        self.msg = None

    def publish(self, data):
        self.publisher.send_pyobj(data)
        # sleep(self.frequency)


class Service:
    def __init__(self, ip="", port="", use_json=False):
        # recieved_data from client
        # data_to_send to client
        self.use_JSON = use_json
        context = zmq.Context().instance()
        url = "tcp://" + ip + ":" + port

        self.recieved_data = None
        self.data_to_send = None

        self.server = context.socket(zmq.REP)
        self.server.bind(url)

    def recieveData__(self):
        self.recieved_data = self.server.recv_pyobj()
        # print(self.recieved_data)

    def recieveDataJSON__(self):
        self.recieved_data = json.loads(self.server.recv_pyobj())
        # print(self.recieved_data)

    def reply__(self):
        self.server.send_pyobj(self.data_to_send)

    def startService(self):
        if self.use_JSON:
            while True:
                self.recieveDataJSON__()
                self.reply__()
        else:
            while True:
                self.recieveData__()
                self.reply__()

    def makeThead(self):
        threading.Thread(target=self.startService).start()


class Client:
    def __init__(self, ip="", port=""):
        # recieved_data from service
        # data_to_send to service
        context = zmq.Context().instance()
        url = "tcp://" + ip + ":" + port

        self.recieved_data = None
        self.data_to_send = None

        self.client = context.socket(zmq.REQ)
        self.client.connect(url)

    def sendRequest__(self):
        self.client.send_pyobj(self.data_to_send)

    def getRespose__(self):
        self.recieved_data = self.client.recv_pyobj()
        print("Got msg = ", self.recieved_data)

    def startClient(self):
        self.sendRequest__()
        self.getRespose__()

    def makeThead(self):
        threading.Thread(target=self.startClient).start()
