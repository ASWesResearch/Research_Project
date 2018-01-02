from astroquery.ned import Ned
from ciao_contrib.runtool import *
from region import *
import numpy as np
import math
import os
from os import system
def Background_Finder_3(gname,evtfname,objLfname,R): #Need to apply energy filter (0.3kev to 10kev) to the counts, This may allow the code to treat back illuminated chips and front illuminated chips the same, if not then the code must be modifed to consider both cases
    """
    gname:-str, Galaxy Name, The name of the galaxy in the form NGC #, For Example 'NGC 3077'
    evtfname:-str, Event File Name, The name of the event file of the observation, For Example 'acisf02076_repro_evt2.fits'
    objLfname:-str, Object List File Name, The name of the object list file which is a list of circluar regions around the X-ray objects. For Example 'ngc3077_ObsID-2076_Source_List_R_Mod_2.txt'
    n:-int, Number of objects, The number of objects in the observation
    R:-float(?) or int, Radius, The radius of the circle used to find the background in pixels
    Returns: BG_Ratio:-float, Background Ratio, The background ratio in number of counts per pixel
             or "None" if a region without an object in it cannot be found
    """
    Obj_L=[] #Obj_L:-List, Object_List, The list of all object string shapes in the observation
    Obj_B=True #Obj_B:-bool, Object Boolean, A Boolean statement in regards to if there is no X-ray objects in the area being used to find the background
    List_Done_Bool=False #List_Done_Bool:-bool, List_Done_Boolean, A Boolean statement in regards to if 3 background measurments were found in the observation
    #BG_Circle_Overlap_Bool=False
    BG_R=R # Note: Physical Radius might not be equal to the Pixel Radius
    Num_BG_Pix=math.pi*((BG_R)**2) #Num_BG_Pix:-float or int, the number of pixels in the background test region
    print Num_BG_Pix
    CCD_L=[] # Note: I don't even know if I need this, It's only defined here and never used again I think
    Obj_Shape="" # Note: I don't even know if I need this, It's only defined here and never used again I think
    #system('pwd')
    #system('ls')
    #system('cd ~/Desktop/Big_Object_Regions/')
    #os.chdir('~/Desktop/Big_Object_Regions/')
    dir = os.path.dirname(__file__)
    #filename= os.path.join(dir, '~','Desktop','SQL_Standard_File',)
    #filepath=os.path.abspath("~/Desktop/SQL_Standard_File")
    #print "Filepath =",filepath
    #path= os.path.join(dir,'~','Desktop','SQL_Standard_File',)
    #path=os.path.realpath('~/Desktop/SQL_Standard_File/SQL_Sandard_File.csv')
    path=os.path.realpath('../Big_Object_Regions/')
    print "Path=",path
    #system('pwd')
    os.chdir(path)
    #system('ls')
    #os.chdir("~")
    #os.system("cd ~")
    #Objfile=open("Desktop/Big_Object_Regions/"+str(objLfname),"r") #Objfile:-file, Objectfile, a file containing the regions of the X-ray objects in the observation as strings regions
    Objfile=open(str(objLfname),"r")
    #print type(Objfile)
    path2=os.path.realpath('../Background_Finder/') #Changes PWD back to this code's PWD in Desktop/Background_Finder, this may be Changed later to go to the location of the Evt2 file that will be used in the DMCOORDS, the location will be given by File_Query_Code
    os.chdir(path2)
    Objstring=Objfile.read() #Objstring:-str, Objstring, the all X-ray object regions all in one big string with each object "\n" seperated
    #print Objstring
    #print type(Objstring)
    G_Data = Ned.query_object(gname) #G_Data:-astropy.table.table.Table, Galaxy_Data, The queryed data of the galaxy from NED in the form of a astropy table
    #print G_Data
    #print type(G_Data)
    raGC=float(G_Data['RA(deg)']) #raGC:-float, Right Ascension of Galatic Center, The right ascension of the galatic center of the current galaxy in degrees.
    decGC=float(G_Data['DEC(deg)']) #decGC:-float, Declination of Galatic Center, The declination of the galatic center of the current galaxy in degrees.
    """
    Dia_A= Ned.get_table(gname,table='diameters') #Dia_A:-astropy.table.table.Table, Diameter_Array, The astropy table that contains the diameter info for the galaxy, which is referred to as an array
    #print type(Dia_A)
    #print Dia_A
    Dia_A2=Dia_A[6] #Dia_A2:-astropy.table.row.Row, Diameter Array 2, The diameter subarray using  RC3 D_0 (blue) standard for the diameter, contians the galaxy diameter infomation as an astropy row
    #print type(Dia_A2)
    #print Dia_A2
    Maj=Dia_A2[18] #Maj:-numpy.float64, Major axis, The major axis of the galaxy in arcseconds
    #print type(Maj)
    #print Maj
    #Maj=Dia_A2[18]
    Min=Dia_A2[25] #Min:-numpy.float64, Minor axis, The minor axis of the galaxy in arcseconds
    #print type(Min)
    #print Min
    S_Maj=Maj/2 #S_Maj:-numpy.float64, Semi_Major axis, The semi major axis of the galaxy in acrseconds
    """
    G_Data= Ned.query_object(gname)
    Dia_Table = Ned.get_table(gname, table='diameters')
    #print G_Data
    #print Dia_Table
    #print Dia_Table.colnames
    #print Dia_Table.meta
    #print Dia_Table.columns
    Dia_Table_Feq=Dia_Table['Frequency targeted']
    #print Dia_Table['NED Frequency']
    #print Dia_Table_Feq
    Dia_Table_Feq_L=list(Dia_Table_Feq)
    #print Dia_Table_Feq_L
    Dia_Table_Num=Dia_Table['No.']
    #print Dia_Table_Num
    Dia_Table_Num_L=list(Dia_Table_Num)
    #print Dia_Table_Num_L
    for i in range(0,len(Dia_Table_Feq_L)-1): #There is a bug here with index matching, The matched index isn't that same index for the major axis
        Cur_Feq=Dia_Table_Feq_L[i]
        #print Cur_Feq
        if(Cur_Feq=="RC3 D_25, R_25 (blue)"):
            Match_inx=i
            Match_Feq=Dia_Table_Feq_L[Match_inx]
            Match_Num=Dia_Table_Num_L[Match_inx]
            #Match_Num
            #print "Match_Feq ", Match_Feq
            #print "Match_inx ", Match_inx
            #print "Match_Num ", Match_Num
    #Dia_Table_Maj=Dia_Table['Major Axis']
    Dia_Table_Maj=Dia_Table['NED Major Axis']
    #print Dia_Table_Maj
    Dia_Table_Maj_L=list(Dia_Table_Maj)
    #print Dia_Table_Maj_L
    Dia_Table_Maj_Units=Dia_Table['Major Axis Unit']
    #print Dia_Table_Maj_Units
    Dia_Table_Maj_Units_L=list(Dia_Table_Maj_Units)
    #print Dia_Table_Maj_Units_L
    #print "i ", i
    D25_Maj=Dia_Table_Maj_L[Match_inx]
    #print "D25_Maj ", D25_Maj
    D25_Units=Dia_Table_Maj_Units[Match_inx]
    #print "D25_Units ", D25_Units
    #print type(Dia_Table)
    #print Dia_Table.info()
    #Dia_Table_2=Dia_Table[6]
    #print Dia_Table_2
    #Maj=Dia_Table_2[18]
    #print "Maj, ! ! !", Maj
    D25_S_Maj=D25_Maj/2.0
    #D25_S_Maj_Deg=D25_S_Maj/3600.0
    dmcoords(infile=str(evtfname),ra=str(raGC), dec=str(decGC), option='cel', verbose=0, celfmt='deg') # Runs the dmcoords CIAO tool, which converts coordinates like CHIP_ID to SKY, the tool is now being used to convert the RA and Dec of the GC to SKY coodinates in pixels (?)
    X_Phys=dmcoords.x #X_Phys:-float, X_Physical, The sky plane X pixel coordinate in units of pixels of the galatic center
    Y_Phys=dmcoords.y #Y_Phys:-float, Y_Physical, The sky plane Y pixel coordinate in units of pixels of the galatic center
    Chip_ID=dmcoords.chip_id #Chip_ID:-int, Chip_ID, The Chip ID number the GC is on
    print Chip_ID
    print "GC X is ", X_Phys
    print "GC Y is ", Y_Phys
    #R_Phys=S_Maj*2.03252032520325 #R_Phys:-numpy.float64, Radius_Physical, The radius of the galaxy in pixels, the converstion factor is 2.03252032520325pix/arcsec
    R_Phys=D25_S_Maj*2.03252032520325 #R_Phys:-numpy.float64, Radius_Physical, The radius of the galaxy in pixels, the converstion factor is 2.03252032520325pix/arcsec
    #D25_S_Maj
    #print type(R_Phys)
    print "Radius of Galaxy is ", R_Phys
    Gal_V_Shape='circle(' + str(X_Phys) +','+ str(Y_Phys)+','+ str(R_Phys)+')' # This might not be used at all in this code
    Objstring_L=Objstring.split("\n")
    del Objstring_L[len(Objstring_L)-1]
    #print "n ", n
    #print "Objstring_L ", Objstring_L
    #print "len(Objstring_L) ", len(Objstring_L)
    for Cur_Obj in Objstring_L:
        Obj_L.append(Cur_Obj)
    """
    for i in range(0,n):
        Cur_Obj= Objstring.split("\n")[i] #Cur_Obj:-str, Current Object, The current X-ray object region string that is being added to the Object List
        Obj_L.append(Cur_Obj) #Obj_L:-List, Object List, list of the string regions of all the X-ray objects that are in the observation
    """
    Header_String=dmlist(infile=str(evtfname),opt="header")
    #print Header_String
    Header_String_Reduced=Header_String.split("DETNAM")[1]
    #print Header_String_Reduced
    Header_String_Reduced_2=Header_String_Reduced.split("String")[0]
    #print Header_String_Reduced_2
    Header_String_Reduced_3=Header_String_Reduced_2.replace(' ', '')
    print Header_String_Reduced_3
    #dmkeypar(infile=str(evtfname), keyword="DETNAM")
    #pget(paramfile, paramname)
    #Chip_ID_String=pget(toolname="dmkeypar", parameter="value")
    #Chip_ID_String=pget("dmkeypar","value") #Chip_ID_String:-str, Chip_Idenifcation_String, Runs the pget tool to get the string containing what CCDs are used in the FOV1.fits file from the parameter file asscoiated with the dmkeypar tool and sets it equal to the Chip_ID_String (This) variable
    Chip_ID_String=Header_String_Reduced_3 #Chip_ID_String:-str, Chip_Idenifcation_String, Runs the pget tool to get the string containing what CCDs are used in the FOV1.fits file from the parameter file asscoiated with the dmkeypar tool and sets it equal to the Chip_ID_String (This) variable
    #Chip_ID_String=pget(toolname="dmkeypar", p_value="value")
    print "Chip_ID_String ", Chip_ID_String
    Chip_ID_String_L=Chip_ID_String.split('-') #Chip_ID_String_L:-List, Chip_Idenifcation_String_List, The resulting list from spliting the Chip_ID_String on "_", This list contains 2 elements, the first element is the string "ACIS" and the second element is the string segment in the form (Example) "356789" where each number in the list is its own CCD ID
    #print "Chip_ID_String_L ", Chip_ID_String_L
    Chip_ID_String_Reduced=Chip_ID_String_L[1] #Chip_ID_String_Reduced:-str, Chip_Idenifcation_String_Reduced, the string segment in the form (Example) "356789" where each number in the list is its own CCD ID
    print "Chip_ID_String_Reduced ", Chip_ID_String_Reduced
    Chip_ID_L=[] #Chip_ID_L:-List, Chip_Idenifcation_List, The list of all the int CCD IDs in FOV1.fits file
    for Cur_Chip_ID_Str in Chip_ID_String_Reduced: #Cur_Chip_ID_Str:-str, Current_Chip_Idenifcation_Str, The string vaule of the current string CCD ID in the Chip_ID_String_Reduced string, for example "3"
        Cur_Chip_ID=int(Cur_Chip_ID_Str) #Cur_Chip_ID:-int, Current_Chip_Idenifcation, The current chip ID number as an int, for example 3
        Chip_ID_L.append(Cur_Chip_ID) #Appends The current chip ID number as an int to Chip_Idenifcation_List
    print "Chip_ID_L ", Chip_ID_L
    #Step_L=[500,250,100,50,25,10,5,1]
    Step_L=[500,250,100]
    Background_L=[]
    BG_Circle_Info_L=[]
    #BG_Circle_Overlap_Bool=False
    if(len(Background_L)<=3):
        for Step in Step_L:
            #print "Step ", Step
            for Chip_ID_Test in Chip_ID_L:
                #print "Chip_ID_Test ", Chip_ID_Test
                for c in range(0+BG_R,1025-BG_R,Step):   # c is "x"  #Check Bounds #The Bounds for CHIP coordinates are (1,1024)(both included), ie range(1,1025), So if this is correct (I am not 100% sure about these CHIP bounds), "for c in range(0+BG_R,1025-BG_R):" should instead be "for c in range(1+BG_R,1025-BG_R):"
                    for v in range(0+BG_R,1025-BG_R,Step): # v is "y"  #Check Bounds, should instead be "for v in range(1+BG_R,1025-BG_R):"(?)
                        BG_Circle_Overlap_Bool=False
                        Obj_B=True #Obj_B:-bool, Object Boolean, A Boolean statement in regards to if there is no X-ray objects in the area being used to find the background
                        #print "         " # Puts a space between objects
                        BG_X=c #BG_X:-int, BackGround circle_X, The x coordinate of the backgound circle in Chip coordinates, Note: This should probably be a float along with all numerical imputs to this function
                        #print type(BG_X)
                        BG_Y=v #BG_Y:-int, BackGround circle_Y, The y coordinate of the backgound circle in Chip coordinates, Note: This should probably be a float along with all numerical imputs to this function
                        #print "Chip x is ",c
                        #print "Chip y is ",v
                        #dmcoords(infile=str(evtfname),chipx=BG_X, chipy=BG_Y, chip_id=Chip_ID, option='chip', verbose=0) # Runs the dmcoords CIAO tool, which converts coordinates like CHIP_ID to SKY, The tool is now being used to convert the Background Circle center from CHIP to SKY coordinates (?)
                        dmcoords(infile=str(evtfname),chipx=BG_X, chipy=BG_Y, chip_id=Chip_ID_Test, option='chip', verbose=0) # Runs the dmcoords CIAO tool, which converts coordinates like CHIP_ID to SKY, The tool is now being used to convert the Background Circle center from CHIP to SKY coordinates (?)
                        BG_X_Pix=dmcoords.x #BG_X_Pix:-float, BackGround circle_X_Pixels, The x of the center of the background circle in SKY coordinates in pixels
                        BG_Y_Pix=dmcoords.y #BG_Y_Pix:-float, BackGround circle_Y_Pixels, The y of the center of the background circle in SKY coordinates in pixels
                        #print "Background X is ", BG_X_Pix
                        #print "Background Y is ", BG_Y_Pix
                        #print "Background R is ", BG_R
                        Dis_GC=math.sqrt(((BG_X_Pix-X_Phys)**2)+((BG_Y_Pix-Y_Phys)**2)) #Dis_GC:-float, Distance_Galatic_Center, The distance from the background circle to the galatic center in pixels
                        #print "BG_Circle_Info_L ", BG_Circle_Info_L
                        if(len(BG_Circle_Info_L)>0): #Need to stop testing against background cirlces only on the current chip and instead on all chips
                            for BG_Circle_Info_Old in BG_Circle_Info_L:
                                BG_X_Pix_Old=BG_Circle_Info_Old[0]
                                BG_Y_Pix_Old=BG_Circle_Info_Old[1]
                                BG_R_Pix_Old=BG_Circle_Info_Old[2]
                                Dis_BG_to_BG=math.sqrt(((BG_X_Pix-BG_X_Pix_Old)**2)+((BG_Y_Pix-BG_Y_Pix_Old)**2))
                                BG_Total_Reach=Dis_BG_to_BG-BG_R-BG_R_Pix_Old
                                if(BG_Total_Reach<=0):
                                    BG_Circle_Overlap_Bool=True
                        #print type(Dis_GC)
                        #print "Distance to GC is ", Dis_GC
                        #print "R_Phys is ", R_Phys
                        #print "The GC Test is ", Dis_GC-R_Phys-BG_R
                        if((Dis_GC-R_Phys-BG_R)>0): # Makes sure that the backgound cirlce does not intersect with the radius of the galaxy, ie this functions disregards all X-ray objects in the visible extent of the galaxy
                            for Obj_S in Obj_L: #String split X, Y and the R out
                                Cur_X=Obj_S.split(",")[0] #Cur_X:-str, Current_X, The unreduced X-ray object string in the form "circle(5330.96623132" with the X coordinate in it in pixels
                                Cur_X_R=Cur_X.split('(')[1] #Cur_X_R:-str, Current_X_Reduced, The reduced X-ray object string in the form "5330.96623132" which is the X coordinate in pixels
                                Cur_Y=Obj_S.split(",")[1] #Cur_Y:-str, Current_Y_Reduced, The reduced X-ray object string in the form "5333.51369932" which is the Y coordinate in pixels
                                Cur_R=Obj_S.split(",")[2] #Cur_R:-str, Current_Radius, The unreduced X-ray object string in the form "233.272357724)" with the radius in it in pixels
                                Cur_R_R=Cur_R.split(')')[0] #Cur_R_R:-str, Current_Radius_Reduced, The reduced X-ray object string in the form "233.272357724" which is the radius in pixels
                                Cur_X_N=float(Cur_X_R) #Cur_X_N:-float, Current_X_Number, The current coordinate of the X-ray object region's X coordinate in pixels
                                Cur_Y_N=float(Cur_Y) #Cur_Y_N:-float, Current_Y_Number, The current coordinate of the X-ray object region's Y coordinate in pixels
                                Cur_R_N=float(Cur_R_R) #Cur_R_N:-float, Current_Radius_Number, The current coordinate of the X-ray object region's radius in pixels
                                Dis_Obj=math.sqrt(((BG_X_Pix-Cur_X_N)**2)+((BG_Y_Pix-Cur_Y_N)**2)) #Dis_Obj:-float, Distance_Object, The distance from the backgound cirlce to the current object
                                #print "Distance to Object is ", Dis_Obj
                                #print "Cur_R_N is ", Cur_R_N
                                #print "BG_R is ", BG_R
                                #print "The Obj Test is ", Dis_Obj-Cur_R_N-BG_R
                                if((Dis_Obj-Cur_R_N-BG_R)<=0):# Checks to see if the backgound circle contian or is touching an object
                                    Obj_B=False #Obj_B:-bool, Object_Boolean, A boolean that is false if the background cirlce is intersecting with an object region
                            #print "Obj_B ", Obj_B
                            #print "BG_Circle_Overlap_Bool ", BG_Circle_Overlap_Bool
                            if((Obj_B==True) and (BG_Circle_Overlap_Bool==False)): #Makes sure that the background circle is not intersecting with any objects or any other other background circle
                                #print "Background Found ! ! !"
                                #Dm_Out=dmlist(infile=str(evtfname)+"[sky=circle("+str(BG_X_Pix)+","+str(BG_Y_Pix)+","+str(BG_R)+")]", opt='counts', outfile="", verbose=2) #Dm_Out:-ciao_contrib.runtool.CIAOPrintableString,Dmlist_Out,Uses the Dmlist CIAO tool to find the amount of counts in the background cirlce, Note: mlist "acis_evt2.fits[sky=rotbox(4148,4044,8,22,44.5)]" counts #Need to apply energy filter (0.3kev to 10kev) to the counts, This may allow the code to treat back illuminated chips and front illuminated chips the same, if not then the code must be modifed to consider both cases
                                Dm_Out=dmlist(infile=str(evtfname)+"[sky=circle("+str(BG_X_Pix)+","+str(BG_Y_Pix)+","+str(BG_R)+"),energy=300:10000]", opt='counts', outfile="", verbose=2) #Dm_Out:-ciao_contrib.runtool.CIAOPrintableString,Dmlist_Out,Uses the Dmlist CIAO tool to find the amount of counts in the background cirlce, Note: mlist "acis_evt2.fits[sky=rotbox(4148,4044,8,22,44.5)]" counts #Energy filter (0.3kev to 10kev) has been applied to the counts, This may allow the code to treat back illuminated chips and front illuminated chips the same, if not then the code must be modifed to consider both cases
                                #print Dm_Out
                                #print type(Dm_Out)
                                Num_Counts_S=Dm_Out.split('\n')[9] #Num_Counts_S:-str, Number_of_Counts_String, The number of counts in the background cirlce as a string
                                #print Num_Counts_S
                                #print type(Num_Counts_S)
                                Num_Counts=float(Num_Counts_S) #Num_Counts:-float, Number_of_Counts, The number of counts as a float
                                BG_Ratio=Num_Counts/Num_BG_Pix #BG_Ratio:-float, Background_Ratio, The background of the observation
                                #return BG_Ratio #Returns the background of the observation
                                Background_L.append(BG_Ratio)
                                Cur_BG_Circle_Info=[BG_X_Pix,BG_Y_Pix,BG_R,Chip_ID_Test]
                                BG_Circle_Info_L.append(Cur_BG_Circle_Info)
                        if(len(Background_L)==3):
                            print "List Done ! ! ! ! ! ! ! ! !"
                            List_Done_Bool=True
                            print "Background_L ", Background_L
                            print "BG_Circle_Info_L Final", BG_Circle_Info_L
                            if(List_Done_Bool==True):
                                BG_Ratio_Avg=np.average(Background_L)
                                return BG_Ratio_Avg
    #print "List_Done_Bool ", List_Done_Bool
    #print "List_Done_Bool==False ", str(List_Done_Bool==False)
    if(List_Done_Bool==False):
        #print "List_Done_Bool==False ", str(List_Done_Bool==False)
        return "None_Found" # returns the string "None" if there is no place to put the background cirlce without intersecting the visible extent of the galaxy or an X-ray object

    #Need for figure out how to select where the test circle should be, needs to be on a CCD, (back and front Illiminated?)





#Background_Finder_3('NGC 3077','acisf02076_repro_evt2.fits','ngc3077_ObsID-2076_Source_List_R_Mod_2.txt',16,10)
#print Background_Finder_3('NGC 3077','acisf02076_repro_evt2.fits','ngc3077_ObsID-2076_Source_List_R_Mod_2.txt',10)
#print Background_Finder_3('NGC 3077','acisf02076_repro_evt2.fits','ngc3077_ObsID-2076_Source_List_R_Mod_2_Artificial.txt',10)
#print Background_Finder_3('NGC 3077','acisf02076_repro_evt2.fits','ngc3077_ObsID-2076_Source_List_R_Mod_2_Artificial.txt',420)
#print Background_Finder_3('NGC 3077','acisf02076_repro_evt2.fits','ngc3077_ObsID-2076_Source_List_R_Mod_2_Artificial.txt',435) #This will not have a suitable background
#print Background_Finder_3('NGC 3077','acisf02076_repro_evt2.fits','ngc3077_ObsID-2076_Source_List_R_Mod_2_Artificial.txt',200)
#print Background_Finder_3('NGC 3077','acisf02076_repro_evt2.fits','ngc3077_ObsID-2076_Source_List_R_Mod_2_Artificial.txt',280)
print Background_Finder_3('NGC 3077','acisf02076_repro_evt2.fits','ngc3077_ObsID-2076_Source_List_R_Mod_2_Artificial.txt',282) #This is the largest possible radius for this Artifical Big Object Region
#print Background_Finder_3('NGC 3077','acisf02076_repro_evt2.fits','ngc3077_ObsID-2076_Source_List_R_Mod_2_Artificial.txt',50)
