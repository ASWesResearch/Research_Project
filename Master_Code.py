import subprocess
import threading
from threading import Thread
import os
from os import system
def Pipeline_A(Gname_L):
    for Gname in Gname_L:
        #Pipeline_A Code
        #os.system('python Hello_World.py')
        dir = os.path.dirname(__file__)
        path=os.path.realpath('../GitHub/Galaxy_Histogram_Code.py') #Need to modify so it is possible to input Gname to the Galaxy_Histogram_Code
        #print "Path=",path
        #system('pwd')
        os.system('python '+path) #Runs Galaxy_Histogram_Code.py
def Pipeline_B(Gname_L):
    for Gname in Gname_L:
        #Pipeline_B Code
def Pipeline_C(Gname_L):
    for Gname in Gname_L:
        #Pipeline_C Code
def Pipeline_D(Gname_L):
    for Gname in Gname_L:
        #Pipeline_D Code
def Master():
    if __name__ == '__main__':
        Thread(target = Pipeline_A).start()
        Thread(target = Pipeline_B).start()
        Thread(target = Pipeline_C).start()
        Thread(target = Pipeline_D).start()
