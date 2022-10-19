class MEvent:

    # Class-structure with parameters (can be overrided - edited)
    # def __init__(self, lat=0, long=0, height=0):
    #     self.lat = float(lat)
    #     self.long = float(long)
    #     self.height = float(height)

    def __init__(self, x=0, y=0, z=0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)


class Mission:
    # Class-structure with mission parameters

    def __init__(self, trajectory=list(), origin=MEvent(), mission_time_stamp=0.0):
        self.trajectory = trajectory
        self.origin = origin
        self.mission_time_stamp_ = mission_time_stamp


class MissionManager:
    # Class for working with missions

    def __init__(self):
        self.missions = dict()
        self.current_mission = None
        self.mission_counter = 0  # Номер следуещей команды
        pass

    def __getMissionsCount(self):
        # Returns amount of missions in dict (self.missions)
        return len(self.missions)

    def __getMissionsIDs(self):
        # returns list of keys from dictionary (self.missions)
        return list(self.missions.keys())

    def __raiseMissionCounter(self):
        # Increases latest ID (Needs for future uniqe ID)
        self.mission_counter = self.mission_counter + 1
        pass

    def getMissionByKey(self, key: int):
        # Returns object of Mission according to key (key)
        return self.missions.get(key)

    def getCurrentMissionNumber(self):
        # TODO: needs a rename
        return self.mission_counter

    def addMission(self, mission: Mission):
        # Adds an object (mission) in dict(self.missions)
        self.__raiseMissionCounter()
        self.missions[self.mission_counter] = mission
        pass

    def deleteMission(self, mission_number: int):
        # Deletes an object from dict(self.missions) according to ID(mission_number)
        self.missions.pop(mission_number)
        return

    def chooseMissionByPriority(self):
        # TODO: if some kind of priority needed
        return

    def chooseMissionByQueue(self):
        # Takes first mission from dictionary (self.missions)
        keys_count = self.__getMissionsCount()
        if keys_count == 0:
            self.current_mission = None
        else:
            self.current_mission = self.__getMissionsIDs()[0]
        pass

    def chooseMissionByKey(self, key: int):
        # Defines key to current mission (key)
        self.current_mission = key
        pass

    def resetMissionManager(self):
        # Resets class MissionManager
        self.__init__()
