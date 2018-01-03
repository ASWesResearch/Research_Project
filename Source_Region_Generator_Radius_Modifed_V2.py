from astropy.io import ascii
import os
import pyregion
def Source_Region_Generator_Radius_Modifed_V2(Gname,M=10):
        """
        Gname:-str, Galaxy Name, The name of the galaxy in the form NGC #, For Example 'NGC 3077'
        M:-int, Multiplier, The amount the radius of the X-ray source regions will be multiplied to from the modifed regions

        This code takes the name of the galaxy and the X-ray source region multiplier and creates a modifed region file containing the
        regions of the X-ray sources modifed by multiplying their radii.
        While this code has been documented assuming that the galaxies in CSC and Not in CSC were all in the same file, it turns out they are in one file called trace
        which contians all the obsIDs (all obsIDs for the study?, most likely yes, All)
        """
        #data = ascii.read("/home/asantini/Desktop/SQL_Standard_File/SQL_Sandard_File.csv") #data:-astropy.table.table.Table, data, The data from the SQL_Standard_File
        dir = os.path.dirname(__file__)
        path=os.path.realpath('../SQL_Standard_File/SQL_Sandard_File.csv')
        print "Path=",path
        #system('pwd')
        data = ascii.read(path) #data:-astropy.table.table.Table, data, The data from the SQL_Standard_File
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
            os.chdir("/Volumes/xray/spirals/trace/") #Tells the code to consider the files in the directory that has the obsevation files that are contained in the Chandra Source Cataloge (CSC), This is as if the code changed its directory but the current directory of the code has not changed(?)
            retval = os.getcwd() #retval:-str, retval, The current working directory as a string
            #print retval
            #print "type(retval) ", type(retval)
            #print "Directory changed successfully %s" % retval  #Checks the this line and the line above it combined check what the current working directory is
            LS_Str= os.popen("ls").read() #LS_Str:-str, LS_String, The string output of "Ls"ing the filenames in the current directory (/Volumes/xray/spirals/trace/), As if "ls" was typed in the terminal window, the filenames are all just the observations IDs here, so the filename for the observation ID 794 is just "794"
            #print "LS_Str ", LS_Str
            #print "type(LS_Str) ", type(LS_Str)
            LS_Str_L=LS_Str.split("\n") #LS_Str_L:-List, LS_String_List, The list of the all filenames in the current directory (/Volumes/xray/spirals/trace/)
            #print "LS_Str_L ", LS_Str_L
            #print "type(LS_Str_L) ", type(LS_Str_L)
            if(Cur_Obs_ID_Str in LS_Str_L): #Checks to see if the current observation IDs files are in the directory that contains only the observations form the Chandra Source Cataloge, if not then the code skips this part and checks the directory containing only the files for the observations outside the Chandra Sorce Cataloge
                print "Cur_Obs_ID_Str ", Cur_Obs_ID_Str
                File_Path_Str_Main="/Volumes/xray/spirals/trace/"+Cur_Obs_ID_Str #File_Path_Str_Main:-str, File_Path_String_Main, The directory of the Main files of the current observation, this directory contains the wavdetect region (.reg) files amoung others
                #print "File_Path_Str_Main ", File_Path_Str_Main
                os.chdir(File_Path_Str_Main) #Changes the directory to the directory where the Main files for the current observation are held (/Volumes/xray/spirals/trace/"+Cur_Obs_ID_Str)
                retval_2 = os.getcwd() #retval_2:-str, Retval_In_Chandra_Source_Catologe, The filepath of the Main directory as a string, should be identical to File_Path_Str_Main except that there is not "/" at the end of the filepath
                #print "retval_In_CSC ", retval_In_CSC
                #print "type(retval) ", type(retval)
                #print "Directory changed successfully %s" % retval_In_CSC  #Checks the this line and the line above it combined check what the current working directory is
                LS_Str_Main=os.popen("ls").read() #LS_Str_Main:-str, LS_String_In_Chandra_Source_Cataloge_Main, The string containing all the filenames of the files in the Main directory, As if the "ls" command was used in the terminal to list out all the files name in the Main directory
                #print "LS_Str_Main ", LS_Str_Main
                #print type(LS_Str_Main)
                LS_Str_Main_L=LS_Str_Main.split("\n") #LS_Str_Main_L:-List, LS_String_In_Chandra_Source_Cataloge_Main_List, The list of all filenames in the Main file of the current observation
                #print "LS_Str_Main_L ", LS_Str_Main_L
                #File_Type_With_Extension_Str=File_Type_Str+Extension #File_Type_With_Extension_Str:-str, File_Type_With_Extension_String, The string that contains both the File_Type (For example: evt2,fov1, ect) and the Extension (For Example: .fits, .reg, ect), in the form File_Type_Str+Extension, for example "evt2.fits"
                #print "File_Type_With_Extension_Str ", File_Type_With_Extension_Str
                Filtered_Fname_L=[]
                for fname in LS_Str_Main_L:
                    fname_L=fname.split(".")
                    fname_extension=fname_L[len(fname_L)-1]
                    fname_header=fname_L[0]
                    fname_header_L=fname_header.split("_")
                    #print "len(fname_header_L) ", len(fname_header_L)
                    if((len(fname_L)<=2) and (fname_extension=="reg") and (len(fname_header_L)==1)):
                        fname_filtered=fname
                        #print "filtered fname ", fname_filtered
                        Filtered_Fname_L.append(fname_filtered)
                #print "Filtered_Fname_L ", Filtered_Fname_L
                Filtered_Fname_L_Ordered=[]
                Source_Num_List=[]
                for Source_Num in range(1,len(Filtered_Fname_L)+1):
                    #print "Source_Num ", Source_Num
                    for Filtered_Fname in Filtered_Fname_L:
                        Filtered_Fname_Str_L=Filtered_Fname.split(".")
                        Filtered_Fname_Header=Filtered_Fname_Str_L[0]
                        Filtered_Fname_Extension=Filtered_Fname_Str_L[len(Filtered_Fname_Str_L)-1]
                        Filtered_Fname_Header_Int=int(Filtered_Fname_Header)
                        if(Source_Num==Filtered_Fname_Header_Int):
                            Filtered_Fname_L_Ordered.append(Filtered_Fname)
                #print "Filtered_Fname_L_Ordered ", Filtered_Fname_L_Ordered
                """
                Source_Region_Tables_Filepath="/home/asantini/Desktop/Source_Region_Tables/"
                os.chdir(Source_Region_Tables_Filepath)
                Region_fname=Gname+"_"+Cur_Obs_ID_Str+"_Source_Region_Radius_Modifed_Table.csv"
                file=open(Region_fname,"w")
                #file.write("X"+","+"Y"+","+"Maj_Ax"+","+"Min_Ax"+","+"Angle")
                file.write("X"+","+"Y"+","+"Maj_Ax")
                """
                Shape_String_List=[]
                for Reg_Fname in Filtered_Fname_L_Ordered:
                    Cur_Reg_Data_L=pyregion.open(Reg_Fname)
                    #print "Cur_Reg_Data_L ", Cur_Reg_Data_L
                    Cur_Reg_Data=Cur_Reg_Data_L[0]
                    #print "Cur_Reg_Data ", Cur_Reg_Data
                    Cur_Reg_Coords=Cur_Reg_Data.coord_list
                    #print "Cur_Reg_Coords ", Cur_Reg_Coords
                    X=Cur_Reg_Coords[0]
                    #print "X ", X
                    #print type(X)
                    Y=Cur_Reg_Coords[1]
                    #print "Y ", Y
                    Maj_Ax=Cur_Reg_Coords[2]
                    #print "Maj_Ax ", Maj_Ax
                    Cur_Shape='circle('+str(X)+','+str(Y)+','+str(Maj_Ax * M) + ')' + '\n' #Cur_Shape:-str, Current_Shape, The big region (called a shape) of the current X-ray object, 'Big' refers to the multiplied radius
                    Shape_String_List.append(Cur_Shape)
                #Source_Region_Tables_Filepath="/home/asantini/Desktop/Source_Region_Tables/"
                #system('pwd')
                cwd = os.getcwd()
                print cwd
                #Source_Region_Tables_Filepath=os.path.realpath('../../../../vvodata/home/asantini/Desktop/Source_Region_Tables/')
                #Source_Region_Tables_Filepath=path=os.path.realpath('~')
                Source_Region_Tables_Filepath='/Network/Servers/vimes.astro.wesleyan.edu/Volumes/vvodata/home/asantini/Desktop/Source_Region_Tables' #Need to use relitive path intead but will not work since it goes to Volumes
                os.chdir(Source_Region_Tables_Filepath)
                cwd = os.getcwd()
                print cwd
                Gname_Underscore=Gname.replace(Gname[3], "_", 1)
                Region_fname=Gname_Underscore+"_"+"ObsID_"+Cur_Obs_ID_Str+"_Source_Regions_Radius_Modifed.txt"
                file=open(Region_fname,"w")
                #file.write("X"+","+"Y"+","+"Maj_Ax"+","+"Min_Ax"+","+"Angle")
                #file.write("X"+","+"Y"+","+"Maj_Ax")
                for Shape_String in Shape_String_List:
                    file.write(Shape_String)









Source_Region_Generator_Radius_Modifed_V2("NGC 891")
