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
    from Histogram_Code import Galaxy_Histogram_Code_3
    for Gname in Gname_L:
        #Pipeline_A Code
        Galaxy_Histogram_Code_3.Driver_Code(Gname) #This runs the histrogram code and creates the histrograms and the directories with the histrograms in them

# Pipelines are quoted until they are finished

def Pipeline_B(Gname_L):
    dir = os.path.dirname(__file__)
    path=os.path.realpath('../')
    #print "Path=",path
    system('pwd')
    sys.path.append(os.path.abspath(path))
    #print sys.path
    from File_Query_Code import File_Query_Code_5
    from XPA_DS9_Region_Generator import XPA_DS9_Region_Generator_3
    for Gname in Gname_L:
        #Pipeline_B Code
        Gname_List=Gname.split(" ")
        print "Gname_List: ", Gname_List
        if(len(Gname_List)>1):
            Gname_Modifed=Gname_List[0]+"_"+Gname_List[1] #Adds underscore to remove space from "NGC #" to change to "NGC_#" if there is a space in the name
        else:
            Gname_Modifed=Gname # Does nothing if the galaxy name has no space, ie. NGC#, For example NGC253 instead of NGC 253 or NGC_253
        print "Gname_Modifed ", Gname_Modifed
        path_2=os.path.realpath('../Master_Code/Master_Output/')
        path_3=path_2+'/'+Gname_Modifed+'/'
        directory = os.path.dirname(path_3)
        if not os.path.exists(directory):
            os.makedirs(directory)
        #os.chdir(path_3) #Goes to Current Galaxies Folder
        path_Area=path_3+'Area_Lists/'
        directory_Area=os.path.dirname(path_Area)
        if not os.path.exists(directory_Area):
            os.makedirs(directory_Area)
        print "path_Area=",path_Area
        #os.chdir(path_Area)
        Evt2_File_H_L=File_Query_Code_5.File_Query(Gname,"evt2")
        Reg_File_H_L=File_Query_Code_5.File_Query(Gname,"reg",".reg")
        print "Evt2_File_H_L ", Evt2_File_H_L
        print "Reg_File_H_L ", Reg_File_H_L
        for Evt2_File_L in Evt2_File_H_L:
            Cur_Evt2_ObsID=Evt2_File_L[0]
            Cur_Evt2_Filepath=Evt2_File_L[1]
            for Reg_File_L in Reg_File_H_L:
                Cur_Reg_ObsID=Reg_File_L[0]
                Cur_Reg_Filepath=Reg_File_L[1]
                if(Cur_Evt2_ObsID==Cur_Reg_ObsID):
                    #print "Test"
                    path_Obs=path_Area+'/'+str(Cur_Evt2_ObsID)+'/'
                    directory_Obs=os.path.dirname(path_Obs)
                    if not os.path.exists(directory_Obs):
                        os.makedirs(directory_Obs)
                    os.chdir(path_Obs)
                    XPA_DS9_Region_Generator_3.XPA_DS9_Region_Generator(Cur_Evt2_Filepath,Cur_Reg_Filepath)
        path_5=os.path.realpath('../../../../')
        os.chdir(path_5)
        #Need to add the rest of Pipeline B after XPA_DS9_Region_Generator
"""
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
        Thread(target = Pipeline_B(Gname_L)).start()
        #Thread(target = Pipeline_C(Gname_L)).start()
        #Thread(target = Pipeline_D(Gname_L)).start()

Master(['NGC4258','M31','NGC 1365']) #This works
