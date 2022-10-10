import time
import zmq
import pickle
import msgs

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

lat = 47.20446963240012
lon = 38.94366977457449
df = 0.0000001
print("Server created")


while True:
    lat += df
    lon += df

    drone_pose = msgs.Telemetry(lat = lat, lon = lon)
    print(drone_pose.latitude, " ", drone_pose.longitude)
    message = socket.recv()
    # print("Received request: %s" % message)

    time.sleep(0.01)

    socket.send(pickle.dumps(drone_pose))
    # print(1)