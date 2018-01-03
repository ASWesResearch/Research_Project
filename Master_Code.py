import subprocess
import threading
from threading import Thread
import os
from os import system
import sys
def Pipeline_A(Gname_L):
    #Imports alaxy_Histogram_Code_2
    #os.system('python Hello_World.py')
    #dir = os.path.dirname(__file__)
    #path=os.path.realpath('../GitHub/Galaxy_Histogram_Code.py') #Need to modify so it is possible to input Gname to the Galaxy_Histogram_Code
    #print "Path=",path
    #system('pwd')
    #os.system('python '+path) #Runs Galaxy_Histogram_Code.py
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
    for Gname in Gname_L:
        #Pipeline_A Code
        Galaxy_Histogram_Code_2.Driver_Code(Gname) #This runs the histrogram code and creates the histrograms and the directories with the histrograms in them
"""
# Pipelines are quoted until they are finished
def Pipeline_B(Gname_L):
    for Gname in Gname_L:
        #Pipeline_B Code
def Pipeline_C(Gname_L):
    for Gname in Gname_L:
        #Pipeline_C Code
def Pipeline_D(Gname_L):
    for Gname in Gname_L:
        #Pipeline_D Code
"""

def Master(Gname_L):
    if __name__ == '__main__':
        Thread(target = Pipeline_A(Gname_L)).start()
        #Thread(target = Pipeline_B(Gname_L)).start()
        #Thread(target = Pipeline_C(Gname_L)).start()
        #Thread(target = Pipeline_D(Gname_L)).start()

Master(['NGC4258','M31']) #This works
