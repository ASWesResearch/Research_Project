from astropy.io import ascii
import os
from os import system
def File_Query(Gname,File_Type_Str,Extension=".fits"): #Still bugs, Bug:(UnboundLocalError: local variable 'File_Path_With_Filename_Str' referenced before assignment), Update(I fixed this bug, but I need to bug check more)
    File_Path_With_Filename_Str="Some Filepath"
    dir = os.path.dirname(__file__)
    path=os.path.realpath('../SQL_Standard_File/SQL_Sandard_File.csv')
    print "Path=",path
    data = ascii.read(path)
    #data = ascii.read("/home/asantini/Desktop/SQL_Standard_File/SQL_Sandard_File.csv") #data:-astropy.table.table.Table, data, The data from the SQL_Standard_File
    #print data
    #print type(data)
    #Standard_File=open("/home/asantini/Desktop/SQL_Standard_File/SQL_Sandard_File.csv","r")
    #print Standard_File
    Obs_ID_A=data["obsid"] #Obs_ID_A:-astropy.table.column.Column, Observation_Idenification_Array, The array containing all Observation IDs in the SQL_Standard_File (not indexable)
    #print type(Obs_ID_A)
    Obs_ID_L=list(Obs_ID_A) #Obs_ID_L:-List, Observation_Idenification_List, The list containing all Observation IDs in the SQL_Standard_File (So it is indexable)
    #print "Obs_ID_L ", Obs_ID_L
    #print type(Obs_ID_L)
    #print Obs_ID_A
    #FGname_A=data["foundName"]
    #FGname_L=list(FGname_A)
    #print FGname_A
    QGname_A=data["queriedName"] #QGname_A:-Obs_ID_A:-astropy.table.column.Column, Query_Galaxy_Name_Array, The array containing all Query Galaxy Names in the SQL_Standard_File (not indexable)
    QGname_L=list(QGname_A) #QGname_L:-List, Query_Galaxy_Name_Array, The list containing all Query Galaxy Names in the SQL_Standard_File (So it is indexable)
    #print type(QGname_A)
    #print QGname_A
    Matching_Index_List=[] #Matching_Index_List:-List, Matching_Index_List, The list of all indexes (ref. QGname_L) that corresepond to the input Galaxy Name, All arrays are of equal lenth, and "ith" value of an array is the correseponding value for any other arrays "ith" value, so for example Obs_ID_L[228]=794 and the Galaxy in the Observation is QGname_L[228]="NGC 891", Note both lists have the same index
    for i in range(0,len(QGname_L)): # i:-int, i, the "ith" index of QGname_L
        #print "i ", i
        QGname=QGname_L[i] #QGname:-string, Query_Galaxy_Name, The current test Galaxy Name, if this Galaxy name equals the input Galaxy Name (Gname) then this Matching_Index, i (ref. QGname_L) will be appended to the Matching_Index_List
        #QGname_Reduced=QGname.replace(" ", "")
        #print "QGname ", QGname
        #print "QGname_Reduced ", QGname_Reduced
        if(Gname==QGname): #Checks to see if the current test Galaxy Name is the same as the input Galaxy Name, if so it appends the current index (ref. QGname_L) to the Matching_Index_List
            #print "i ", i
            Matching_Index_List.append(i) #Appends the current index (ref. QGname_L) to the Matching_Index_List
    Matching_Obs_ID_L=[] #Matching_Obs_ID_L:-List, Matching_Observation_Idenification_List, The list of all Observation IDs for the current input Galaxy Name
    for Cur_Matching_Index in Matching_Index_List: #Cur_Matching_Index:-int, Current_Matching_Index, The current index (ref. QGname_L) in the list of matching indexes for the current input Galaxy Name (Matching_Index_List)
        Cur_Matching_Obs_ID=Obs_ID_L[Cur_Matching_Index] #Cur_Matching_Obs_ID:-numpy.int64, Current_Matching_Observation_Idenification, The current Observation ID for the input Galaxy Name
        #print "type(Cur_Matching_Obs_ID) ", type(Cur_Matching_Obs_ID)
        if(Cur_Matching_Obs_ID not in Matching_Obs_ID_L): #Checks to see if the current Observation ID is already included in the list of Observation IDs (Matching_Obs_ID_L) for the input Galaxy Name
            Matching_Obs_ID_L.append(Cur_Matching_Obs_ID) #Appends the Current_Matching_Observation_Idenification to the Matching_Observation_Idenification_List if the Current_Matching_Observation_Idenification has not already been included
    #print "Matching_Index_List ", Matching_Index_List
    #print "Matching_Obs_ID_L ", Matching_Obs_ID_L
    for Cur_Obs_ID in Matching_Obs_ID_L: #Cur_Obs_ID:-numpy.int64, Current_Observation_Idenification, The current Observation ID in the list of all obsevation IDs for the current Galaxy Name (Matching_Obs_ID_L)
        #print "Cur_Obs_ID ", Cur_Obs_ID
        #print "type(Cur_Obs_ID) ", type(Cur_Obs_ID)
        Cur_Obs_ID_Str=str(Cur_Obs_ID) #Cur_Obs_ID_Str:-Str, Current_Observation_Idenification_String, The current Observation ID in the list of all obsevation IDs for the current Galaxy Name (Matching_Obs_ID_L) as a string
        #print "type(Cur_Obs_ID_Str) ", type(Cur_Obs_ID_Str)
        os.chdir("/Volumes/xray/simon/chandra_from_csc/") #Tells the code to consider the files in the directory that has the obsevation files that are contained in the Chandra Source Cataloge (CSC), This is as if the code changed its directory but the current directory of the code has not changed(?)
        retval = os.getcwd() #retval:-str, retval, The current working directory as a string
        #print retval
        #print "type(retval) ", type(retval)
        #print "Directory changed successfully %s" % retval  #Checks the this line and the line above it combined check what the current working directory is
        LS_Str_In_CSC= os.popen("ls").read() #LS_Str_In_CSC:-str, LS_String_In_Chandra_Source_Cataloge, The string output of "Ls"ing the filenames in the current directory (/Volumes/xray/simon/chandra_from_csc/), As if "ls" was typed in the terminal window, the filenames are all just the observations IDs here, so the filename for the observation ID 794 is just "794"
        #print "LS_Str_In_CSC ", LS_Str_In_CSC
        #print "type(LS_Str_In_CSC) ", type(LS_Str_In_CSC)
        LS_Str_In_CSC_L=LS_Str_In_CSC.split("\n") #LS_Str_In_CSC_L:-List, LS_String_In_Chandra_Source_Cataloge_List, The list of the all filenames in the current directory (/Volumes/xray/simon/chandra_from_csc/)
        #print "LS_Str_In_CSC_L ", LS_Str_In_CSC_L
        #print "type(LS_Str_In_CSC_L) ", type(LS_Str_In_CSC_L)
        Fits_Gz_Bool=False
        Found_File_Bool=False
        n=0
        while((Found_File_Bool==False) and (n<2)):
            n=n+1
            if(Cur_Obs_ID_Str in LS_Str_In_CSC_L): #Checks to see if the current observation IDs files are in the directory that contains only the observations form the Chandra Source Cataloge, if not then the code skips this part and checks the directory containing only the files for the observations outside the Chandra Sorce Cataloge
                File_Path_Str_Primary_In_CSC="/Volumes/xray/simon/chandra_from_csc/"+Cur_Obs_ID_Str+"/primary/" #File_Path_Str_Primary_In_CSC:-str, File_Path_String_Primary_In_Chandra_Source_Cataloge, The directory of the primary files of the current observation, this directory contains the evt2.fits files and the fov1.fits files amoung others, this code will only be able to get .fits and .fits.gz files
                #print "File_Path_Str_Primary_In_CSC ", File_Path_Str_Primary_In_CSC
                os.chdir(File_Path_Str_Primary_In_CSC) #Changes the directory to the directory where the primary files for the current observation are held (/Volumes/xray/simon/chandra_from_csc/"+Cur_Obs_ID_Str+"/primary/)
                retval_In_CSC = os.getcwd() #retval_In_CSC:-str, Retval_In_Chandra_Source_Catologe, The filepath of the primary directory as a string, should be identical to File_Path_Str_Primary_In_CSC except that there is not "/" at the end of the filepath
                #print "retval_In_CSC ", retval_In_CSC
                #print "type(retval) ", type(retval)
                #print "Directory changed successfully %s" % retval_In_CSC  #Checks the this line and the line above it combined check what the current working directory is
                LS_Str_In_CSC_Primary=os.popen("ls").read() #LS_Str_In_CSC_Primary:-str, LS_String_In_Chandra_Source_Cataloge_Primary, The string containing all the filenames of the files in the primary directory, As if the "ls" command was used in the terminal to list out all the files name in the primary directory
                #print "LS_Str_In_CSC_Primary ", LS_Str_In_CSC_Primary
                #print type(LS_Str_In_CSC_Primary)
                LS_Str_In_CSC_Primary_L=LS_Str_In_CSC_Primary.split("\n") #LS_Str_In_CSC_Primary_L:-List, LS_String_In_Chandra_Source_Cataloge_Primary_List, The list of all filenames in the primary file of the current observation
                #print "LS_Str_In_CSC_Primary_L ", LS_Str_In_CSC_Primary_L
                File_Type_With_Extension_Str=File_Type_Str+Extension #File_Type_With_Extension_Str:-str, File_Type_With_Extension_String, The string that contains both the File_Type (For example: evt2,fov1, ect) and the Extension (For Example: .fits, .reg, ect), in the form File_Type_Str+Extension, for example "evt2.fits"
                #print "File_Type_With_Extension_Str ", File_Type_With_Extension_Str
                if(Fits_Gz_Bool==True): #Checks to see if the code is now looking form ".gz" compressed files
                    File_Type_With_Extension_Str=File_Type_Str+Extension+".gz" #Adds ".gz" to the File_Type_With_Extension_String so the code trys to find ".gz" compressed files, An example of the File_Type_With_Extension_String with ".gz" added to the end of it is: "fov1.fits.gz" instead of the uncompressed, "fov1.fits"
                for Fname_Str_In_CSC in LS_Str_In_CSC_Primary_L: #Fname_Str_In_CSC:-str, Filename_String_In_Chandra_Source_Cataloge, The current filename in the primary directory of the current observation ID, for example "acisf00794N003_evt2.fits"
                    #print "Fname_Str_In_CSC ", Fname_Str_In_CSC
                    Fname_Str_In_CSC_L=Fname_Str_In_CSC.split("_") #Fname_Str_In_CSC_L:-List, Filename_String_In_Chandra_Source_Cataloge_L, Splits the current filename on "_", seperating the "name" of the file and the test File_Type_With_Extension_Str, for example ['acisf00794N003', 'evt2.fits']
                    #print "Fname_Str_In_CSC_L ", Fname_Str_In_CSC_L
                    File_Type_With_Extension_Str_Test=Fname_Str_In_CSC_L[len(Fname_Str_In_CSC_L)-1] #File_Type_With_Extension_Str_Test:-str, File_Type_With_Extension_String_Test, The test File_Type_With_Extension_String, if the File_Type_With_Extension_Str_Test equals the File_Type_With_Extension_Str then a matching file has been found and the current test filename (Fname_Str_In_CSC) is added to the list of filenames for this Galaxy Name
                    #print "File_Type_With_Extension_Str ", File_Type_With_Extension_Str
                    #print "File_Type_With_Extension_Str ", type(File_Type_With_Extension_Str)
                    #print "File_Type_With_Extension_Str_Test ", File_Type_With_Extension_Str_Test
                    #print "type(File_Type_With_Extension_Str_Test) ", File_Type_With_Extension_Str_Test
                    if(File_Type_With_Extension_Str==File_Type_With_Extension_Str_Test): #Checks to see if the current test filenames is the inputed file type with the inputed Extension
                        Filename_String=Fname_Str_In_CSC #Filename_String:-str, Filename_String, The filename of the matching file, ie the filename that the code is looking for
                        File_Path_With_Filename_Str=File_Path_Str_Primary_In_CSC+Filename_String #File_Path_With_Filename_Str:-str, File_Path_With_Filename_String, The filepath to the matching file, for example: "/Volumes/xray/simon/chandra_from_csc/794/primary/acisf00794N003_evt2.fits"
                        Found_File_Bool=True #Sets Found_File_Bool=True to indcate that the file has been found
                        print "Found the File (IN) ! ! !"
            os.chdir("/Volumes/xray/simon/chandra_not_csc/") #Tells the code to consider the files in the directory that has the obsevation files that are NOT contained in the Chandra Source Cataloge (CSC), This is as if the code changed its directory but the current directory of the code has not changed(?)
            retval = os.getcwd() #retval:-str, retval, The current working directory as a string
            #print "type(retval) ", type(retval)
            #print "Directory changed successfully %s" % retval  #Checks the this line and the line above it combined check what the current working directory is
            LS_Str_Not_CSC= os.popen("ls").read() #LS_Str_NOT_CSC:-str, LS_String_NOT_in_Chandra_Source_Cataloge, The string output of "Ls"ing the filenames in the current directory (/Volumes/xray/simon/chandra_not_csc/), As if "ls" was typed in the terminal window, the filenames are all just the observations IDs here, so the filename for the observation ID 10125 is just "10125"
            #print "LS_Str_Not_CSC ", LS_Str_Not_CSC
            #print "type(LS_Str_Not_CSC) ", type(LS_Str_Not_CSC)
            LS_Str_Not_CSC_L=LS_Str_Not_CSC.split("\n") #LS_Str_Not_CSC_L:-List, LS_String_Not_in_Chandra_Source_Cataloge_List, The list of the all filenames in the current directory (/Volumes/xray/simon/chandra_not_csc/)
            #print "LS_Str_Not_CSC_L ", LS_Str_Not_CSC_L
            if(Cur_Obs_ID_Str in LS_Str_Not_CSC_L): #Checks to see if the current observation IDs files are in the directory that contains only the observations Not in the Chandra Source Cataloge, if not then the code skips this part
                #print "Not in CSC"
                File_Path_Str_Primary_Not_CSC="/Volumes/xray/simon/chandra_not_csc/"+Cur_Obs_ID_Str+"/primary/"
                os.chdir(File_Path_Str_Primary_Not_CSC) #Changes the directory to the directory where the primary files for the current observation are held (/Volumes/xray/simon/chandra_not_csc/"+Cur_Obs_ID_Str+"/primary/)
                retval_Not_CSC = os.getcwd() #retval_Not_CSC:-str, Retval_Not_Chandra_Source_Catologe, The filepath of the primary directory as a string, should be identical to File_Path_Str_Primary_Not_CSC except that there is not "/" at the end of the filepath
                #print "type(retval) ", type(retval)
                #print "Directory changed successfully %s" % retval_Not_CSC  #Checks the this line and the line above it combined check what the current working directory is
                LS_Str_Not_CSC_Primary=os.popen("ls").read() #LS_Str_Not_CSC_Primary:-str, LS_String_Not_in_Chandra_Source_Cataloge_Primary, The string containing all the filenames of the files in the primary directory, As if the "ls" command was used in the terminal to list out all the files name in the primary directory
                #print "LS_Str_Not_CSC_Primary ", LS_Str_Not_CSC_Primary
                LS_Str_Not_CSC_Primary_L=LS_Str_Not_CSC_Primary.split("\n") #LS_Str_Not_in_CSC_Primary_L:-List, LS_String_Not_in_Chandra_Source_Cataloge_Primary_List, The list of all filenames in the primary file of the current observation
                #print "LS_Str_Not_CSC_Primary_L ", LS_Str_Not_CSC_Primary_L
                File_Type_With_Extension_Str=File_Type_Str+Extension #File_Type_With_Extension_Str:-str, File_Type_With_Extension_String, The string that contains both the File_Type (For example: evt2,fov1, ect) and the Extension (For Example: .fits, .reg, ect), in the form File_Type_Str+Extension, for example "evt2.fits"
                if(Fits_Gz_Bool==True): #Checks to see if the code is now looking form ".gz" compressed files
                    File_Type_With_Extension_Str=File_Type_Str+Extension+".gz" #Adds ".gz" to the File_Type_With_Extension_String so the code trys to find ".gz" compressed files, An example of the File_Type_With_Extension_String with ".gz" added to the end of it is: "fov1.fits.gz" instead of the uncompressed, "fov1.fits"
                #print "File_Type_With_Extension_Str ", File_Type_With_Extension_Str
                for Fname_Str_Not_CSC in LS_Str_Not_CSC_Primary_L: #Fname_Str_Not_in_CSC:-str, Filename_String_Not_in_Chandra_Source_Cataloge, The current filename in the primary directory of the current observation ID, for example "acisf10125N002_evt2.fits"
                    Fname_Str_Not_CSC_L=Fname_Str_Not_CSC.split("_") #Fname_Str_In_CSC_L:-List, Filename_String_In_Chandra_Source_Cataloge_L, Splits the current filename on "_", seperating the "name" of the file and the test File_Type_With_Extension_Str, for example ['acisf10125N002', 'evt2.fits']
                    #print "Fname_Str_Not_CSC_L ", Fname_Str_Not_CSC_L
                    File_Type_With_Extension_Str_Test=Fname_Str_Not_CSC_L[len(Fname_Str_Not_CSC_L)-1] #File_Type_With_Extension_Str_Test:-str, File_Type_With_Extension_String_Test, The test File_Type_With_Extension_String, if the File_Type_With_Extension_Str_Test equals the File_Type_With_Extension_Str then a matching file has been found and the current test filename (Fname_Str_In_CSC) is added to the list of filenames for this Galaxy Name
                    #print "File_Type_With_Extension_Str ", File_Type_With_Extension_Str
                    #print "File_Type_With_Extension_Str ", type(File_Type_With_Extension_Str)
                    #print "File_Type_With_Extension_Str_Test ", File_Type_With_Extension_Str_Test
                    #print "type(File_Type_With_Extension_Str_Test) ", File_Type_With_Extension_Str_Test
                    if(File_Type_With_Extension_Str==File_Type_With_Extension_Str_Test): #Checks to see if the current test filenames is the inputed file type with the inputed Extension
                        Filename_String=Fname_Str_Not_CSC #Filename_String:-str, Filename_String, The filename of the matching file, ie the filename that the code is looking for
                        File_Path_With_Filename_Str=File_Path_Str_Primary_Not_CSC+Filename_String #File_Path_With_Filename_Str:-str, File_Path_With_Filename_String, The filepath to the matching file, for example: "/Volumes/xray/simon/chandra_from_csc/794/primary/acisf00794N003_evt2.fits"
                        Found_File_Bool=True #Sets Found_File_Bool=True to indcate that the file has been found
                        print "Found the File (NOT) ! ! !"
            if(Found_File_Bool==False): #Checks to see if an uncompressed file was found, if not it sets Fits_Gz_Bool=True so the code starts checking for ".gz" compressed files
                Fits_Gz_Bool=True #Sets Fits_Gz_Bool=True so the code starts checking for ".gz" compressed files
                "Finding compressed"
        #print "Filename_String ", Filename_String
        print "File_Path_With_Filename_Str ", File_Path_With_Filename_Str
        return File_Path_With_Filename_Str



File_Query("NGC 891","evt2") #In in CSC
#File_Query("NGC 6946","evt2") #In CSC
#File_Query("NGC 891","fov1") #In in CSC
#File_Query("NGC 891","reg",".reg") #In in CSC
#File_Query("NGC 6946","fov1") #In CSC
#File_Query("NGC 4449","evt2") # Not CSC
#File_Query("NGC 4449","fov1") #Not CSC
#File_Query("NGC 4449","reg",".reg") #NOT CSC
