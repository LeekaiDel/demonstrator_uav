import zmq
from struct import *
import threading
import msgs
import pickle

class Client:
    def __init__(self, ip: str = "", port: str = ""):
        '''
        Create client to read data from ral
        '''
        self.telemetry_raw = None
        self.telemetry = msgs.Telemetry()

        self.client = zmq.Context()
        self.client_socket = self.client.socket(zmq.STREAM)  # client with stream type
        self.client_socket.connect("tcp://" + ip + ":" + port)  # connect to ral ip  192.168.166.12:4500 -- 12 ral

        self.create_thread()

    def create_thread(self):
        thread = threading.Thread(target=self.start_client(), args=(), daemon=True)
        thread.start()

    def start_client(self):
        while True:
            ral_data = self.client_socket.recv()  # read raw data from ral
            if len(ral_data) == 64 and ral_data[5] == 81 and ral_data[8] == 37:  # filter ral data
                self.telemetry_raw = unpack('=4cBBHBIHHIi5h5B4H4f', ral_data)
                self.telemetry.latitude = self.telemetry_raw[29]
                self.telemetry.longitude = self.telemetry_raw[28]
                self.telemetry.azimute = self.telemetry_raw[15] * 0.1


class Server:
    def __init__(self, ip: str = "", port: str = ""):
        '''
        Create server to publish data from ral
        '''
        self.telemetry_raw = None
        self.telemetry = msgs.Telemetry()

        self.server = zmq.Context()
        self.server_socket = self.server.socket(zmq.REP)  # request server
        self.server_socket.bind("tcp://" + ip + ":" + port)

        self.create_thread()

    def create_thread(self):
        thread = threading.Thread(target=self.start_server(), args=(), daemon=True)
        thread.start()

    def start_server(self):
        while True:
            if self.telemetry_raw is not None:
                message = self.server_socket.recv()
                # print(message)
                self.server_socket.send(pickle.dumps(self.telemetry))  # Send ral tele data to clients

