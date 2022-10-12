import zmq
from struct import *
import threading
import msgs
import pickle

class RalTeleServer:
    def __init__(self):
        '''
        Create client to read data from ral
        '''
        self.client = zmq.Context()
        self.client_socket = self.client.socket(zmq.STREAM)  # client with stream type
        self.client_socket.connect("tcp://192.168.166.11:4500")  # connect to ral ip  192.168.166.12:4500 -- 12 ral

        '''
        Create server to publish data from ral
        '''
        self.server = zmq.Context()
        self.server_socket = self.server.socket(zmq.REP)  # request server
        self.server_socket.bind('tcp://192.168.166.100:4501')

        self.telemetry_raw = None
        self.telemetry = msgs.Telemetry()

        self.tele_server_thread = threading.Thread(target=self.tele_server, args=(), daemon=True)
        self.tele_server_thread.start()  # Start server thread

        # self.ral_tele_thread = threading.Thread(target=self.ral_tele_data, args=(), daemon=True)
        # self.ral_tele_thread.start()  # Start client thread

        # self.ral_tele_data()
        while True:
            ral_data = self.client_socket.recv()  # read raw data from ral
            if len(ral_data) == 64 and ral_data[5] == 81 and ral_data[8] == 37:  # filter ral data
                self.telemetry_raw = unpack('=4cBBHBIHHIi5h5B4H4f', ral_data)
                self.telemetry.latitude = self.telemetry_raw[29]
                self.telemetry.longitude = self.telemetry_raw[28]
                self.telemetry.azimute = self.telemetry_raw[15] * 0.1

    def tele_server(self):
        while True:
            if self.telemetry_raw is not None:
                message = self.server_socket.recv()
                # print(message)
                self.server_socket.send(pickle.dumps(self.telemetry))  # Send ral tele data to clients


if __name__ == '__main__':
    RalTeleServer()

