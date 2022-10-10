import zmq 
import pickle
# import msgs
context = zmq.Context()

print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

for request in range(10):
    print("Sending request %s …" % request)
    socket.send(b"Hello")
    message = socket.recv()

# while True:
#     message = socket.recv()
#     print(message)
    # print("Received reply %s [ %s ]" % (request, type(pickle.loads(message))))
    print(pickle.loads(message).latitude, " ",pickle.loads(message).longitude)