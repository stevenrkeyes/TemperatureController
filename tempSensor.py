# Author: Steven Keyes
# 23 January 2012
# Class that represents a LM335x zener diode temperature sensor
# connected in series with a resistor with an arduino reading the
# voltage above the diode

import arduino, linReg, temperature


# class for a temperature sensor
# also implements a table of read values and their calibrated counterparts
# in order to calibrate the sensor
class tempSensor(arduino.AnalogInput):
    def __init__(self, ard, port, location):
        self.ard = ard

        # list of tuples [(readVoltage, actualTemperature), ...]
        # like [(3.0, temp(k=290)), (4.2, temp(k=310))], etc
        self.calibrationValues = []
        
        arduino.AnalogInput.__init__(self, ard, port)
        

    # read a temperature in K, correcting using the calibration values
    def readTemp(self):
        if len(self.calibrationValues)<2:
            # very rough approximation
            return temperature.temp(k = self.getValue() * (5.0 / 1023.0) * 100 - 220)
        else:
            # just submit the k value, not the temp object
            formattedValues = [(point[0], point[1].k)
                               for point in self.calibrationValues]
            return temperature.temp(k=linReg.forecast(formattedValues,
                                                      self.getValue()))

    def addCalibrationPoint(self, point):
        self.calibrationValues.append(point)

    # getValue is inherited

if __name__ == "__main__":
    import time
    ard = arduino.Arduino()
    t = tempSensor(ard, 0)
    time.sleep(1)

    
