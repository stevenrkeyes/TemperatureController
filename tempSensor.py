# Author: Steven Keyes
# 23 January 2012
# Class that represents a LM335x zener diode temperature sensor
# connected in series with a resistor with an arduino reading the
# voltage above the diode

import arduino, linReg, temperature, pickle

# class for a temperature sensor
# also implements a table of read values and their calibrated counterparts
# in order to calibrate the sensor
class tempSensor(arduino.AnalogInput):
    def __init__(self, ard, port, location):
        self.ard = ard
        
        # string for storing the physical location of the sensor
        self.location = location

        # calibration values:
        # list of tuples [(readValue, actualTemperature), ...]
        # like [(600, temp(k=290)), (800, temp(k=310))], etc

        # try loading previous calibration values if they exist
        # in file like "desk_CalibrationData", which is a pickle
        try:
            f = open(str(self.location)+"_CalibrationData", 'r')
            self.calibrationValues = pickle.load(f)
            f.close()
        except IOError:
            self.calibrationValues = []
        
        arduino.AnalogInput.__init__(self, ard, port)

    # read a temperature in K, correcting using the calibration values
    def readTemp(self):
        if len(self.calibrationValues)<2:
            # very rough approximation
            return temperature.temp(f = self.getValue() * (5.0 / 1023.0) * 100 - 220)
        else:
            # just submit the k value, not the temp object
            formattedValues = [(point[0], point[1].k)
                               for point in self.calibrationValues]
            return temperature.temp(k=linReg.forecast(formattedValues,
                                                      self.getValue()))

    def addCalibrationTemp(self, temp):
        point = (self.getValue(), temp)
        self.calibrationValues.append(point)

        # save the updated calibration values
        f = open(str(self.location)+"_CalibrationData", 'w')
        pickle.dump(self.calibrationValues, f)
        f.close()

    # getValue is inherited

if __name__ == "__main__":
    import time
    ard = arduino.Arduino()
    t = tempSensor(ard, 0, "desk")
    ard.run()
    time.sleep(1)

    
