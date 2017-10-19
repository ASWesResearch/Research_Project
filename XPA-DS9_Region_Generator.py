import pyds9
def XPA_DS9_Region_Generator(evtfname,fovfname):
    """
    evtfname:-str, Event_Filename, The filename of the Event 2 File
    fovfname:-str, Feild_Of_View_Filename, The filename of the FOV 1 File

    This function take the Event 2 filename of the current observation and the Feild Of View filename of the current
    observation (Which are the CCD polygon regions) and opens both the evt2.fits file and the fov1.fits files in DS9 and
    saves the fov1.fits file as a text file with the regions in physical coordinates. In short this function converts the
    fov.fits files to indentical text files that can be used in the Simple_Region_Generator Code to create simple_region_no_header_modifed files
    that are used in the Area_Calc code
    """
    print(pyds9.ds9_targets())
    d = pyds9.DS9()  # will open a new ds9 window or connect to an existing on
    #81853a27:55005 #The value for the
    #d = pyds9.DS9("81853a27:55005")
    #d.set("~/asantini/Desktop/CCD_Region_Testing/evtfname")  # send the file to the open ds9 session #d.set("file /path/to/fits")  # send the file to the open ds9 session
    #d.set(str(evtfname) + "~/asantini/Desktop/CCD_Region_Testing/evtfname")
    #d.set(str(evtfname))
    #d.set(str(evtfname) + " ~/asantini/Desktop/CCD_Region_Testing/")
    #d.set("~/asantini/Desktop/CCD_Region_Testing/"+str(evtfname))
    #d.set("/home/asantini/Desktop/XPA-DS9_Region_Generator/acisf03931_repro_evt2.fits")
    #d.set("acisf03931_repro_evt2.fits")
    #d.set(acisf03931_repro_evt2.fits)
    #d.set("DS9 acisf03931_repro_evt2.fits")
    #pyds9.DS9().set("acisf03931_repro_evt2.fits")
    #d.set("acisf03931_repro_evt2.fits")
    #d.set("acisf03931_repro_evt2.fits /path/to/fits")
    d.set("file "+str(evtfname)) #Opens the Event 2file in DS9 #THIS WORKS ! ! !
    #d.get("regions acisf03931_repro_fov1.fits")
    #d.get("regions -load acisf03931_repro_fov1.fits")
    #acisf03931_repro_evt2.fits -regions acisf03931_repro_fov1.fits -regions system physical -regions save foo2 -exit
    #d.set("acisf03931_repro_evt2.fits -regions acisf03931_repro_fov1.fits -regions system physical -regions save foo2 -exit") #This only opens the fits file
    #d.get("-regions acisf03931_repro_fov1.fits")
    #d.set("-regions acisf03931_repro_fov1.fits")
    #d.set("regions acisf03931_repro_fov1.fits") #This works ! ! !
    d.set("regions " + str(fovfname)) #Loads the Feild Of View 1 file in DS9 #This Works ! ! !
    d.set("regions system physical") #This converts the region's coordinate system to physical coordinates (pixels) #This works ! ! !
    #d.set("regions save foo2") #This works ! ! !
    #CCD Regions
    fovfname_Split_L=fovfname.split('_') #fovfname_Split_L:-List, Feild_Of_View_Filename_Split_List, The resulting list of the split string regions of fovfname, The fovfname string was split on "_"
    #print "fovfname_Split_L ", fovfname_Split_L
    fovfname_reduced=fovfname_Split_L[0]+"_"+fovfname_Split_L[1] #fovfname_reduced:-str, Feild_Of_View_Filename_Reduced, The Feild_Of_View_Filename without the "_fov1.fits" part, for example the fovfname_reduced of the fovfname "acisf03931_repro_fov1.fits" is "acisf03931_repro"
    #print "fovfname_reduced ", fovfname_reduced
    #print fovfname_reduced
    d.set("regions save "+str(fovfname_reduced)+"_CCD_Regions") #Saves the FOV1.fits file as a text file in physical coordinates with the filename in the form of str(fovfname_reduced)+"_CCD_Regions", for example for "acisf03931_repro_fov1.fits" the output file name is "acisf03931_repro_CCD_Regions"
    d.set("exit") #Exits DS9 #This Works ! ! !
    #d.set('quit') #I think this does the exact same thing as d.set("exit"), I don't know if this is necessary, but I CAN'T be used when d.set("exit") is on the line above it #This Works ! ! !
XPA_DS9_Region_Generator("acisf03931_repro_evt2.fits","acisf03931_repro_fov1.fits")
#XPA_DS9_Region_Generator("acisf13830_repro_evt2.fits","acisf13830_repro_fov1.fits")
