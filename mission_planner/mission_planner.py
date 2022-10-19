from mission_planner_lib.mission_manager_lib import Mission, MissionManager
from zmq_wrapper_lib import Publisher, Subscriber


def main():
    topic = "topic"
    frequency = 1

    ip = "192.168.88.229"
    port = "8080"

    publish_point = Publisher(frequency, ip, port)
    subscribe_recieve_pose = Subscriber(ip, port)
    publish_point.msg = Mission


if __name__ == "__main__":
    main()
