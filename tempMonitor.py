# Author: Steven Keyes
# 23 Jan 2012
# monitor for temperatures

# other backend pieces:
# along with the radiator controller
# radiator knob reader

import tempSensor, threading

# class that represents a temperature monitor for steven's room
class tempMonitor:
    def __init__(self, ard):
        self.ard = ard

        sensors = [tempSensor.tempSensor(ard, 0, "desk"),
                   tempSensor.tempSensor(ard, 1, "bed"),
                   tempSensor.tempSensor(ard, 2, "door"),
                   tempSensor.tempSensor(ard, 3, "hall"),
                   tempSensor.tempSensor(ard, 4, "radiator")]

    def avgTemp(self):
        return sum([sensor.readTemp() for sensor in self.sensors])/len(self.sensors)
    # later, implement weighted average temperature

    def getSensor(self, location):
        return [sensor for sensor in self.sensors if sensor.location == location][0]
    # from this, you can access the sensor's getTemp and addCalibrationPoint methods

            
