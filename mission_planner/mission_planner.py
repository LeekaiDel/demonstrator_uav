from mission_planner_lib.mission_manager_lib import Mission, MissionManager
from zmq_wrapper_lib import Publisher, Subscriber


def main():
    topic = "topic"
    frequency = 10

    publish_point = Publisher(topic, frequency)
    subscribe_recieve_pose = Subscriber(topic)
    publish_point.msg = Mission


if __name__ == "__main__":
    main()
