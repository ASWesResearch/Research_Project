import threading
from threading import Thread
import os
from os import system
import sys
def func1():
    print 'Working'
def func2():
    #print 'Working'
    import os
    from os import system
    #os.system('python Hello_World.py')
    dir = os.path.dirname(__file__)
    #path=os.path.realpath('../GitHub/Galaxy_Histogram_Code_2.py')
    path=os.path.realpath('../')
    print "Path=",path
    system('pwd')
    #os.system('python '+path) #This works when inputs are not used
    #import Galaxy_Histogram_Code_2
    #Driver_Code('NGC4258')
    sys.path.append(os.path.abspath(path))
    print sys.path
    #from Galaxy_Histogram_Code_2 import *
    #import Galaxy_Histogram_Code_2
    from Histogram_Code import Galaxy_Histogram_Code_2
    Galaxy_Histogram_Code_2.Driver_Code('NGC4258')
    #print "Parinoia Test"
if __name__ == '__main__':
    Thread(target = func1).start()
    Thread(target = func2).start()
