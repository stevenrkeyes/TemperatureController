# Author: Steven Keyes
# 27 Jan 2012
# UI for the temperature monitor

import Tkinter, tempMonitor, arduino


class monitorUI(Tkinter.Frame):
    def __init__(self, win):
        Tkinter.Frame.__init__(self, win)
        self.pack() # pack frame into window
        self.createWidgets()

        ard = arduino.Arduino()
        self.tempMonitor = tempMonitor.tempMonitor(ard)
        ard.run()

    def createWidgets(self):
        self.tempLabel = Tkinter.Label(self)
        self.tempLabel["bg"] = "black"
        self.tempLabel["padx"] = 50
        self.tempLabel["pady"] = 250
        self.tempLabel["fg"] = "purple"
        self.tempLabel["text"] = "TT" + u'\N{DEGREE SIGN}' + "F"
        self.tempLabel["font"]=('Digital-7', 100)
        self.tempLabel["anchor"]="center"
        self.tempLabel.pack({"side": "top"})

    # starts the monitor (then calls itself recursively)
    def startMonitor(self):
        self.tempLabel.config(text="77" + u'\N{DEGREE SIGN}' + "F")
        # use the labe's sleep thread function to call this again
        self.tempLabel.after(200, self.startMonitor)
        


win = Tkinter.Tk()
win['bg'] = "black"
win.title("Temperature Monitor")
# syntax: root.geometry('AxB-C+D')
# A is width, B height, C distance from right side of screen, D distance from top of screen
win.geometry('500x300')

UI = monitorUI(win)
UI.startMonitor()

UI.mainloop()
win.destroy()
