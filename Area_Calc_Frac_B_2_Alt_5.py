from ciao_contrib.runtool import *
from region import *
#from paramio import *
from astroquery.ned import Ned
import numpy as np
#import subprocess
#subprocess.call("pset dmkeypar mode='hl'")
def Area_Calc_Frac_B_2_Alt_2(gname,evtfname,polyfname,rchange=121.9512195,B=1): #NEED to finish this code, Check to see if the radius is increaing correctly and write outputs to a file
    """
    gname:-str, Galaxy Name, The name of the galaxy in the form NGC #, For Example 'NGC 3077'
    evtfname:-str, Event File Name, The name of the event file of the observation, For Example 'acisf02076_repro_evt2.fits'
    ployfname:-str, PolyFileName, The filename of the simple_region_modifed file as a string
    rchange:-int(float?), Radius Change, The change in radius from one area cirlce to another area cirlce in pixels, must equal one arcminute in pixels
    B:-int, Binning, The binning on the regArea CIAO tool, It's standard value is 1 pixel
    """
    inner_r=0.0 #inner_r:-float, Inner_Radius, The radius of the inner most circle
    #outer_r_gap=25.0 #outer_r_gap:-float, Outer_Radius_Gap, The addtional distance that needs to be added to the outer radius inorder to account for dithering #The addtional distance that needs to be added to the outer radius inorder to account for dithering
    outer_r_gap=40.0 #outer_r_gap:-float, Outer_Radius_Gap, The addtional distance that needs to be added to the outer radius inorder to account for dithering #The addtional distance that needs to be added to the outer radius inorder to account for dithering
    cur_r=inner_r #cur_r:-float?, Current_Radius, The current radius of the area circle in pixels
    n=1 #n:-int, n, the radius change multiplier, ie the the maximum n is the number of times the radius increases
    a_tot=0.0 #a_tot:-float, Area_Total, The total intersecting area of all the CCDs currently intersecting with the area circle
    a_L=[] #a_L:-list, Area_List, The list of Area Ratios for each n
    Evtfname_Reduced=evtfname.split(".")[0] #Evtfname_Reduced:-str, Event_Filename_Reduced, The filename of the event 2 file of the observation without the extention ".fits" at the end, for example "acisf02076_repro_evt2"
    Output_File=open(str(gname)+"_"+Evtfname_Reduced+"_Area_List.txt","w") #Output_File:-file, Output_File, The Area_List file, which is the file were the list of Area_Ratios one for each circle (ie. each n) are saved, in the form of one line per ratio
    polystring_L=[] #polystring_L:-list, Polygon String List, A list of all the CCD shape strings
    polyfile=open("/home/asantini/Desktop/Polygons/"+str(polyfname),"r") #polyfile:-file, Polyfile, The polygon file that has the CCD shape strings in it
    #print type(polyfile)
    #print polyfile
    G_Data = Ned.query_object(gname) #G_Data:-astropy.table.table.Table, Galaxy_Data, The queryed data of the galaxy from NED in the form of a astropy table
    #print G_Data
    #print type(G_Data)
    raGC=float(G_Data['RA(deg)']) #raGC:-float, Right Ascension of Galatic Center, The right ascension of the galatic center of the current galaxy in degrees.
    decGC=float(G_Data['DEC(deg)']) #decGC:-float, Declination of Galatic Center, The declination of the galatic center of the current galaxy in degrees.
    dmcoords(infile=str(evtfname),ra=str(raGC), dec=str(decGC), option='cel', verbose=0, celfmt='deg') # Runs the dmcoords CIAO tool, which converts coordinates like CHIP_ID to SKY, the tool is now being used to convert the RA and Dec of the GC to SKY coodinates in pixels (?)
    X_Phys=dmcoords.x #X_Phys:-float, X_Physical, The sky plane X pixel coordinate in units of pixels of the galatic center
    Y_Phys=dmcoords.y #Y_Phys:-float, Y_Physical, The sky plane Y pixel coordinate in units of pixels of the galatic center
    Chip_ID=dmcoords.chip_id #Chip_ID:-int, Chip_ID, The Chip ID number the GC is on
    print "X_Phys ", X_Phys
    print "Y_Phys ", Y_Phys
    #Max_Min_Chip_Coord_L=[0,1024]
    #Max_Min_Chip_Coord_L=[1,1025]
    #dmkeypar acisf03931_repro_evt2.fits "DETNAM"
    #punlearn("dmkeypar") #This wipes the dmkeypar paramiter file
    #pset("dmkeypar",'hl') #This symtax is wrong
    #pset("dmkeypar", "mode", "hl")
    #pset("dmkeypar", "infile", str(evtfname))
    #pset("dmkeypar", "keyword","DETNAM")
    """
    pars = plist("dmkeypar")
    values = {}
    for p in pars:
        values[p] = pget( "dmkeypar", p )
    print pars
    print values
    """
    #dmkeypar(infile=str(evtfname), keyword="DETNAM") #Runs the dmkeypar tool which finds the data in the FITS header asscoiated with a certain header name, in this case dmkeypar is finding the "DETNAM" header info, which is a string containing what CCDs are used in the FOV1.fits file for the observation, For example "ACIS-356789" Chip_ID_String contains the chip IDs the string segment "356789" where each number in the list is its own CCD ID
    """
    pars = plist("dmkeypar")
    values = {}
    for p in pars:
        values[p] = pget( "dmkeypar", p )
    print pars
    print values
    """
    """
    This Par of the code finds what CCD's are used in the current observation by finding a string in the "DETNAM" header in the Event 2 file 
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
    #print "Chip_ID_L ", Chip_ID_L
    """
    This part of the code finds every distance between the Galatic Center and each corner of each CCD and puts them all into a list (Dist_L), The largest distance in Dist_L is the Outer_Radius
    """
    #Max_Min_Chip_Coord_L=[0.0,1025.0] #Max_Min_Chip_Coord_L:-List, Maximum_Minimum_Chip_Coordinates_List, A list containing 2 elements the first of which is the lowest possble Chip value (X or Y) for the given Axis (in pixels) and the second is the largest possble Chip value (X or Y) for the given Axis. Since the CCDs on Chandra are square 1024 X 1024 pixel CCDs, the minimun and maximum Chip X values and Chip Y values are identical and therefore can be represented by this single list
    #Max_Min_Chip_Coord_L=[0,1025] #Max_Min_Chip_Coord_L:-List, Maximum_Minimum_Chip_Coordinates_List, A list containing 2 elements the first of which is the lowest possble Chip value (X or Y) for the given Axis (in pixels) and the second is the largest possble Chip value (X or Y) for the given Axis. Since the CCDs on Chandra are square 1024 X 1024 pixel CCDs, the minimun and maximum Chip X values and Chip Y values are identical and therefore can be represented by this single list
    Max_Min_Chip_Coord_L=[1,1024] #Max_Min_Chip_Coord_L:-List, Maximum_Minimum_Chip_Coordinates_List, A list containing 2 elements the first of which is the lowest possble Chip value (X or Y) for the given Axis (in pixels) and the second is the largest possble Chip value (X or Y) for the given Axis. Since the CCDs on Chandra are square 1024 X 1024 pixel CCDs, the minimun and maximum Chip X values and Chip Y values are identical and therefore can be represented by this single list
    #Max_Min_Chip_Coord_L=[0,1023] #Max_Min_Chip_Coord_L:-List, Maximum_Minimum_Chip_Coordinates_List, A list containing 2 elements the first of which is the lowest possble Chip value (X or Y) for the given Axis (in pixels) and the second is the largest possble Chip value (X or Y) for the given Axis. Since the CCDs on Chandra are square 1024 X 1024 pixel CCDs, the minimun and maximum Chip X values and Chip Y values are identical and therefore can be represented by this single list
    Dist_L=[] #Dist_L:-List, Distance_List, The list of every distance between the Galatic Center and each corner of each CCD
    for Chip_ID_Test in Chip_ID_L: #Chip_ID_Test:-int, Chip_Idenifcation_Test, The current test CCD were that four corners are being tested as the furthest point of the Galatic Center
        print "Chip_ID_Test ", Chip_ID_Test
        #print type(Chip_ID_Test)
        for Cur_Chip_X in Max_Min_Chip_Coord_L: #Cur_Chip_X:-float, Current_Chip_X, The chip X value of the current corner in pixels (Can be either 0.0 or 1025.0)
            #print type(Cur_Chip_X)
            for Cur_Chip_Y in Max_Min_Chip_Coord_L: #Cur_Chip_Y:-float, Current_Chip_Y, The chip Y value of the current corner in pixels (Can be either 0.0 or 1025.0)
                dmcoords(infile=str(evtfname),chipx=Cur_Chip_X, chipy=Cur_Chip_Y, chip_id=Chip_ID_Test, option='chip', verbose=0) #Runs dmcoords to convert the current CCD corner coordinates from CHIP coordinates to SKY coordinates
                #pars = plist("dmcoords")
                #values = {}
                #for p in pars:
                    #values[p] = pget( "dmcoords", p )
                #print pars
                #print values
                X_Phys_Test=dmcoords.x #X_Phys_Test:-float, X_Physical_Test, The X value current CCD corner being tested in SKY coordinates
                #print type(X_Phys_Test)
                Y_Phys_Test=dmcoords.y #Y_Phys_Test:-float, Y_Physical_Test, The Y value current CCD corner being tested in SKY coordinates
                print "Test Point CHIP ", [Cur_Chip_X,Cur_Chip_Y,Chip_ID_Test]
                print "Test Point SKY ", [X_Phys_Test,Y_Phys_Test]
                X_Phys_Diff=X_Phys-X_Phys_Test #X_Phys_Diff:-float, X_Physical_Difference, The differnce between the Galatic Center X value and the current chip corner X value
                Y_Phys_Diff=Y_Phys-Y_Phys_Test #Y_Phys_Diff:-float, Y_Physical_Difference, The differnce between the Galatic Center Y value and the current chip corner Y value
                Dist=np.sqrt(((X_Phys_Diff)**2)+((Y_Phys_Diff)**2)) #Dist:-numpy.float64, Distance, The distance between the Galatic Center and the current CCD Corner
                print "Dist ", Dist
                #print type(Dist)
                Dist_L.append(Dist) #Appends the current Distance to Distance_List
    #print "Dist_L ", Dist_L
    Dist_Max=max(Dist_L) #Dist_Max:-numpy.float64, Distance_Maximum, The distance between the Galatic Center and the furthest CCD Corner
    print "Dist_Max ", Dist_Max
    #print type(Dist_Max)
    outer_r=Dist_Max+outer_r_gap #outer_r:-numpy.float64, Outer_Radius, The largest radius of the area circle, this radius should just barely inclose the all the active CCDs for the observation (All the CCDs used in the FOV1.fits file)
    print "outer_r ", outer_r
    #print type(outer_r)
    polystring=polyfile.read() #polystring:-str, Polystring, The string containing the CCD shapes strings in it seperated by "\n"
    cur_polys_L=polystring.split("\n") #cur_polys_L:-List, Current_Polygons_List, The list of all the CCD Polygons (Simple Regions) strings for the observation, Since it is split on "\n" it is in the form ['Polystring_1','Polystring_2',...'Polystring_n',''], Example, ['box(4344.13761125,3924.99595875,5253.72685384,1088.14064223,-34.6522013895)', 'box(3728.26318125,2700.00581875,1086.83938437,1086.83938437,-34.6522013895)', ''], This has an extra element on the end that is a empty string needs to be removed from the list
    #print "cur_polys_L ", cur_polys_L
    del cur_polys_L[len(cur_polys_L)-1] #This deletes the last element containing the "" from the cur_polys_L
    #print "cur_polys_L ", cur_polys_L
    """
    #This is for simple_region_no_header_modifed files
    for i in range(1,CCD_amt+1): #Splits up the polystring into the CCD shape strings
        cur_polys=polystring.split("\n")[i] #cur_polys:-str, Current Polystring, The current CCD shape string
        polystring_L.append(cur_polys) #polystring_L:-list, Polystring List, A list of all the CCD shape strings
    """
    for cur_poly in cur_polys_L: #cur_poly:-str, Current_Polygon, The Current_Polygon string in Current_Polygons_List
        polystring_L.append(cur_poly) #Appends the Current_Polygon string to polystring_L
    while((cur_r)<=outer_r): #makes sure the largest area circle used is not larger then the outer radius outer_r
        cur_r=(n*rchange) + inner_r #increases the current radius by n times the change in radius
        shape1 ='circle(' + str(X_Phys) +','+ str(Y_Phys)+','+ str(cur_r)+')' #shape1:-str, shape1, The shape string of the current area circle
        r1 = regParse(shape1) #r1:-Region, Region 1, the region of the current area circle
        a_tot=0.0 #a_tot:-float, Area_Total, The total intersecting area of all the CCDs currently intersecting with the area circle
        a1_cur = regArea(r1,0,0,8192,8192,B) #a1_cur:-float, Area_1_Current, The area of the current area circle
        for s in polystring_L: #s:-str, String, the current CCD string
            shape2 =s #Renames "s" to "shape2"
            r2 = regParse(shape2) #r2:-region, Region 2, The region of the current CCD
            r3 = regParse(shape2 + "-" + shape1) #r3:-region, Region 3, The region of the current area circle that is NOT on the CCD
            cur_a= regArea(r2,0,0,8192,8192,B) - regArea(r3,0,0,8192,8192,B) #cur_a:-float, Current_Area, The area of the current CCD that is intersecting with the area circle (?)
            #print "Current Area is ", cur_a
            a_tot=a_tot+cur_a #Adds the intersecting area of the current CCD polygon to the total intersecting area of all previous the CCD polygons for the current radius (cur_r)
            #print "Area Total is ", a_tot
            #print ""
        #print "a_tot ", a_tot #When the previous area total is equal to the current area total the previous radius is greater then or equal to the maximum radius, this could be used to tell the code when to stop
        a_ratio=float(a_tot)/float(a1_cur) # a_ratio:-float, Area_Ratio, The ratio of the total intersecting area on the total area of the current area circle
        #print "Area Ratio is ", a_ratio
        a_L.append(a_ratio) #a_L:-list, Area_List, The list of Area Ratios for each n
        n=n+1 # Itterates n
        cur_r=(n*rchange) + inner_r #Increases the current radius by n times the change in radius
    for Current_Ratio in a_L: #Current_Ratio:-float, Current_Ratio, The Current_Ratio of the total intersecting area on the total area of the current area circle in a_L
        #print type(Current_Ratio)
        Current_Ratio_Str=str(Current_Ratio) #Current_Ratio_Str:-Str, Current_Ratio_String, The Current_Ratio as a string value
        Current_Ratio_Str_New_Line=Current_Ratio_Str+"\n" #Current_Ratio_Str_New_Line:-str, Current_Ratio_String_New_Line, The Current_Ratio_String with a "\n" at the end of the string to make sure that each line in the output file contains only one Area_Ratio
        Output_File.write(Current_Ratio_Str_New_Line) #Writes the Current_Ratio_String_New_Line to the Output_File
    return a_L #Returns the Area List #May not be nessary

#print Area_Calc_Frac_B_2_Alt_2("NGC 253","acisf03931_repro_evt2.fits","acisf03931_repro_CCD_Regions_simple_region_no_header_modifed.txt",0,120,3000,2,1)
#print Area_Calc_Frac_B_2_Alt_2("NGC 253","acisf03931_repro_evt2.fits","acisf03931_repro_CCD_Regions_simple_region_modifed_Code.txt",0,120,3000)
print Area_Calc_Frac_B_2_Alt_2("NGC 253","acisf03931_repro_evt2.fits","acisf03931_repro_CCD_Regions_simple_region_modifed_Code.txt")
#print Area_Calc_Frac_B_2_Alt_2("NGC 253","acisf13830_repro_evt2.fits","acisf13830_Unconnnected_simple_region_modifed_Code.txt") #This does not work, The polyfname needs to be a real observation
#print Area_Calc_Frac_B_2_Alt_2("NGC 253","acisf13830_repro_evt2.fits","acisf13830_repro_CCD_Regions_simple_region_modifed_Code.txt")
