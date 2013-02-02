# Author: Steven Keyes
# 27 Jan 2012
# UI for the temperature monitor

import tempMonitor, arduino_win, time, Tkinter, ttk, temperature
#from Tkinter import *
#from ttk import * # to override some of the Tkinter widgets


class monitorUI(Tkinter.Frame):
    def __init__(self, win):
        Tkinter.Frame.__init__(self, win)

        self["padx"] = 15
        self["pady"] = 15
        self["bg"] = "black"
        
        self.grid() # pack frame into window

        # create an object for interfacing with the arduino
        self.ard = arduino_win.Arduino()

        self.tempMonitor = tempMonitor.tempMonitor(self.ard)

        # create widgets using information about the temp monitor
        self.createWidgets()

        self.ard.run()
        # wait for the arduino's ports to open
        time.sleep(0.75)

    def createWidgets(self):

        # temperature text
        self.tempLabel = Tkinter.Label(self)
        self.tempLabel["bg"] = "black"
        self.tempLabel["padx"] = 25
        self.tempLabel["pady"] = 25
        self.tempLabel["fg"] = "purple"
        self.tempLabel["text"] = "TT" + u'\N{DEGREE SIGN}' + "F"
        self.tempLabel["font"]=('Digital-7', 100)
        self.tempLabel["anchor"]="center"
        
        # combobox widget with location
        self.locationSelection = ttk.Combobox(self)
        self.locationSelection['values'] = [sensor.location for sensor in self.tempMonitor.sensors]
        self.locationSelection.current(0)
        self.locationSelectionValue = ''
        self.locationSelection["textvariable"] = self.locationSelectionValue
        self.locationSelection["state"] = "readonly"
        self.locationSelection["width"] = 7
        #self.locationSelection["padding"] = "10 0 0 10"
        
        # place to type temperature
        self.tempTypeBox = ttk.Entry(self)
        self.tempTypeBox["width"] = 5
        #self.tempTypeBox["padx"] = 10
        
        # label afterward with degF
        self.degFsign = ttk.Label(self)
        #self.degFsign["background"] = "black"
        self.degFsign["text"] = u'\N{DEGREE SIGN}' + "F"
        #self.degFsign["padx"] = 10
        
        # button to submit new calibration
        self.calibrateButton = ttk.Button(self)        
        self.calibrateButton["text"] = "Recalibrate"
        self.calibrateButton["command"] = self.addCalibrationInput
        self.calibrateButton["width"] = 9
        #self.calibrateButton["padx"] = 10

        # place all the widgets
        self.locationSelection.grid(row=1, column=0, ipadx=10)
        self.tempTypeBox.grid(row=1, column=1, ipadx=4, sticky='E')
        self.degFsign.grid(row=1, column=2, sticky='W')
        self.calibrateButton.grid(row=1, column=3, ipadx=10)
        
        self.tempLabel.grid(row=0, columnspan=4)

    def addCalibrationInput(self):
        # get the sensor location and the new calibration temperature in defF
        sensorLocation = self.locationSelection.get()
        newTemp = temperature.temp(f=float(self.tempTypeBox.get()))

        # set the temperature
        self.tempMonitor.getSensor(sensorLocation).addCalibrationTemp(newTemp)

        # clear the entry field
    
    # starts the monitor (then cal5ls itself recursively)
    def startMonitor(self):

        # if the arduino is connected, run the stuff
        if self.ard.portOpened:

            # print the temperatures
            for sensor in self.tempMonitor.sensors:
                print sensor.location, sensor.readTemp().f
            print "---------------"

            # display the average temperatures
            t = str(int(round(self.tempMonitor.avgTemp().f)))
            self.tempLabel.config(text=t + u'\N{DEGREE SIGN}' + "F")
            # use the labe's sleep thread function to call this again
            self.locationSelection.after(200, self.startMonitor)
        else:
            print "arduino not connected"
        


win = Tkinter.Tk()
win['bg'] = "black"
win.title("Temperature Monitor")
# syntax: root.geometry('AxB-C+D')
# A is width, B height, C distance from right side of screen, D distance from top of screen
win.geometry('440x300')

UI = monitorUI(win)
UI.startMonitor()

UI.mainloop()
UI.ard.stop()
win.destroy()
