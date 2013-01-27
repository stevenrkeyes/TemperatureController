# Author: Steven Keyes
# 23 Jan 2012
# code for manipulating temperatures

# based on code found here
# http://code.activestate.com/recipes/286226-temperature-class/

# class that represents a temperature
class temp(object):
    equations = {'c': (1.0, 0.0, -273.15), 'f': (1.8, -273.15, 32.0)}
    
    # init a temperature object with a temperature value
    # like c=5 or k=278.15; defaults to k=0
    def __init__(self, k=0, **args):
        self.k = k
        
        # check if the temperature is input in a different unit
        for u in args:
            if u in ('f', 'c', 'k'): # lol
                # if so, set the temperature in kelvin
                setattr(self, u, args[u])

    # return the temperature obtained calculating from the temp in k
    def __getattr__(self, name):
        # if it's "c" or "f", calculate it
        if name in self.equations: 
            eq = self.equations[name]
            return (self.k + eq[1]) * eq[0] + eq[2]
        else:
            # if it's k or some other attribute, just look it up
            return object.__getattr__(self, name) 

    # set the temp in k by converting from the given temperature
    def __setattr__(self, name, value):
        if name in self.equations:
            eq = self.equations[name]
            self.k = (value - eq[2]) / eq[0] - eq[1]
        else:
            object.__setattr__(self, name, value)

    def __str__(self):
        return "%g K" % self.k

    def __repr__(self):
        return "Temperature(%g)" % self.k

    def __float__(self):
        return float(self.k)

    def __int__(self):
        return int(self.k)
