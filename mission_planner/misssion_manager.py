import math
from time import sleep
from mission_planner_lib.mission_manager_lib import Mission, MissionManager
from msgs import GeoPoint
from zmq_wrapper_lib import Service, Subscriber, Publisher

IP_ROBOT_POSITION = "192.168.166.100"
IP_NPU_COMMAND = "192.168.166.100"

PORT_ROBOT_POSITION_RECIEVE = "4502"
PORT_ROBOT_POSITION_DESTINATION = "8090"
PORT_NPU_COMMAND = "8100"


def convertDictToGeopoint(point: dict):
    return GeoPoint(point.get("latitude"), point.get("longitude"))


def getDistBetweenGeopoints(point1: GeoPoint, point2: GeoPoint):
    dx = point1.latitude - point2.latitude
    dy = point1.longitude - point2.longitude
    return math.sqrt(dx**2 + dy**2)


class PositionalLocalPlanner:
    def __init__(self, initial_point_idx=0, trajectory_len=0, switch_dist=0.5):
        self.current_point_idx_in_traj = initial_point_idx
        self.trajectory_len = trajectory_len
        self.trajectory_passed = False
        self.switch_dist = switch_dist

    def changeCurrentPointIdxByDistance(self, dist):
        if dist < self.switch_dist:
            if (self.trajectory_len) > self.current_point_idx_in_traj + 1:
                self.current_point_idx_in_traj = self.current_point_idx_in_traj + 1
            else:
                self.trajectory_passed = True

    def getDist(point1: GeoPoint, point2: GeoPoint):
        point1


class MissionPlanner:
    def checkIfMissionIsNotValid(self, mission):
        if mission == None:
            return True
        return False

    def checkIfMissionIsNew(self, recieved_mission, mission_manager):
        new_mission = False
        print(recieved_mission)
        # If no mission recieved
        if mission_manager.getMissionsCount() == 0:
            new_mission = True
        # If there any mission in progress, change current on new one received
        else:
            if recieved_mission.get("mission_waypoints") != mission_manager.missions.get(mission_manager.current_mission).get("mission_waypoints"):
                new_mission = True
        return new_mission

    def missionPlanner(self, recieved_mission, mission_manager):
        if self.checkIfMissionIsNotValid(recieved_mission):
            return mission_manager.missions.get(mission_manager.current_mission), False

        new_mission = self.checkIfMissionIsNew(
            recieved_mission, mission_manager)
        if new_mission == True:
            # If mission any mission in progress
            if mission_manager.getMissionsCount() != 0:
                mission_manager.deleteMission(mission_manager.current_mission)
                mission_manager.addMission(
                    recieved_mission)
                mission_manager.chooseMissionByQueue()

            # If mission no mission in progress
            else:
                # If mission no mission in progress
                mission_manager.addMission(
                    recieved_mission)
                mission_manager.chooseMissionByQueue()

        return mission_manager.missions.get(mission_manager.current_mission), new_mission


def update_robot_pose(robot_pose, target_pose):
    robot_pose.latitude = robot_pose.latitude + \
        (target_pose.latitude - robot_pose.latitude) / 2.0
    robot_pose.longitude = robot_pose.longitude + \
        (target_pose.longitude - robot_pose.longitude) / 2.0
    return robot_pose


def main():

    # Define Publishers and subscriber
    robot_position_subscriber = Subscriber(
        IP_ROBOT_POSITION, PORT_ROBOT_POSITION_RECIEVE)
    current_point_publisher = Publisher(
        IP_ROBOT_POSITION, PORT_ROBOT_POSITION_DESTINATION)

    # Define Service
    mission_service = Service(IP_NPU_COMMAND, PORT_NPU_COMMAND, True)
    mission_service.makeThead()

    # Define Mission Manager
    mission_manager = MissionManager()
    mission_planner = MissionPlanner()
    local_planner = PositionalLocalPlanner()

    mission = Mission()

    # # ZAGLUSKA
    robot_pose = GeoPoint(0, 0, 0)
    robot_position_subscriber.msg = robot_pose
    # ##

    while True:
        print("curent mission ID ", mission_manager.current_mission)

        # TODO: SPLIT CODE IN TWO MODULES, even DIFFERENT MODULES

        mission, new_mission = mission_planner.missionPlanner(
            mission_service.recieved_data, mission_manager)

        # Check if local planner needs a restart, when new mission received
        if new_mission:
            local_planner = PositionalLocalPlanner(
                0, len(mission.get("mission_waypoints")))

        # If any mission exists
        if mission_manager.getMissionsCount() != 0 and mission != None:

            # Local Planner starts here
            if mission != None:
                # Change current planning point
                goal_geopoint_from_dict = mission.get(
                    "mission_waypoints")[local_planner.current_point_idx_in_traj]
                goal_point = convertDictToGeopoint(goal_geopoint_from_dict)

                dist = getDistBetweenGeopoints(
                    robot_position_subscriber.msg,  goal_point)

                local_planner.changeCurrentPointIdxByDistance(dist)
                # publish point to move if mission is not empty
                current_point_publisher.publish(
                    mission.get(
                        "mission_waypoints")[local_planner.current_point_idx_in_traj])

                # Local planner ends here

                # # TODO: DELETE ZAGLUSHKA___
                # robot_pose = update_robot_pose(robot_pose, GeoPoint(
                #     goal_point.latitude, goal_point.longitude))
                # robot_position_subscriber.msg = robot_pose
                # # _____________


            if local_planner.trajectory_passed:
                print(mission_manager.current_mission)
                mission_manager.deleteMission(
                    mission_manager.current_mission)
                mission = None
                mission_service.recieved_data = None
                mission_manager.chooseMissionByQueue()

            print("point in traj to follow",
                  local_planner.current_point_idx_in_traj)

        sleep(0.1)


if __name__ == "__main__":
    main()
