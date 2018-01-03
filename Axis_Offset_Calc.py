from ciao_contrib.runtool import *
import os
from os import system
def Axis_Offset_Calc(fname,evtfname):
    dir = os.path.dirname(__file__)
    #filename= os.path.join(dir, '~','Desktop','SQL_Standard_File',)
    #filepath=os.path.abspath("~/Desktop/SQL_Standard_File")
    #print "Filepath =",filepath
    #path= os.path.join(dir,'~','Desktop','SQL_Standard_File',)
    #path=os.path.realpath('~/Desktop/SQL_Standard_File/SQL_Sandard_File.csv')
    path=os.path.realpath('../Axis_Offset_Files/'+str(fname))
    print "Path=",path
    #Sourcefile=open("/home/asantini/Desktop/Axis_Offset_Files/"+str(fname),"r") #Sourcefile:-file, Sourcefile, The text file contianing the coordinates of X-ray objects in physical(?) coordinates in pixels
    Sourcefile=open(path,"r") #Sourcefile:-file, Sourcefile, The text file contianing the coordinates of X-ray objects in physical(?) coordinates in pixels
    SourceS=Sourcefile.read() #SourceS:-str, Source String, The string contianing all the physical coordinates of the objects in pixels
    rowL=SourceS.split('\n') #rowL:-list, Row List, The list of all the rows of the text files as strings
    row_num_L=[] #row_num_L:-list, Row Number List, The list of all row numbers in the file as int
    Theta_L=[] #Theta_L:-list, Theta List, The list of all offaxis angles of the objects in the observation
    for i in range(0,len(rowL)): #Iterates through the Row List selecting each object posistion string one at a time
        Cur_Row=rowL[i] #Cur_Row:-str, Current Row, The current object posistion string with whitespace still in it
        Cur_Row_R="".join(Cur_Row.split()) #Cur_Row_R:-str, Current Row Reduced, The current object posistion string with whitespace removed.
        #print "Cur_Row_R", Cur_Row_R
        Cur_Row_Num=Cur_Row_R.split('(')[0] #Cur_Row_Num:-str, Current Row Number, The current number of the row in the file, ie. Row 2 is "2 (     4861.2316715543,     3583.7976539589)"
        row_num_L.append(int(Cur_Row_Num)) #Appends the currnet row number as an int on to the Row Number List
        Cur_Coords=Cur_Row_R.split('(')[1] #Cur_Coords:-str, Current Coordinates, The unreduced string contianing the coordinates of the current object in the form "4861.2316715543,3583.7976539589)"
        Cur_X=Cur_Coords.split(',')[0] #Cur_X:-str, Current X, The current X coordinate in pixels as a string
        Cur_Y_Raw=Cur_Coords.split(',')[1] #Cur_Y_Raw:-str, Currnet Y Raw, The unreduced string contianing the Y coordinate of the current object in the form "3583.7976539589)"
        Cur_Y=Cur_Y_Raw.split(')')[0] #Cur_Y:-str, Current Y, The current Y coordinate in pixels as a string
        dmcoords(infile=str(evtfname),x=float(Cur_X), y=float(Cur_Y), option='sky', verbose=0) #Calls dmcoords to get the offaxis angle from the physical coordinates #I should just use the RA and DEC of each X-ray object instead of the SKY coordinate
        Cur_Theta=dmcoords.theta #Cur_Theta:-float, Current Theta, The current offaxis angle of the object in arcmin
        Theta_L.append(Cur_Theta) #Appends the current offaxis angle to the Theta List
        #print Cur_Theta
    return Theta_L

print Axis_Offset_Calc('NGC_253_Objects_Physical_Coordinates_Plain_Text_Modifed.txt','acisf13830_repro_evt2.fits')
