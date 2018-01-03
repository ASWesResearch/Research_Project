import threading
from threading import Thread
import os
from os import system
def func1():
    print 'Working'
def func2():
    #print 'Working'
    import os
    from os import system
    #os.system('python Hello_World.py')
    dir = os.path.dirname(__file__)
    path=os.path.realpath('../GitHub/Galaxy_Histogram_Code_2.py')
    print "Path=",path
    system('pwd')
    os.system('python '+path)
if __name__ == '__main__':
    Thread(target = func1).start()
    Thread(target = func2).start()
