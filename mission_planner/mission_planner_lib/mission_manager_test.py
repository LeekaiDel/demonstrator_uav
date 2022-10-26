from mission_manager_lib import MEvent, Mission, MissionManager


def createMisions(i: int):
    points = list()
    points.append(MEvent(1*i, 2*i, 3*i))
    points.append(MEvent(1*i, 2*i, 4*i))
    points.append(MEvent(1*i, 2*i, 5*i))
    points.append(MEvent(2*i, 2*i, 5*i))
    points.append(MEvent(4*i, 4*i, 5*i))
    points.append(MEvent(10*i, 10*i, 5*i))

    return Mission(points, MEvent(0, 0, 0), 10*i)


def main():
    missionManager = MissionManager()
    for mission_number in range(10):
        missionManager.addMission(createMisions(mission_number))

    missionManager.chooseMissionByQueue()
    missionManager.deleteMission(missionManager.current_mission)
    missionManager.chooseMissionByQueue()
    # missionManager.resetMissionManager()
    mission = missionManager.getMissionByKey(
        missionManager.current_mission)
    return


if __name__ == "__main__":
    main()
