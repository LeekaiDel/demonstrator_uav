import crcmod
from struct import *
import zmq
import threading
from zmq_wrapper_lib import Subscriber


class RalPoint:
    def __init__(self):
        self.identify_drone = 2070360064

        self.ral_client = zmq.Context()
        self.point_to_ral_client = self.ral_client.socket(zmq.PUB)
        self.point_to_ral_client.connect("tcp://192.168.166.12:4500")

        # self.client = zmq.Context()
        # self.point_client = self.client.socket(zmq.SUB)
        # adress = "tcp://192.168.88.182:8090"

        self.point_sub = Subscriber("192.168.166.100","8090")


        # self.point_client.bind(adress)
        # self.point_client.setsockopt(zmq.SUBSCRIBE, b'')
        # self.msg = None

        while True:
            if self.point_sub.msg is not None:
                self.msg = self.point_sub.msg
                latitude = round(self.msg.get("latitude"), 6)
                longitude = round(self.msg.get("longitude"), 6)

                self.do_point(latitude, longitude)


        # self.point_client.connect("tcp://192.168.88.182:8090")  # TODO ip port

    def add_crc(self, byte_data):
        b = byte_data
        crc16 = crcmod.mkCrcFun(0x18005, 0x0000, True, 0xFFFF)
        hex_crc = hex(crc16(b[-4:-3], crc16(b[-3:-2], crc16(b[-2:-1], crc16(b[-1:], crc16(b[6:-4], crc16(b[0:6])))))))
        byte_crc = bytearray.fromhex(hex_crc[2:])
        out_data = b[0:6] + byte_crc[1:] + byte_crc[0:1] + b[6:]
        return out_data

    def do_point(self, lat, lon):
        data_pack = pack('=4c3B2fBHBI', b'A', b'E', b'N', b'T', 1, 13, 206, lat, lon, 1, 0, 51, self.identify_drone)
        print(data_pack)
        # data_pack_1 = unpack('=4c3B2fBHBI', data_pack)
        # print(data_pack_1)
        send_data = self.add_crc(data_pack)

        self.point_to_ral_client.send(send_data)


# def cmd_move():
#     print("движение вверх - 1\nдвижение вниз - 2\nдвижение вперед - 3\nдвижение назад - 4\nдвижение влево - 5\n"
#           "движение вправо - 6\nповорот по часовой - 7\nповорот против часовой - 8\nполет в точку - 9")
#     cmd = int(input("Введите команду: "))
#     if cmd >= 1 and cmd <= 6:
#         var = (int(input("Введите величину в метрах: ")))
#         do_move(cmd, var)
#     elif cmd == 7 or cmd == 8:
#         var = int(input("Введите величину в градусах: "))
#         do_move(cmd, var)
#     elif cmd == 9:
#         lat = float(input("Введите широту в градусах: "))
#         lon = float(input("Введите долготу в градусах: "))
#         do_point(lat, lon)
#     else:
#         pass


# def do_move(cmd, var):
#     v = var * 100
#     type_cmd = b'\x00'
#     if cmd == 1:
#         type_cmd = b'\x11'
#     elif cmd == 2:
#         type_cmd = b'\x32'
#     elif cmd == 3:
#         type_cmd = b'\x49'
#     elif cmd == 4:
#         type_cmd = b'\x5B'
#     elif cmd == 5:
#         type_cmd = b'\x6F'
#     elif cmd == 6:
#         type_cmd = b'\x73'
#     elif cmd == 7:
#         type_cmd = b'\x84'
#     elif cmd == 8:
#         type_cmd = b'\x97'
#     else:
#         pass
#     data_pack = pack('=4c3BchI', b'A', b'E', b'N', b'T', 1, 4, 207, type_cmd, v, identify_drone)
#     send_data = add_crc(data_pack)
#     print(send_data)
#     s.sendall(send_data)

def main():
    RalPoint()


if __name__ == '__main__':
    main()
