import zmq
from struct import *
import threading
import msgs

import crcmod
from zmq_wrapper_lib import Publisher


class RalTeleServer:
    def __init__(self):
        '''
        Create client to read data from ral
        '''
        self.client = zmq.Context()
        self.client_socket = self.client.socket(zmq.STREAM)  # client with stream type
        self.client_socket.connect("tcp://192.168.166.11:4500")  # connect to ral ip  192.168.166.12:4500 -- 12 ral

        ip = '192.168.166.100'
        port = '4501'
        self.tele_publisher = Publisher(ip, port)
        '''
        Create server to publish data from ral
        '''
        # self.server = zmq.Context()
        # self.server_socket = self.server.socket(zmq.REP)  # request server
        # self.server_socket.bind('tcp://192.168.166.100:4502')

        self.telemetry_raw = None
        self.telemetry = msgs.Telemetry()

        self.tele_server_thread = threading.Thread(target=self.tele_server, args=(), daemon=True)
        self.tele_server_thread.start()  # Start server thread

        self.data_p_1 = []
        self.data_p_2 = []
        self.data_all = []
        # self.ral_tele_thread = threading.Thread(target=self.ral_tele_data, args=(), daemon=True)
        # self.ral_tele_thread.start()  # Start client thread

        # self.ral_tele_data()
        while True:
            ral_data = self.client_socket.recv()  # read raw data from ral
            # print(ral_data)
            if len(ral_data) == 64:
                self.data_p_1 = ral_data
            elif len(ral_data) == 29:
                self.data_p_2 = ral_data
            if self.data_p_1 and self.data_p_2:
                self.data_all = self.data_p_1 + self.data_p_2
                # print(self.data_all)
                crc16 = crcmod.mkCrcFun(0x18005, 0x0000, True, 0xFFFF)
                # print(self.data_all)
                crc = (crc16(self.data_all[-4:-3], crc16(self.data_all[-3:-2], crc16(self.data_all[-2:-1],
                                                                                     crc16(self.data_all[-1:],
                                                                                           crc16(self.data_all[8:-4],
                                                                                                 crc16(self.data_all[
                                                                                                       0:6])))))))
                b_crc_in = self.data_all[6:8]
                # print(b_crc_in)
                crc_in = unpack('=H', b_crc_in)
                # print(int(crc_in[0]))
                # print(int(crc))

                if self.data_all[5] == 81 and self.data_all[8] == 37 and int(crc) == int(crc_in[0]):
                    self.telemetry_raw = unpack('=4cBBHBIHHIi5h5B4H6fH4B2H2B2HBI', self.data_all)

                    self.telemetry.latitude = self.telemetry_raw[29]
                    self.telemetry.longitude = self.telemetry_raw[28]
                    # print(self.telemetry.latitude)
                    # print(self.telemetry.longitude)
                    self.telemetry.altitude = self.telemetry_raw[12] * 0.01
                    self.telemetry.azimute = self.telemetry_raw[15] * 0.1
                    self.telemetry.home_point = [self.telemetry_raw[29], self.telemetry_raw[30]]

            # if len(ral_data) == 64 and ral_data[5] == 81 and ral_data[8] == 37:  # filter ral data
            #     self.telemetry_raw = unpack('=4cBBHBIHHIi5h5B4H4f', ral_data)
            #
            #     # print(self.telemetry_raw)
            #
            #     self.telemetry.latitude = self.telemetry_raw[29]
            #     self.telemetry.longitude = self.telemetry_raw[28]
            #     # print(self.telemetry.latitude)
            #     # print(self.telemetry.longitude)
            #     self.telemetry.altitude = self.telemetry_raw[12] * 0.01
            #     self.telemetry.azimute = self.telemetry_raw[15] * 0.1
            #     self.telemetry.home_point = [self.telemetry_raw[29], self.telemetry_raw[30]]

                # print(self.telemetry.home_point)

    def tele_server(self):
        while True:
            if self.telemetry_raw is not None:
                # message = self.server_socket.recv()
                # print(self.telemetry.latitude)
                self.tele_publisher.publish(self.telemetry)
                # self.server_socket.send(pickle.dumps(self.telemetry))  # Send ral tele data to clients


if __name__ == '__main__':
    RalTeleServer()

