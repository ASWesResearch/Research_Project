import astropy.io.ascii as ascii
import tarfile
import numpy as np
import math
import matplotlib.pyplot as plt
import os
from os import system
from astropy.io import fits
from astroquery.ned import Ned

def Area_GC_R_N_F_2(Gname):
    """
    Gname: str- The name of the galaxy in the form NGC #
    Data: array- a table of data containg the coordinates of each object

    This fucntion takes the inputs for the name of the galaxy and returns a histrogram that plots the number of objects per bin by the
    area enclosed by the cirlce centered on the center of the galaxy that inculdes the objects in each bin in
    square degrees divided by the visible area of the galaxy in square degrees.
    This function plots the visible Major axis of the galaxy area enclosed by a circle that uses the Major axis as
    the diameter of the cirlce divided by itself to give 1 on histogram.
    This function uses astroquary to get data directly from NED

    #THIS IS THE CURRENT RUNNING VERSION OF THIS CODE
    """
    import math
    from astropy.io import ascii
    import matplotlib.pyplot as plt
    #system('pwd')
    #system('cd ~/Desktop/SQL_Standard_File/')
    #import os
    dir = os.path.dirname(__file__)
    #filename= os.path.join(dir, '~','Desktop','SQL_Standard_File',)
    #filepath=os.path.abspath("~/Desktop/SQL_Standard_File")
    #print "Filepath =",filepath
    #path= os.path.join(dir,'~','Desktop','SQL_Standard_File',)
    #path=os.path.realpath('~/Desktop/SQL_Standard_File/SQL_Sandard_File.csv')
    path=os.path.realpath('../SQL_Standard_File/SQL_Sandard_File.csv')
    #print "Path=",path
    #os.chdir(path)
    #os.chdir('~/Desktop/SQL_Standard_File/')
    #system('cd ~/Desktop/Big_Object_Regions/')
    #system('cd ../SQL_Standard_File/')
    system('pwd')
    #system('ls')
    #data = ascii.read("SQL_Sandard_File.csv") #data:-astropy.table.table.Table, data, The data from the SQL_Standard_File
    #data = ascii.read(filename) #data:-astropy.table.table.Table, data, The data from the SQL_Standard_File
    #data = ascii.read(filepath) #data:-astropy.table.table.Table, data, The data from the SQL_Standard_File
    data = ascii.read(path) #data:-astropy.table.table.Table, data, The data from the SQL_Standard_File
    #data2=open("SQL_Sandard_File.csv","r")
    #print data2
    #system('cd ~/Desktop/galaxies/out')
    RA_A=data['sourceRA'] #RA_A:-astropy.table.column.Column, Right_Ascension_Array, The array containing all Right Ascensions in the SQL Standard File
    #print type(RA_A)
    RA_L=list(RA_A) #RA_L:-list, Right_Ascension_List, The list containing all Right Ascensions in the SQL Standard File
    #print RA_L
    Dec_A=data['sourceDec'] #Dec_A:-astropy.table.column.Column, Declination_Array, The array containing all Declinations in the SQL Standard File
    Dec_L=list(Dec_A) #Dec_L:-List, Declination_List, The list containing all Declinations in the SQL Standard File
    #print Dec_L
    #Obs_ID_A=data["obsid"] #Obs_ID_A:-astropy.table.column.Column, Observation_Idenification_Array, The array containing all Observation IDs in the SQL_Standard_File (not indexable)
    #print type(Obs_ID_A)
    #Obs_ID_L=list(Obs_ID_A) #Obs_ID_L:-List, Observation_Idenification_List, The list containing all Observation IDs in the SQL_Standard_File (So it is indexable)
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
    RA_Match_L=[] #RA_Match_L:-List, Right_Ascension_Match_List, The list of all source RA's for the input Galaxy Name in decimal degrees
    Dec_Match_L=[] #Dec_Match_L:-List, Declination_Match_List, The list of all source Dec's for the input Galaxy Name in decimal degrees
    for Cur_Matching_Index in Matching_Index_List: #Cur_Matching_Index:-int, Current_Matching_Index, The current index (ref. QGname_L) in the list of matching indexes for the current input Galaxy Name (Matching_Index_List)
        Cur_Match_RA=RA_L[Cur_Matching_Index] #Cur_Match_RA:-numpy.float64, Current_Match_Right_Ascension, The RA of the current source in decimal degrees
        #print type(Cur_Match_RA)
        Cur_Match_Dec=Dec_L[Cur_Matching_Index] #Cur_Match_Dec:-numpy.float64, Current_Match_Declination, The Dec of the current source in decimal degrees
        RA_Match_L.append(Cur_Match_RA) #RA_Match_L:-list, Right_Ascension_Match_List, The list of all source RA's for the input Galaxy Name in decimal degrees
        Dec_Match_L.append(Cur_Match_Dec) #Dec_Match_L:-list, Declination_Match_List, The list of all source Dec's for the input Galaxy Name in decimal degrees
    #print RA_Match_L
    #print len(RA_Match_L)
    #print Dec_Match_L
    #print len(Dec_Match_L)
    #decA=Data['dec']
    #raA=Data['ra']
    #Maj=Maj/3600
    #S_Maj=Maj/2
    #area_T=((S_Maj)**2)*math.pi
    G_Data= Ned.query_object(Gname) #G_Data:-astropy.table.table.Table, Galaxy_Data, The Galaxy Data Table queried from NED
    #print type(G_Data)
    Dia_Table = Ned.get_table(Gname, table='diameters') #Dia_Table:-astropy.table.table.Table, Diameter_Table, The Data table queried from NED that contains the infomation about the Major Axis of the input Galaxy Name
    #print type(Dia_Table)
    #print G_Data
    #print Dia_Table
    #print Dia_Table.colnames
    #print Dia_Table.meta
    #print Dia_Table.columns
    Dia_Table_Feq=Dia_Table['Frequency targeted'] #Dia_Table_Feq:-astropy.table.column.MaskedColumn, Diameter_Table_Fequency, The Array containing all named frequencies of light that are being used for the Major Axis Measurement
    #print Dia_Table['NED Frequency']
    #print Dia_Table_Feq
    #print type(Dia_Table_Feq)
    Dia_Table_Feq_L=list(Dia_Table_Feq) #Dia_Table_Feq_L:-List, Diameter_Table_Fequency_List, The list containing all named frequencies of light that are being used for the Major Axis Measurement
    #print Dia_Table_Feq_L
    Dia_Table_Num=Dia_Table['No.'] #Dia_Table_Num:-astropy.table.column.MaskedColumn, Diameter_Table_Number, The number Ned assigns to
    #print Dia_Table_Num
    #print type(Dia_Table_Num)
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
    D25_S_Maj_Deg=D25_S_Maj/3600.0
    area_T=((D25_S_Maj_Deg)**2)*math.pi
    raGC=float(G_Data['RA(deg)'])
    decGC=float(G_Data['DEC(deg)'])
    #area_A=[((((((decGC-dec)**2)+((raGC-ra)**2)))*(math.pi))/area_T) for dec,ra in zip(decA,raA)]
    area_A=[((((((decGC-dec)**2)+((raGC-ra)**2)))*(math.pi))/area_T) for dec,ra in zip(Dec_Match_L,RA_Match_L)] #REAL ONE
    #disA=[math.sqrt(((decGC-dec)**2)+((raGC-ra)**2)) for dec,ra in zip(decA,raA)] #REAL ONE
    #print area_A
    #area_max=max(area_A)
    #print area_max
    #plt.vlines(0.00001,0,10,color='red')
    #plt.vlines(1,0,10,color='red')
    #plt.hist(area_A)
    Hist_A=plt.hist(area_A)
    Bin_Hight_A=Hist_A[0]
    Bin_Hight_Max=max(Bin_Hight_A)
    print Bin_Hight_Max
    plt.vlines(1,0,Bin_Hight_Max,color='red')
    #Hist_Max=max(area_A)
    #print "Hist_Max ", Hist_Max
    plt.plot()
    #plt.savefig('Test1.png')
    path_2=os.path.realpath('../Master_Code/Histograms/') #Goes to Histograms folder, which will hold the histogram pictures
    print "Path_2=",path_2
    os.chdir(path_2)
    #system('mkdir '+Gname) #Creates Current Galaxy's Folder, Folder Named after Galaxy, Note: will have to remove space from "NGC #" to change to "NGC_#", I Don't know if this works
    Gname_L=Gname.split(" ")
    print "Gname_L: ", Gname_L
    if(len(Gname_L)>1):
        Gname_Modifed=Gname_L[0]+"_"+Gname_L[1] #Adds underscore to remove space from "NGC #" to change to "NGC_#" if there is a space in the name
    else:
        Gname_Modifed=Gname # Does nothing if the galaxy name has no space, ie. NGC#, For example NGC253 instead of NGC 253 or NGC_253
    print Gname_Modifed
    path_3=path_2+'/'+Gname_Modifed+'/'
    directory = os.path.dirname(path_3)
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.chdir(path_3) #Goes to Current Galaxies Folder
    plt.savefig(Gname+'_Frac.png') #Saves angluar histogram figure
    #system('pwd')
    path_4=os.path.realpath('../../../GitHub/')
    print "Path_4=",path_4
    os.chdir(path_4) #Goes back to where this code (the histogram code) is being run, ie. Desktop/GitHub
    plt.close()
    #plt.show()

#Area_GC_R_N_F_2('NGC4258')

def Area_GC_R_N(Gname):
    """
    Gname: str- The name of the galaxy in the form NGC #
    Data: array- a table of data containg the coordinates of each object

    This fucntion takes the inputs for the name of the galaxy and returns a histrogram that plots the number of objects per bin by the
    area enclosed by the cirlce centered on the center of the galaxy that inculdes the objects in each bin in
    square degrees divided by the visible area of the galaxy in square degrees.
    This function plots the visible Major axis of the galaxy area enclosed by a circle that uses the Major axis as
    the diameter of the cirlce divided by itself to give 1 on histogram.
    This function uses astroquary to get data directly from NED

    #THIS IS THE CURRENT RUNNING VERSION OF THIS CODE
    """
    import math
    from astropy.io import ascii
    import matplotlib.pyplot as plt
    system('pwd')
    #system('cd ~/Desktop/SQL_Standard_File/')
    #import os
    dir = os.path.dirname(__file__)
    #filename= os.path.join(dir, '~','Desktop','SQL_Standard_File',)
    #filepath=os.path.abspath("~/Desktop/SQL_Standard_File")
    #print "Filepath =",filepath
    #path= os.path.join(dir,'~','Desktop','SQL_Standard_File',)
    #path=os.path.realpath('~/Desktop/SQL_Standard_File/SQL_Sandard_File.csv')
    path=os.path.realpath('../SQL_Standard_File/SQL_Sandard_File.csv')
    print "Path=",path
    #os.chdir(path)
    #os.chdir('~/Desktop/SQL_Standard_File/')
    #system('cd ~/Desktop/Big_Object_Regions/')
    #system('cd ../SQL_Standard_File/')
    system('pwd')
    #system('ls')
    #data = ascii.read("SQL_Sandard_File.csv") #data:-astropy.table.table.Table, data, The data from the SQL_Standard_File
    #data = ascii.read(filename) #data:-astropy.table.table.Table, data, The data from the SQL_Standard_File
    #data = ascii.read(filepath) #data:-astropy.table.table.Table, data, The data from the SQL_Standard_File
    data = ascii.read(path) #data:-astropy.table.table.Table, data, The data from the SQL_Standard_File
    #data2=open("SQL_Sandard_File.csv","r")
    #print data2
    #system('cd ~/Desktop/galaxies/out')
    RA_A=data['sourceRA'] #RA_A:-astropy.table.column.Column, Right_Ascension_Array, The array containing all Right Ascensions in the SQL Standard File
    #print type(RA_A)
    RA_L=list(RA_A) #RA_L:-list, Right_Ascension_List, The list containing all Right Ascensions in the SQL Standard File
    #print RA_L
    Dec_A=data['sourceDec'] #Dec_A:-astropy.table.column.Column, Declination_Array, The array containing all Declinations in the SQL Standard File
    Dec_L=list(Dec_A) #Dec_L:-List, Declination_List, The list containing all Declinations in the SQL Standard File
    #print Dec_L
    #Obs_ID_A=data["obsid"] #Obs_ID_A:-astropy.table.column.Column, Observation_Idenification_Array, The array containing all Observation IDs in the SQL_Standard_File (not indexable)
    #print type(Obs_ID_A)
    #Obs_ID_L=list(Obs_ID_A) #Obs_ID_L:-List, Observation_Idenification_List, The list containing all Observation IDs in the SQL_Standard_File (So it is indexable)
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
    RA_Match_L=[] #RA_Match_L:-List, Right_Ascension_Match_List, The list of all source RA's for the input Galaxy Name in decimal degrees
    Dec_Match_L=[] #Dec_Match_L:-List, Declination_Match_List, The list of all source Dec's for the input Galaxy Name in decimal degrees
    for Cur_Matching_Index in Matching_Index_List: #Cur_Matching_Index:-int, Current_Matching_Index, The current index (ref. QGname_L) in the list of matching indexes for the current input Galaxy Name (Matching_Index_List)
        Cur_Match_RA=RA_L[Cur_Matching_Index] #Cur_Match_RA:-numpy.float64, Current_Match_Right_Ascension, The RA of the current source in decimal degrees
        #print type(Cur_Match_RA)
        Cur_Match_Dec=Dec_L[Cur_Matching_Index] #Cur_Match_Dec:-numpy.float64, Current_Match_Declination, The Dec of the current source in decimal degrees
        RA_Match_L.append(Cur_Match_RA) #RA_Match_L:-list, Right_Ascension_Match_List, The list of all source RA's for the input Galaxy Name in decimal degrees
        Dec_Match_L.append(Cur_Match_Dec) #Dec_Match_L:-list, Declination_Match_List, The list of all source Dec's for the input Galaxy Name in decimal degrees
    #print RA_Match_L
    #print len(RA_Match_L)
    #print Dec_Match_L
    #print len(Dec_Match_L)
    #decA=Data['dec']
    #raA=Data['ra']
    #Maj=Maj/3600
    #S_Maj=Maj/2
    #area_T=((S_Maj)**2)*math.pi
    G_Data= Ned.query_object(Gname) #G_Data:-astropy.table.table.Table, Galaxy_Data, The Galaxy Data Table queried from NED
    #print type(G_Data)
    Dia_Table = Ned.get_table(Gname, table='diameters') #Dia_Table:-astropy.table.table.Table, Diameter_Table, The Data table queried from NED that contains the infomation about the Major Axis of the input Galaxy Name
    #print type(Dia_Table)
    #print G_Data
    #print Dia_Table
    #print Dia_Table.colnames
    #print Dia_Table.meta
    #print Dia_Table.columns
    Dia_Table_Feq=Dia_Table['Frequency targeted'] #Dia_Table_Feq:-astropy.table.column.MaskedColumn, Diameter_Table_Fequency, The Array containing all named frequencies of light that are being used for the Major Axis Measurement
    #print Dia_Table['NED Frequency']
    #print Dia_Table_Feq
    #print type(Dia_Table_Feq)
    Dia_Table_Feq_L=list(Dia_Table_Feq) #Dia_Table_Feq_L:-List, Diameter_Table_Fequency_List, The list containing all named frequencies of light that are being used for the Major Axis Measurement
    #print Dia_Table_Feq_L
    Dia_Table_Num=Dia_Table['No.'] #Dia_Table_Num:-astropy.table.column.MaskedColumn, Diameter_Table_Number, The number Ned assigns to
    #print Dia_Table_Num
    #print type(Dia_Table_Num)
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
    D25_S_Maj_Deg=D25_S_Maj/3600.0
    area_T=((D25_S_Maj_Deg)**2)*math.pi
    raGC=float(G_Data['RA(deg)'])
    decGC=float(G_Data['DEC(deg)'])
    #area_A=[((((((decGC-dec)**2)+((raGC-ra)**2)))*(math.pi))/area_T) for dec,ra in zip(decA,raA)]
    #area_A=[((((((decGC-dec)**2)+((raGC-ra)**2)))*(math.pi))/area_T) for dec,ra in zip(Dec_Match_L,RA_Match_L)] #REAL ONE
    #disA=[math.sqrt(((decGC-dec)**2)+((raGC-ra)**2)) for dec,ra in zip(dec_A,raA)] #REAL ONE?
    disA=[math.sqrt(((decGC-dec)**2)+((raGC-ra)**2)) for dec,ra in zip(Dec_Match_L,RA_Match_L)] #REAL ONE
    #print area_A
    #area_max=max(area_A)
    #print area_max
    #plt.vlines(0.00001,0,10,color='red')
    #plt.vlines(1,0,10,color='red')
    #plt.hist(area_A)
    Hist_A=plt.hist(disA)
    Bin_Hight_A=Hist_A[0]
    Bin_Hight_Max=max(Bin_Hight_A)
    #print Bin_Hight_Max
    plt.vlines(D25_S_Maj_Deg,0,Bin_Hight_Max,color='red') #Plots red line at D25
    print D25_S_Maj_Deg
    #Hist_Max=max(area_A)
    #print "Hist_Max ", Hist_Max
    plt.plot()
    #plt.savefig('Test2.png')
    path_2=os.path.realpath('../Master_Code/Histograms/') #Goes to Histograms folder, which will hold the histogram pictures
    print "Path_2=",path_2
    os.chdir(path_2)
    #system('mkdir '+Gname) #Creates Current Galaxy's Folder, Folder Named after Galaxy, Note: will have to remove space from "NGC #" to change to "NGC_#", I Don't know if this works
    Gname_L=Gname.split(" ")
    print "Gname_L: ", Gname_L
    if(len(Gname_L)>1):
        Gname_Modifed=Gname_L[0]+"_"+Gname_L[1] #Adds underscore to remove space from "NGC #" to change to "NGC_#" if there is a space in the name
    else:
        Gname_Modifed=Gname # Does nothing if the galaxy name has no space, ie. NGC#, For example NGC253 instead of NGC 253 or NGC_253
    print Gname_Modifed
    path_3=path_2+'/'+Gname_Modifed+'/'
    print "path_3=",path_3
    directory = os.path.dirname(path_3)
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.chdir(path_3) #Goes to Current Galaxies Folder
    plt.savefig(Gname+'_Ang.png') #Saves angluar histogram figure
    #system('pwd')
    path_4=os.path.realpath('../../../GitHub/')
    print "Path_4=",path_4
    os.chdir(path_4) #Goes back to where this code (the histogram code) is being run, ie. Desktop/GitHub
    #plt.show()

#Area_GC_R_N('NGC4258')

def Driver_Code(Gname):
    Area_GC_R_N_F_2(Gname)
    Area_GC_R_N(Gname)

Driver_Code('NGC4258')
