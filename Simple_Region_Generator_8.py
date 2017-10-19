from astropy.io.fits import Header
from astropy.io import fits
import matplotlib.pyplot as plt
import pyregion
import decimal
import numpy as np
def Simple_Region_Generator (fname,evtfname):
    """
    fname:-str, Filename, The string filename of the CCD Region File from the XPA-DS9 Region Generator (Does Not Exist Yet) that take the FOV1.fits files from an observation as an input
    evtfname:-str, Event 2 Filename, The string filename of the Event 2 file of the obseravation that the current FOV1.fits file and therefore the CCD Region File are from

    This function takes the filename of the CCD Region File generated from the FOV1.fits file from a perticular observation ID which consists of a list of shape strings in the from
    polygon(X1,Y1,X2,Y2...,Xn,Yn) for finte n and converts them to simple regions, ie. box regions of the form box(XCenter,YCenter,X_Width (Called l in code),Y_Hight (Called h in code),Rotation_Angle)
    that the RegArea module for the CIAO tools in python uses to rapidly find the area of the CCD Region geometrically rather then by brute fore with binning. This require that the regions must be moved slightly
    and some loss of area my occur as gaps between regions once connnected are 3 pixels wide. This code works are all possible combinations of CCDs on the Chandra Space Telescope
    for other telescopes and Chandra observations with subarrays ALL BETS ARE OFF ! ! !
    """
    Reg_Data=pyregion.open(fname) #Reg_Data:-pyregion.ShapeList, Region_Data, The Region Data that is obtainted when the pyregion module converts the CCD Region File for it's use
    #print type(Reg_Data)
    fname_Reduced_L=fname.split('.') #fname_Reduced_L:-List, Filename_Reduced_List, The list of strings of the split fname string that was split on ".". fname_Reduced_L[0] is the filename without the extention and fname_Reduced_L[1] is the extenstion
    #print fname_Reduced_L
    fname_Reduced=fname_Reduced_L[0] #fname_Reduced:-str, Filename_Reduced, The filename string without the extention at the end. ie NO .reg or .txt at the end
    #print fname_Reduced
    file=open(fname_Reduced + "_simple_region_no_header_modifed.txt",'w') # file:-file, File, The file that will become the simple_region_no_header_modifed file
    #print type(file)
    file.write('\n') # This imediately moves to the next line (ie. hits the enter key) in the simple_region_no_header_modifed file. This is necessary for the Area Calc code to run correctly and is why the simple_region_no_header_modifed file has the "no_header" part in it's name. I will probbaly unify with file type with simple_region_modifed files and have those work with Area Calc instead.
    file_2=open(fname_Reduced + "_simple_region_modifed_Code.txt",'w') #file_2:-file, File_2, the file that will become the simple_region_modifed file that can be open in DS9 and viewed, This does not work consistanly with the simple_region_no_header_modifed files
    Shape_List=[] #Shape_List:-List, Shape_List, The list of all Cur_Shape strings for an observation
    Shape_Data_L=[] #Shape_Data_L:-List, Shape_Data_List, The list of all data needed to create a simple CCD region for every CCD polygon, represented as a high list where each high element is a list containing the data for a perticular CCD polygon, ie. This list is in the form [[[Midpoint_X_1,Midpoint_Y_1],D_1,Angle_1],[[Midpoint_X_2,Midpoint_Y_2],D_2,Angle_2],...[[Midpoint_X_n,Midpoint_Y_n],D_1,Angle_n]], where 1,2..n are differnt CCD polygons
    for Cur_Reg_Data in Reg_Data: # Selects the current CCD shape polygon
        Point_L=[] #Point_L, Point_list, The list of points that make up the current polygon
        Point_L_R=[]
        Format=Cur_Reg_Data.coord_format #Format:-str, Format, The current coordinate format that the Cur_Reg_Data is in, This code will always use "physical" coordinates
        #print type(Format)
        Coords_L=Cur_Reg_Data.coord_list #Coords_L:-List, Coordinates_List, This is the list of coordinates that makes up the points that make the the current polygon in the form [X1,Y1,X2,Y2...,Xn,Yn] for finte n
        #print type(Coords_L)
        Shape=Cur_Reg_Data.name #Shape:-str, Shape, The string name of the current type of shape, all CCD Region Files will consist of only polygon shapes
        #print type(Shape)
        #print "Format ", Format
        #print "Shape ", Shape
        #print "Coords_L ", Coords_L
        for i in range(0,len(Coords_L)-1,2): # Selects each x value in the Coords_L, ie for the list [X1,Y1,X2,Y2...,Xn,Yn], it only selects X1,X2...Xn for finte n
            Cur_Point=[] #Cur_Point:-List, Current_Point, The current point in the Coords_L, Points are in the form [X,Y] for example [X1,Y1]
            #print i
            Cur_Point.append(Coords_L[i]) # Adds the current X to the Current Point
            Cur_Point.append(Coords_L[i+1]) # Adds the current Y to the Current Point after the X
            Point_L.append(Cur_Point) # Appends the current point to the Point_List
        #print "Point_L ", Point_L
        """
        # Note: This Part of the Code might not be necessary, Note 2: Yep, its definitely not necessary
        for P in Point_L:
            Cur_Point_I=[]
            #print P
            for Comp in P:
                Comp_S=str(Comp)
                Comp_Deci=decimal.Decimal(Comp_S)
                Comp_Rounded=round(Comp_Deci,0)
                Cur_Point_I.append(Comp_Rounded)
            Point_L_R.append(Cur_Point_I)
        #print Point_L_R
        """
        """
        This Part of the code finds the duplicate points in the polygon regions
        """
        Dup_Point_Idx_Group_L=[] #Dup_Point_Idx_Group_L:-List, Duplicate_Point_Index_Group_List, The list of groups in index form, with each group containing the 2 point indexes refering to the Point_L that are duplicate points
        for i in range(0,len(Point_L)): # Selects the current point in the Point_L
            Cur_P=Point_L[i] #Cur_P:-List, Current_Point, The current point
            Cur_X=Cur_P[0] #Cur_X:-float, Current_X, The current X value in pixels
            Cur_Y=Cur_P[1] #Cur_Y:-float, Current_Y, The current Y value in pixels
            for j in range(0,len(Point_L)): # Selects the current test point
                Cur_P_Test=Point_L[j] #Cur_P_Test:-List, Cur_Point_Test, The current test point
                if (i!=j): #Makes sure that the current point is not the test point
                    Cur_X_Test=Cur_P_Test[0] #Cur_X_Test:-float, Current_X_Test, The current test X in pixels
                    Cur_Y_Test=Cur_P_Test[1] #Cur_Y_Test:-float, Current_Y_Test, The current test Y in pixels
                    X_Diff=np.absolute(Cur_X-Cur_X_Test) #X_Diff:-float, X_Diff, The differnce between the current X and the current X test in pixels
                    Y_Diff=np.absolute(Cur_Y-Cur_Y_Test) #Y_Diff:-float, Y_Diff, The differnce between the current Y and the current Y test in pixels
                    #print "X Diff, ", X_Diff
                    #print "Y_Diff, ", Y_Diff
                    if((X_Diff<3) and (Y_Diff<3)): #Makes sure the points are close enough together to actullay be the same point, Duplicate points are extremely close togther and are a result of a glitch in the process of making the FOV1.fits files
                        Cur_Dup_Point_Index_Group=[] #Cur_Dup_Point_Index_Group:-List, Current_Duplicate_Point_Index_Group, The group of indexs refering to Point_L, where each group is made of the 2 indexs of the each one the index of an indivdual point,  A Group is a group of two points in the current polygon. Groups are in the form G=[P1,P2], where Pn=[Xn,Yn] for finite n, Pn can be refrenced in terms of indexs in a list of point for example for the list of points [P1,P2,P3], a Group maybe repersented as G=[P1,P2] or G=[0,1]
                        Cur_Dup_Point_Index_Group.append(i) #Appends the current i onto the Cur_Dup_Point_Index_Group
                        Cur_Dup_Point_Index_Group.append(j) #Appends the current j onto the Cur_Dup_Point_Index_Group
                        Cur_Dup_Point_Index_Group_Rev=Cur_Dup_Point_Index_Group[::-1] #Cur_Dup_Point_Index_Group_Rev:-List, Current_Duplicate_Point_Index_Group_Reversed, The reversed duplicate of the current group. The order of the indexs in groups does not matter, for example [0,1] is the same as [1,0], therefore the reversed groups are duplicates and must be removed from Point_L
                        #print "Norm, ", Cur_Dup_Point_Index_Group
                        #print "Rev, ", Cur_Dup_Point_Index_Group_Rev
                        if Cur_Dup_Point_Index_Group_Rev not in Dup_Point_Idx_Group_L: #Makes sure that the current group is not already included as it's reverse in the Dup_Point_Idx_Group_L
                            Dup_Point_Idx_Group_L.append(Cur_Dup_Point_Index_Group) #Appends the Cur_Dup_Point_Index_Group to the Dup_Point_Idx_Group_L
                            #print Dup_Point_Idx_Group_L
        #print Dup_Point_Idx_Group_L
        """
        This part of the code gets rid of duplicate points by replacing them with a single points directly inbetween the duplicates
        """
        Point_L_Cor=[] #Point_L_Cor:-List, Point_List_Corrected, The list of points that make up the current polygon which as the duplicate points replaced by one new point at the center of the segment that the two duplicate points makes up
        for k in range(0,len(Point_L)): # k:-int, k, k is an index refering to the Point_L
            #print k
            #print "Point_L[k], ", Point_L[k]
            Unique_Test=1 #Unique_Test:-int, Unique_Test, Unique_Test repersents the 3 states of uniqueness that the current k index (ref. Point_L) can have, Unique_Test=1 means k is unique, Unique_Test=-1 means k=i and thus is not unique, Unique_Test=0 means k=j and thus is not unique
            for Dup_P_Inx in Dup_Point_Idx_Group_L: #Dup_P_Inx:-int, Duplicate_Point_Index, The group of duplicate point indexs (ref. Point_L) of the form [i,j], for example: [6, 7]
                Cur_i=Dup_P_Inx[0] #Cur_i:-int, Current_i, the Current i index (ref. Point_L)
                Cur_j=Dup_P_Inx[1] #Cur_j:-int, Current_j, the Current j index (ref. Point_L)
                if(k==Cur_i): #Selects only the first point index i (ref. Point_L) in the current Dup_P_Inx
                    Unique_Test=-1 #Sets Unique_Test equal to 1
                if(k==Cur_j): # Throws out the second point index j (ref. Point_L) in the current Dup_P_Inx
                    Unique_Test=0 #Sets Unique_Test equal to 0
            if(Unique_Test==1):
                Point_L_Cor.append(Point_L[k]) #Appends the current point with the "Kth" index (ref. Point_L) if the current point is unique
            if(Unique_Test==-1): #This only selects the first of the 2 duplicate point indexs (ref. Point_L)
                for Dup_P_I in Dup_Point_Idx_Group_L: #Dup_P_I:-List, The group of duplicate point indexs (ref. Point_L) of the form [i,j], just like Dup_P_I
                    C_i=Dup_P_I[0] #C_i:-int, Current_i, the Current i index (ref. Point_L)
                    C_j=Dup_P_I[1] #C_j:-int, Current_j, the Current j index (ref. Point_L)
                    if (k==C_i): # Makes sure that the current point from the Point_L is the first point index i (ref. Point_L) in the current Dup_P_Inx
                        Point_i=Point_L[C_i] #Point_i:-List, Point_i, the first point in a group of duplicate points #Here is the mistake(I don't think there is a mistake anymore)
                        #print Point_i
                        Point_j=Point_L[C_j] #Point_j:-List, Point_j,the secound point in a group of duplicate points #Here is the mistake(I don't think there is a mistake anymore)
                        X_i=Point_i[0] #X_i:-float, X_i, The first X value of the group of duplicate points in pixels
                        #print "X_i", X_i
                        Y_i=Point_i[1] #Y_i:-float, Y_i, The first Y value of the group of duplicate points in pixels
                        #print "Y_i", Y_i
                        X_j=Point_j[0] #X_j:-float, X_j, The second X value of the group of duplicate points in pixels
                        #print "X_j", X_j
                        Y_j=Point_j[1] #Y_j:-float, Y_j, The second Y value of the group of duplicate points in pixels
                        #print "Y_j", Y_j
                        X_New=(X_i+X_j)/2.0 #X_New:-float, X_New, The New X value for the new point that will be in the center of the 2 duplicate points of the cur duplicate point group
                        Y_New=(Y_i+Y_j)/2.0 #Y_New:-float, Y_New, The New Y value for the new point that will be in the center of the 2 duplicate points of the cur duplicate point group
                        Point_New=[X_New,Y_New] #Point_New:-List, Point_New, The new point that is in the center of the 2 duplicate points, that will be replacing the 2 duplicate points
                        #print "Point_New, ", Point_New
                        Point_L_Cor.append(Point_New) #Appens the new point onto the Point_List_Corrected in place of the 2 duplicate points
        """
        This Part of the Code finds the Corner Groups in index form (ref. Point_L_Cor) that are the corners of the polygon and uses each indivdual group to create a single midpoint in the center of each Corner Group that will be used to find the distances between Corner Groups
        """
        #print Point_L_Cor
        #print len(Point_L_Cor)
        Dist_L=[] #Dist_L:-List, Distance_List, The list of all possible distances between points of the corrected polygon, ie, a list of all distances from one point to all other points in the polygon except itself, then the distances from the next point to all other points in the polygon except itself, repeat for all points in the polygon
        Dist_L_With_P=[] #Dist_L_With_P:-List, Distance_List_With_Points, The list of all distances like the Dist_L but now each distance has the indexs of the points that are that distance apart attached to the distance itself in the form of a list. Indexs refer to Point_L_Cor # Change Name to Dist_L_With_Group=[]
        Min_Dist_L=[] #Min_Dist_L:-List, Minimum_Distance_List, The list of distances short enough to have to be a Corner Groups
        Min_P_L=[] #Min_P_L, Minimum_Points_List, The list of all Corner Groups in index form (ref. Point_L_Cor)
        for i in range(0,len(Point_L_Cor)): # i:-int, i, i refers to the "ith" index in Point_L_Cor
            Current_Point=Point_L_Cor[i] #Current_Point:-List, Current_Point, The Current Point in the Point_L_Cor
            Current_X=Current_Point[0] #Current_X:-float, Current_X, The Current X value
            Current_Y=Current_Point[1] #Current_Y:-float, Current_Y, The Current Y value
            for j in range(0,len(Point_L_Cor)):
                if(i!=j): #Makes sure that the Current Point is not the Test Point
                    Current_Point_Test=Point_L_Cor[j] #Current_Point_Test:-List, Current_Point_Test, The Current Test Point
                    Current_X_Test=Current_Point_Test[0] #Current_X_Test:-float, Current_X_Test, The Current Test X from the Current Test Point
                    Current_Y_Test=Current_Point_Test[1] #Current_Y_Test:-float, Current_Y_Test, The Current Test Y from the Current Test Point
                    Cur_X_Diff=Current_X-Current_X_Test #Cur_X_Diff:-float, Current_X_Differnce, The current differnce between the Current_X and the Current_X_Test
                    Cur_Y_Diff=Current_Y-Current_Y_Test #Cur_Y_Diff:-float, Current_Y_Differnce, The current differnce between the Current_Y and the Current_Y_Test
                    Cur_Distance=np.sqrt(((Cur_X_Diff)**2)+((Cur_Y_Diff)**2)) #Cur_Distance:-numpy.float64, Current_Distance, The Current Distance between the Current Point and the Current Test Point
                    #print Cur_Distance
                    #print type(Cur_Distance)
                    Dist_L.append(Cur_Distance) #Appends the Current Distance to the Dist_L
                    Cur_Dist_With_P=[i,j,Cur_Distance] #Cur_Dist_With_P:-List, Current_Distance_With_Points, The list containing the current distance between the Current Point and the Current Test Point and both the index for the current point i and the index for the current test point j in the form [i,j,Cur_Distance]
                    #print Cur_Dist_With_P
                    Dist_L_With_P.append(Cur_Dist_With_P) #Appends the Current_Distance_With_Point to the Distance_List_With_Points
                    #print Dist_L_With_P
        #print Dist_L
        Dist_Min=min(Dist_L) #Dist_Min:-numpy.float64, Distance_Minimum, The minimum distance between any 2 differnt points in the current polygon
        #print type(Dist_Min)
        #print Dist_Min
        #for Dist in Dist_L:
            #if (Dist<(3.0*Dist_Min)):
                #Min_Dist_L.append(Dist_Min)
        for Dist_W_P in Dist_L_With_P: #Dist_W_P:-List, Distance_With_Points, The current distance with point indexs (indexs ref. Point_L_Cor) in Distance_List_With_Points
            Dist=Dist_W_P[2] #Dist:-numpy.float64, Distance, The current distance in the current Distance_With_Points
            #print type(Dist)
            if (Dist<(3.0*Dist_Min)): #Checks to see the the current two points selected in the Distance_List_With_Points are close enough that they have to be a "Corner" in the Octagonal polygon, ie. the 2 points can be replaced by the corner of the simple region box
                Cur_Min_i=Dist_W_P[0] #Cur_Min_i:-int, Current_Minimum_i, The current i index refering to the Point_L_Cor that is the index of the first point making up the current Corner Group
                Cur_Min_j=Dist_W_P[1] #Cur_Min_j:-int, Current_Minimum_j, The current j index refering to the Point_L_Cor that is the index of the second point making up the current Corner Group
                Cur_Min_Group=[Cur_Min_i,Cur_Min_j] #Cur_Min_Group:-List, Currnet_Minimum_Group, The list of indexs (ref. Point_L_Cor) that make up a Corner in the Octagonal polygon, The name of this list is a "Corner Group"
                Min_Dist_L.append(Dist) #Appends the current distance associated with the current Corner Group
                Min_P_L.append(Cur_Min_Group) #Appends the current points indexs (ref. Point_L_Cor) of the Curent Corner Group to the Cur_Min_Group


        #print Min_Dist_L
        #print Min_P_L #Need to eliminate duplicate groups  Ex. [1, 2], [2, 1]
        Min_P_L_Cor=Min_P_L #Min_P_L_Cor:-List, Minimum_Points_List_Corrected, The list of Corner Groups in index form that have (or will at this line 173) all reversed duplicates removed
        for Min_G in Min_P_L: #Min_G:-List, Minimum_Group, The current "Minimum_Group" aka. the current Corner Group in index form (ref. Point_L_Cor)
            Min_G_Rev=Min_G[::-1] #Min_G_Rev:-List, Minimum_Group_Reversed, The reverse duplicate of the current Corner Group in index form (ref. Point_L_Cor)
            Min_P_L_Cor.remove(Min_G_Rev) #Removes the current reverse duplicate Corner Group from Min_P_L_Cor
        #print Min_P_L_Cor
        Midpoint_L=[] #Midpoint_L:-List, Midpoint_List, The list of all Corner Group Midpoints
        Midpoint_L_With_Groups=[] #Midpoint_L_With_Groups:-List, Midpoint_List_With_Groups, The list of all Corner Group Midpoints with the Corner Group in index (ref. Point_L_Cor) form attached onto each midpoint
        for Cur_Group in Min_P_L_Cor: #Cur_Group:-list, Current_Group, The current Corner Group
            Point_One_Inx=Cur_Group[0] #Point_One_Inx:-int, Point_One_Index, The index (ref. Point_L_Cor) that is the index for the first point in the Current Corner Group
            Point_Two_Inx=Cur_Group[1] #Point_Two_Inx:-int, Point_Two_Index, The index (ref. Point_L_Cor) that is the index for the second point in the Current Corner Group
            Point_One=Point_L_Cor[Point_One_Inx] #Point_One:-List, Point_One, The first point in the current Corner Group
            Point_Two=Point_L_Cor[Point_Two_Inx] #Point_Two:-List, Point_Two, The second point in the current Corner Group
            #print Point_One
            #print Point_Two
            X_One=Point_One[0] #X_One:-float, X_One, The X value in pixels of the first point in the current Corner Group
            Y_One=Point_One[1] #Y_One:-float, Y_One, The Y value in pixels of the first point in the current Corner Group
            X_Two=Point_Two[0] #X_Two:-float, X_Two, The X value in pixels of the second point in the current Corner Group
            Y_Two=Point_Two[1] #Y_Two:-float, Y_Two, The Y value in pixels of the second point in the current Corner Group
            X_Mid=(X_One+X_Two)/2.0 #X_Mid:-float, X_Middle, The X point of the new point that will be directly inbetween the two points making up the current Corner Group
            Y_Mid=(Y_One+Y_Two)/2.0 #Y_Mid:-float, Y_Middle, The Y point of the new point that will be directly inbetween the two points making up the current Corner Group
            Point_Mid=[X_Mid,Y_Mid] #Point_Mid:-List, Point_Middle, The midpoint of the current Corner Group
            Point_Mid_With_Groups=[X_Mid,Y_Mid,Cur_Group] #Point_Mid_With_Groups:-List, Point_Middle_With_Groups, The Midpoint of the current Corner Group with the Current Corner Group in index form (ref. Point_L_Cor) attached to the list making the current midpoint
            Midpoint_L.append(Point_Mid) #Appends the Midpoint of the current Corner Group to the Midpoint List #Need to attach Groups
            Midpoint_L_With_Groups.append(Point_Mid_With_Groups) #Appends the current Corner Group with the Current Corner Group in index form (ref. Point_L_Cor) attached, to the Midpoint_L_With_Groups
        #print Midpoint_L
        Midpoint=np.mean(Midpoint_L, axis=0) #Midpoint:-numpy.ndarray, Midpoint, The midpoint of the current polygon
        #print "Midpoint ", Midpoint
        #print type(Midpoint)
        #print Midpoint_L_With_Groups
        """
        This part of the code uses the Midpoint_L_With_Groups to create "Big Groups" which are groups of corner groups and maybe only one of 2 types of Big Group, Short Big Groups and Huge Big Groups, Addtionally the code finds the distance between the Corner Groups for each Big Group
        """
        Dist_L_With_P_Mid=[] #Dist_L_With_P_Mid:-List, Distance_List_With_Points_Midpoints, The list all distances from one Corner Group midpoint to all the other Corner Group Midpoints for all Corner Group Midpoints with the Corner Group Midpoint indexs (ref. Midpoint_L_With_Groups) attached
        for i in range(0,len(Midpoint_L_With_Groups)): # i:-int, i, The "ith" index of Midpoint_L_With_Groups
            Midpoint_Cur=Midpoint_L_With_Groups[i] #Midpoint_Cur:-List, Midpoint_Current, The current midpoint with the Corner Group in index form (ref. Point_L_Cor) attached, in Midpoint_L_With_Groups
            X_Mid_Cur=Midpoint_Cur[0] #X_Mid_Cur:-float, X_Midpoint_Cur, The X value in pixels of the current midpoint
            Y_Mid_Cur=Midpoint_Cur[1] #Y_Mid_Cur:-float, Y_Midpoint_Cur, The Y value in pixels of the current midpoint
            Group_Cur=Midpoint_Cur[2] #Group_Cur:-List, Group_Current, The Current Corner Group in index form (ref. Point_L_Cor) of the current midpoint
            #print i
            for j in range(0,len(Midpoint_L_With_Groups)): # j:-int, j, The "jth" index of Midpoint_L_With_Groups
                if(i!=j): #Makes sure the Current Midpoint is not the Test Midpoint
                    Midpoint_Test=Midpoint_L_With_Groups[j] #Midpoint_Test:-List, Midpoint_Test, The test midpoint with the Corner Group in index form (ref. Point_L_Cor) attached in Midpoint_L_With_Groups
                    X_Mid_Test=Midpoint_Test[0] #X_Mid_Test:-float, X_Midpoint_Test, The X value in pixels of the current test midpoint
                    Y_Mid_Test=Midpoint_Test[1] #Y_Mid_Test:-float, Y_Midpoint_Test, The Y value in pixels of the current test midpoint
                    Group_Test=Midpoint_Test[2] #Group_Test:-List, Group_Test, The Current Test Corner Group in index form (ref. Point_L_Cor) of the current test midpoint
                    X_Mid_Diff=X_Mid_Cur-X_Mid_Test #X_Mid_Diff:-float, X_Midpoint_Differnce, The X differnce bewteen the Current Midpoint and the current Test Midpoint in pixels
                    Y_Mid_Diff=Y_Mid_Cur-Y_Mid_Test #Y_Mid_Diff:-float, Y_Midpoint_Differnce, The Y differnce bewteen the Current Midpoint and the current Test Midpoint in pixels
                    Cur_Dist_Mid=np.sqrt(((X_Mid_Diff)**2)+((Y_Mid_Diff)**2)) #Cur_Dist_Mid:-numpy.float64, Current_Distance_Midpoints, The distance between the current midpoint and the current test midpoint
                    #print type(Cur_Dist_Mid)
                    Cur_Dist_With_P_Mid=[i,j,Cur_Dist_Mid] #Cur_Dist_With_P_Mid:-List, Current_Distance_With_Points_Midpoints, The distance between the current midpoint and the current test midpoint in pixels with the indexs i (The Current index) (ref. Midpoint_L_With_Groups) and j (The Current Test index) attached, list in in the form [i,j,Cur_Dist_Mid] # i and j are group indexs, ie the indexes of the list Midpoint_L_With_Groups
                    Dist_L_With_P_Mid.append(Cur_Dist_With_P_Mid) # Appends the Current_Distance_With_Points_Midpoints to the Distance_List_With_Points_Midpoints
                    #Dist_L_With_P_Mid=
                    #print Cur_Dist_Mid
        #print Dist_L_With_P_Mid
        Dist_Mid_L=[] #Dist_Mid_L:-List, Distance_Midpoint_List, The list of all distances from one Corner Group midpoint to all the other Corner Group Midpoints for all Corner Group Midpoints
        for Dist_W_G in Dist_L_With_P_Mid: #Dist_W_G:-List, Distance_With_Groups, The Current Distance with the Midpoint Group in index form (ref. Midpoint_L_With_Groups) attached, the Midpoint groups represent the corner groups so the Midpoint Group can be thought as a group of groups, this group of groups is named a "Big Group" or "B" for short
            Cur_Mid_Dist=Dist_W_G[2] #Cur_Mid_Dist:-numpy.float64, Current_Midpoint_Distance, The Current distance between the two Corner Midponts in the Current Big Group
            #print Cur_Mid_Dist
            #print type(Cur_Mid_Dist)
            Dist_Mid_L.append(Cur_Mid_Dist) #Appends the Current Midpoint Distance to Distance_Midpoint_List
        #print Dist_Mid_L
        """
        This part of the code makes a list of all Short Big Groups and Short Big Group Distances without reverse duplicates
        """
        Dist_Mid_Min=min(Dist_Mid_L) #Dist_Mid_Min:-numpy.float64, Distance_Midpoint_Minimum, The distance between the 2 closest Corner Group Midpoints
        #print type(Dist_Mid_Min)
        #print Dist_Mid_Min
        Min_Dist_L_With_P_Mid=[] #Min_Dist_L_With_P_Mid:-List, Minimum_Distance_List_With_Points_Midpoint, The list of all Short Big Group Distances
        for Cur_D_W_Group in Dist_L_With_P_Mid: #Cur_D_W_Group:-List, Current_Distance_With_Group, The current distance from the Current Corner Group Midpoint to the Current Corner Group Midpoint Test, ie. the distance associated with the current Big Group, with the current Big Group in index form attached
            Cur_M_D=Cur_D_W_Group[2] #Cur_M_D:-numpy.float64, Current_Midpoint_Distance, The current distance from the Current Corner Group Midpoint to the Current Corner Group Midpoint Test, ie. the distance associated with the current Big Group
            #print Cur_M_D
            #print type(Cur_M_D)
            if(Cur_M_D<1.2*Dist_Mid_Min): #Checks to see if the current distance is small enough to have to be "Short Big Group", Since the polygon shape is symetric there are really only 2 posssible distances that any 2 Corner Groups can be from one another, The short one of these is called the "Short Big Group Distance" and the associated "Short Big Group" where the Short Big Group Distance comes from is one of the sides of the Octagonal Regtangle polygon (Where the Corner Groups are the corners of the rectange), The other distance the "Huge Big Group Distance" (I am running out of words to discribe size here) reperesnets the distance across the Octagonal Regtangle polygon from one corner group to another and is not used in the code
                Min_Dist_L_With_P_Mid.append(Cur_D_W_Group) #Appends the Current_Distance_With_Group that must be a Short Big Group Distance to the Minimum_Distance_List_With_Points_Midpoint
        #print Min_Dist_L_With_P_Mid #Need to eliminate duplicates
        #print len(Min_Dist_L_With_P_Mid)
        Min_P_Mid_L=[] #Min_P_Mid_L:-List, Minimum_Points_Midpoint_List, The list of all Short Big Groups in index form (ref. Midpoint_L_With_Groups) in the current polygon
        for M_D_W_P_M in Min_Dist_L_With_P_Mid: #M_D_W_P_M:-List, Minimum_Distance_With_Points_Midpoint, The current Short Big Group Distance with the associated Short Big Group in index form (ref. Midpoint_L_With_Groups) attached in the form [i,j,Short Big Group Distance]
            #print M_D_W_P_M
            Min_Group=[] #Min_Group:-List, Minimum_Group, The current Short Big Group in index form (ref. Midpoint_L_With_Groups)
            for Z in M_D_W_P_M: #Z:-Variable Type; posssible types {int,numpy.float64}; Type governed by current position in list M_D_W_P_M follows the pattern [int,int,numpy.float64], Z, The current value in the M_D_W_P_M List
                #print type(Z)
                if (Z<10): #This tests if they current Z value is a Corner Group Index (ref. Midpoint_L_With_Groups) or a Short Big Group Distance, To perform this test, this if statement tests if the current value is less then "10", "10" has varying units, as in when Z is an index it is "10" is unitless, when Z is a Short Big Group Distance, "10" is in units of pixels, This works becasue it is not possible for the number of Short Big Group Distances to be larger then 8<10 and it is assummed that the CCD polygon will never have a size on the scale of 10 pixels, Although this works this is a terrible way to do this, instead the test should test what data type Z is since the Corner Group Indexs (ref. Midpoint_L_With_Groups) will always be "int" type and the Short Big Group Distances will always be "numpy.float64" type. This will be corrected and tested in the future
                #if(type(Z)=="int"): This would be the most General way to do this, This will replace the "if (Z<10):" test soon
                    Min_Group.append(Z) #Appends the current Z value onto the current Short Big Group in index form, Z will be i then j (ref. Midpoint_L_With_Groups)
            #print Min_Group
            Min_P_Mid_L.append(Min_Group) #Appends the current Short Big Group in index form (ref. Midpoint_L_With_Groups) to the Min_P_Mid_L
        #print Min_P_Mid_L
        Min_P_Mid_L_Cor=Min_P_Mid_L #Min_P_Mid_L_Cor:-List, Minimum_Points_Midpoint_List_Corrected, The list of all Short Big Groups in index form (ref. Midpoint_L_With_Groups) in the current polygon with (or for this line will have) all reverse duplicates removed
        for Min_Gr in Min_P_Mid_L: #Min_Gr:-List, Minimum_Group, The current Short Big Group in index form (ref. Midpoint_L_With_Groups)
            Min_Gr_Rev=Min_Gr[::-1] #Min_Gr_Rev:-List, Minimum_Group_Reversed, The reverse of the current Short Big Group in index form (ref. Midpoint_L_With_Groups)
            Min_P_Mid_L_Cor.remove(Min_Gr_Rev) #Removes the reverse of the current Short Big Group in index form (ref. Midpoint_L_With_Groups) from Min_P_Mid_L_Cor
        #print Min_P_Mid_L_Cor
        """
        The list of all Short Big Groups in the current polygon with the Corner Groups in the Short Big Groups in index form (ref. Point_L_Cor)
        """
        B_Small_Point_Inx_L=[] #B_Small_Point_Inx_L:-List, B_Small_Point_Index_List, The list of all Short Big Groups in the current polygon with the Corner Groups in the Short Big Groups in index form (ref. Point_L_Cor)
        for B in Min_P_Mid_L_Cor: #B:-List, B, The current Short Big Group in index form (ref. Midpoint_L_With_Groups)
            #print B
            Cur_Group_One_Inx=B[0] #Cur_Group_One_Inx:-int, Current_Group_One_Index, The index (ref. Midpoint_L_With_Groups) of the first Corner Group in the current Short Big Group
            Cur_Group_Two_Inx=B[1] #Cur_Group_Two_Inx:-int, Current_Group_Two_Index, The index (ref. Midpoint_L_With_Groups) of the second Corner Group in the current Short Big Group
            #print "Cur_Group_One_Inx ", Cur_Group_One_Inx
            #print "Cur_Group_Two_Inx ", Cur_Group_Two_Inx
            #print Midpoint_L_With_Groups[Cur_Group_One_Inx]
            Cur_Group_One=Midpoint_L_With_Groups[Cur_Group_One_Inx][2] #Cur_Group_One:-List, Current_Group_One, The first Corner Group in the current Short Big Group in index form (ref. Point_L_Cor)
            Cur_Group_Two=Midpoint_L_With_Groups[Cur_Group_Two_Inx][2] #Cur_Group_Two:-List, Current_Group_Two, The second Corner Group in the current Short Big Group in index form (ref. Point_L_Cor)
            #print ""
            #print "Cur_Group_One ", Cur_Group_One
            #print "Cur_Group_Two ", Cur_Group_Two
            B_Small_Point_Inx=[Cur_Group_One,Cur_Group_Two] #B_Small_Point_Inx:-List, B_Small_Point_Index, The currnet Short Big Group with the Corner Groups in index form (ref. Point_L_Cor)
            #print "B_Small_Point_Inx ", B_Small_Point_Inx
            B_Small_Point_Inx_L.append(B_Small_Point_Inx) #Appends the current Short Big Group with the Corner Groups in index form (ref. Point_L_Cor) to B_Small_Point_Index_List
        #print B_Small_Point_Inx_L
        """
        This part of the code finds the distances between all the points in a perticular Short Big Group
        """
        B_Dist_L=[] #B_Dist_L:-List, B_Distance_List, The list of distances from one point in the currnet Corner Group in the current Short Big Group to all other points in the Short Big Group (Both Corner Groups) for all points in the current Short Big Group for all Short Big Groups
        B_Dist_With_Diff_L=[] #B_Dist_With_Diff_L:-List, B_Distance_With_Differnce_List, The list of distances from one point in the currnet Corner Group in the current Short Big Group to all other points in the Short Big Group (Both Corner Groups) for all points in the current Short Big Group for all Short Big Groups with the current X_Differnce and current Y_Differnce attached attached in the form [X_D,Y_D,C_D]
        for B_S_P_Inx in B_Small_Point_Inx_L: #B_S_P_Inx:-List, B_Small_Point_Index, Short Big Group with the Corner Groups in index form (ref. Point_L_Cor)
            #print B_S_P_Inx
            for i in range(0,len(B_S_P_Inx)): # i:-int, i, The "ith" index in B_S_P_Inx
                Cur_G=B_S_P_Inx[i] #Cur_G:-List, Current_Group, The current Corner Group in index form (ref. Point_L_Cor)
                #print "Cur_G ", Cur_G
                for j in range(0,len(Cur_G)): # j:-int, j, The "jth" index in Cur_G
                    Cur_P_Inx=Cur_G[j] #Cur_P_Inx:-int, Current_Point_Index, The index (ref. Point_L_Cor) of the currrent point in the current Corner Group in the Current Short Big Group
                    #print "Cur_P_Inx ", Cur_P_Inx
                    Cur_Po=Point_L_Cor[Cur_P_Inx] #Cur_Po:-List, Current_Point, The current point in the current Corner Group in the Current Short Big Group
                    #print "Cur_Po ", Cur_Po
                    C_X=Cur_Po[0] #C_X:-float, Current_X, The current X value in the current point in the current Corner Group in the Current Short Big Group in pixels
                    C_Y=Cur_Po[1] #C_Y:-float, Current_Y, The current Y value in the current point in the current Corner Group in the Current Short Big Group in pixels
                    #print "C_X ", C_X
                    #print "C_Y ", C_Y
                    #print type(Cur_X)
                    #B_Dist_L=[]
                    for k in range(0,len(B_S_P_Inx)):
                        if((k>0) and (k!=i)): #This makes sure that the current Test Corner Group is not the Current Corner Group # I need to get rid of duplicate point testing ie. Only top group to bottom Not including bottom to top
                            Cur_G_Test=B_S_P_Inx[k] #Cur_G_Test:-List, Current_Group_Test, The Current Test Corner Group in index form (ref. Point_L_Cor)
                            #print "Cur_G_Test ", Cur_G_Test
                            for Cur_P_Inx_Test in Cur_G_Test: #Cur_P_Inx_Test:-int, Current_Point_Index_Test, The index (ref. Point_L_Cor) of the current test point in the current test Corner Group in the Current Short Big Group
                                #print "Cur_P_Inx_Test ", Cur_P_Inx_Test
                                Cur_Po_Test=Point_L_Cor[Cur_P_Inx_Test] #Cur_Po_Test:-List, Current_Point_Test, The current test point in the current test Corner Group in the Current Short Big Group
                                #print "Cur_Po_Test ", Cur_Po_Test
                                C_X_T=Cur_Po_Test[0] #C_X_T:-float, Currnet_X_Test, The current test X value of the current test point in the current test Corner Group in the Current Short Big Group
                                C_Y_T=Cur_Po_Test[1] #C_Y_T:-float, Currnet_Y_Test, The current test Y value of the current test point in the current test Corner Group in the Current Short Big Group
                                X_D=C_X-C_X_T #X_D:-float, X_Differnce, The current X differnce between the current X value and the currnet X test value in pixels
                                Y_D=C_Y-C_Y_T #Y_D:-float, Y_Differnce, The current Y differnce between the current Y value and the currnet Y test value in pixels
                                C_D=np.sqrt(((X_D)**2)+((Y_D)**2)) #C_D:-numpy.float64, Current_Distance, The distance between the current point and the current test point in the current Short Big Group
                                #print type(C_D)
                                B_Dist_L.append(C_D) #appends the Current_Distance to B_Dist_L
                                Cur_B_Dist_With_Diff=[X_D,Y_D,C_D] #Cur_B_Dist_With_Diff:-List, Current_B_Distance_With_Difference, The current distance between the current point and the test point with the current X_Differnce and current Y_Differnce attached in the form [X_D,Y_D,C_D]
                                B_Dist_With_Diff_L.append(Cur_B_Dist_With_Diff) #Appends the Current_B_Distance_With_Difference to B_Distance_With_Differnce_List
                                #print "C_X_T ", C_X_T
                                #print "C_Y_T", C_Y_T
                                #print "C_D ", C_D
        #print B_Dist_L
        #print B_Dist_With_Diff_L
        """
        This part of the code finds "D", the side distance of the simple region CCD box
        """
        B_Dist_Gen_L=[] #B_Dist_Gen_L:-List, B_Distance_Generated_List, The list of distances from one point in the currnet Corner Group in the current Short Big Group to all other points in the Short Big Group (Both Corner Groups) for all points in the current Short Big Group for all Short Big Groups. These distances are "generated" (Taken) from B_Dist_With_Diff_L, # Distances "generated" (Taken) from B_Dist_With_Diff_L
        for B_Dist_With_Diff in B_Dist_With_Diff_L: #B_Dist_With_Diff:-List, B_Distance_With_Differnce, The currnet distance between points in a Short Big Group in the B_Dist_With_Diff_L
            B_Dist_Gen=B_Dist_With_Diff[2] #B_Dist_Gen:-numpy.float64, B_Distance_Generated, The current distance from B_Dist_With_Diff_L
            #print type(B_Dist_Gen)
            B_Dist_Gen_L.append(B_Dist_Gen) #Appends the current distance to B_Dist_Gen_L
        B_Dist_Max=max(B_Dist_Gen_L) #B_Dist_Max:-numpy.float64, B_Distance_Maximum, The maximum distance between any 2 points in a Short Big Group for all Short Big Groups
        #print B_Dist_Max
        #print type(B_Dist_Max)
        B_Dist_Max_L=[] #B_Dist_Max_L:-List, B_Distance_Maximum_L, The list of all "Maximum Distances" for a polygon. Since the polygon is symetric there should be 4 nearly identical maximum distances per polygon, one per side
        for B_Dist in B_Dist_L: #B_Dist:-numpy.float64, B_Distance, The current distance in B_Dist_L
            #print type(B_Dist)
            if(B_Dist>0.99*B_Dist_Max): #Checks to see if the current distance is also a maximum distance, since the polygon is symetric the maximum distance for each Short Big Group should be NEARLY identical, so all maximum values must be found and averaged to get the best possible value for the maximum distance
                B_Dist_Max_L.append(B_Dist) #Appends the current distance to the B_Distance_Maximum_L
        #print B_Dist_Max_L
        D=np.average(B_Dist_Max_L) #D:-numpy.float64, D, The longest side distance of the CCD simple region Box that will be generated that is being generated #This is the longest "Side" distance of the CCD Box that is being generated
        #print "D ", D
        #print type(D)
        "This part of the code finds the angle at which the box is rotated, this angle is not used instead the rotation angle of the telescope from the evt2.fits file is used, But this code must remain because the calcuated angle is referenced everywhere after this point"
        B_D_W_Diff_Max_L=[] #Big Distance With Points Max List
        for B_D_W_Diff in B_Dist_With_Diff_L: #B_D_W_Diff:-List, B_Distance_With_Differnce, The current distance with X_Diff and Y_Diff attached
            #print B_D_W_Diff
            B_D=B_D_W_Diff[2] #B_D:-numpy.float64, B_Distance, The current distance between Short Big Distance points
            #print type(B_D)
            if(B_D>0.99*B_Dist_Max): #Makes sure that B_D is a "Maximum Distance"
                B_D_W_Diff_Max_L.append(B_D_W_Diff) #Appends the current distance and the X_Differnce and Y_Differnce of that distance to the Big_Distance_With_Points_Max_List if the distance is a "Maximum Distance"
        #print B_D_W_Diff_Max_L
        Angle_L=[]
        for B_D_W_Diff_Max in B_D_W_Diff_Max_L: #B_D_W_Diff_Max:-List, B_Distance_With_Differnce_Maximum, The current Maximum distance with the X_Differnce and Y_Differnce attached
            Cur_X_D=B_D_W_Diff_Max[0] #Cur_X_D:-float, Current_X_Differnce, The Current_X_Differnce related to the current Maximum Distance
            #print type(Cur_X_D)
            Cur_Y_D=B_D_W_Diff_Max[1] #Cur_Y_D:-float, Current_Y_Differnce, The Current_Y_Differnce related to the current Maximum Distance
            Cur_Ratio=Cur_Y_D/Cur_X_D #Cur_Ratio:-float, Current_Ratio, The Current_Ratio of the Y_Differnce to the X_Differnce
            Cur_Angle=np.arctan(Cur_Ratio) #Cur_Angle:-numpy.float64, Current_Angle, The rotation angle of the current simple region CCD box in radians
            #print type(Cur_Angle)
            Cur_Angle_Deg=(180.0/3.141592654)*Cur_Angle #Cur_Angle_Deg:-numpy.float64, Current_Angle_Degrees, The rotation angle of the current simple region CCD box in degrees
            #print Cur_Angle
            #print Cur_Angle_Deg
            #print type(Cur_Angle_Deg)
            if(Cur_Angle_Deg<0): #Checks to see if the current rotation angle is negitve
                Cur_Angle_Deg_Pos=Cur_Angle_Deg+90.0 #Cur_Angle_Deg_Pos:-numpy.float64, Current_Angle_Degrees_Positive, The equlivlent positive angle of the Current_Angle_Degrees if Current_Angle_Degrees is negitve
            else:
                Cur_Angle_Deg_Pos=Cur_Angle_Deg #Sets Cur_Angle_Deg_Pos to Cur_Angle_Deg, ie. The positive version of Current_Angle_Degrees that was positive from the start is equal to the orginal value of Current_Angle_Degrees
            #print Cur_Angle_Deg_Pos
            Angle_L.append(Cur_Angle_Deg_Pos) #Appends the positive rotation angle for the current Short Big Group maximum distance to the Angle_List
        #print Angle_L
        Angle=np.average(Angle_L) #Angle:-numpy.float64, Angle, The average rotation angle for the current CCD # This has to change to include infomation about what side is being used, Maybe use the orinatation angle of the FOV itself
        """
        This part of the code creates the Shape_Data_L, which is a list of all data required to create every simple CCD region for an observation, the list is in the form This list is in the form [[[Midpoint_X_1,Midpoint_Y_1],D_1,Angle_1],[[Midpoint_X_2,Midpoint_Y_2],D_2,Angle_2],...[[Midpoint_X_n,Midpoint_Y_n],D_1,Angle_n]], where 1,2..n are differnt CCD polygons.
        Each element refers to a single CCD polygon, These CCD polygons are overlaping and the ultimate end product simple regions are the result of combining the simple CCD regions into larger simple region boxes that cover multible CCDs
        The Shape_Data_L is referenced consistanly after this point in the code
        """
        #print Angle
        Midpoint_X=Midpoint[0] #Midpoint_X:-numpy.float64, Midpoint_X, The X value of the midpoint of the current simple region CCD box
        Midpoint_Y=Midpoint[1] #Midpoint_X:-numpy.float64, Midpoint_Y, The Y value of the midpoint of the current simple region CCD box
        Cur_Shape='box('+str(Midpoint_X)+','+str(Midpoint_Y)+','+ str(D) +','+str(D)+','+str(Angle)+')' + '\n' #Cur_Shape:-str, Current_Shape, The shape string of the current CCD polygon
        hdulist = fits.open(evtfname) #hdulist:-astropy.io.fits.hdu.hdulist.HDUList, hdulist, The hdulist of the current event 2 file
        #print type(hdulist)
        Tele_Rot_Ang=hdulist[1].header['ROLL_NOM'] #Tele_Rot_Ang:-float, Telescope_Rotation_Angle, The rotation angle of the Chandra Space Telescope during the observation in degrees
        #print "Tele_Rot_Ang ", Tele_Rot_Ang
        #print type(Tele_Rot_Ang)
        Angle_Tele=-Tele_Rot_Ang #Angle_Tele:-float, Angle_Telescope, The angle at which the simple region box will be rotated in degrees, this is the negitive of Tele_Rot_Ang
        Cur_Shape_Tele='box('+str(Midpoint_X)+','+str(Midpoint_Y)+','+ str(D) +','+str(D)+','+str(Angle_Tele)+')' + '\n' #Cur_Shape_Tele:-str, Current_Shape_Telescope, The shape string of the current CCD polygon with the Angle_Tele used instead of Angle
        #print Angle_Tele
        Angle_Tele_Rad=np.radians(Angle_Tele) #Angle_Tele_Rad:-numpy.float64, Angle_Telescope_Radians, The angle at which the simple region box will be rotated in radians
        #print Angle_Tele_Rad
        #print type(Angle_Tele_Rad)
        #print Cur_Shape
        #file.write(Cur_Shape)
        #file.write(Cur_Shape_Tele)
        Shape_List.append(Cur_Shape) #Appends the current shape string to Shape_List
        Cur_Shape_Data=[[Midpoint_X,Midpoint_Y],D,Angle] #Cur_Shape_Data:-List, Current_Shape_Data, The all the data needed to generate a simple CCD region in a list in the form [[Midpoint_X,Midpoint_Y],D,Angle]
        Shape_Data_L.append(Cur_Shape_Data) #Shape_Data_L:-Appends the Current_Shape_Data to Shape_Data_L
    #print Shape_List
    #print "Shape_Data_L ", Shape_Data_L
    Midpoint_List=[] #Midpoint_List:-List, Midpoint_List, The list of all Simple CCD region midpoints in an observation
    """
    This part of the code make the Big Midpoint, The Midpoint of all the Simple CCD regions in an observation wether or not those CCD regions are connected
    """
    for Shape_Data in Shape_Data_L: #Shape_Data:-List, Shape_Data, The Shape_Data of the current Simple CCD reigon in the Shape_Data_L
        Cur_Midpoint=Shape_Data[0] #Cur_Midpoint:-List, Current_Midpoint, The midpoint of the current Simple CCD region
        #Cur_Midpoint_X=Cur_Midpoint[0]
        #Cur_Midpoint_Y=Cur_Midpoint[1]
        Midpoint_List.append(Cur_Midpoint) #Appends the current Simple CCD region midpoint to Midpoint_List
    #print Midpoint_List
    Big_Midpoint=np.mean(Midpoint_List, axis=0) #Big_Midpoint:-numpy.ndarray, Big_Midpoint, The Midpoint of all the Simple CCD regions in an observation wether or not those CCD regions are connected, This might be an output for this function and could be used as the center point for where the Aera_Calc code centers it's annuli
    #print type(Big_Midpoint)
    #print Big_Midpoint #This is the Midpoint of all the CCDs in the FOV wether they are connected to each other or not
    """
    This part of the code trys to find what Simple CCD Regions are directly connected to each other, ie. they are overlaping, and returns as list of all overlaping connections between the Simple CCD Regions in the observation
    Addationally this part of the code makes a list of all Simple CCD Regions that are not overlaping with any other Simple CCD Regions, The CCDs are repersented by the indexs h and i, where the h index is the index for the Current Simple CCD Region and the i index is the index for the Current Test CCD Region.
    Indexs i and h refer to the Shape_Data_L
    """
    Midpoint_Connected_L=[]
    #for Shape_Data in Shape_Data_L:
    CCD_Connection_Info_L=[] #CCD_Connection_Info_L:-List, CCD_Connection_Infomation_List, The list of all CCD Connection Info Lists in the observation, in the form [[Direction_String1,[h1,i1],Side_Gap_X1],[Direction_String2,[h2,i2],Side_Gap_X2],...[Direction_Stringn,[hn,in],Side_Gap_Xn]]
    CCD_Not_Connected_Inx_L=[]
    for h in range(0,len(Shape_Data_L)): #h:-int, h, The index before i, ie. for h in range NOT H as in hight axis, indexs refer to Shape_Data_L
        Connected_Bool=False #Connected_Bool:-bool, Connected_Boolean, A boolean statement that is True when the current Simple CCD region is conferimed to be connected (by overlaping ONLY in the H direction OR the L direction, not both H & L) to another Simple CCD Region
        Shape_Data=Shape_Data_L[h] #Shape_Data:-List, Shape_Data, The current Shape_Data in Shape_Data_L
        Cur_Midpoint=Shape_Data[0] #Cur_Midpoint:-List, Current_Midpoint, The midpoint of the current Simple CCD Region in Shape_Data_L
        Cur_Midpoint_X=Cur_Midpoint[0] #Cur_Midpoint_X:-numpy.float64, Current_Midpoint_X, The X value of the midpoint of the current Simple CCD Region in Shape_Data_L in pixels
        #print type(Cur_Midpoint_X)
        Cur_Midpoint_Y=Cur_Midpoint[1] #Cur_Midpoint_Y:-numpy.float64, Current_Midpoint_Y, The Y value of the midpoint of the current Simple CCD Region in Shape_Data_L in pixels
        """
        The X-axis and the Y_axis are the physical coordinates refering to the observation itself, The Y-axis always points North and the X-axis (always points East(?) or West(?))
        The origin point of the X and Y Axes is the bottom Left corner of the image. The Simple CCD Regions are box regions in the form "box(xcenter,ycenter,width,height,angle)" Where the midpoint of the box region is simply
        the X and Y coordinates the Simple CCD Region is in pixels, This is not so simple for the width and hight of the box because the width and hight of the box are repersented in the coordinates relative to the box itself, INDEPENDENTLY from the rotation of the box
        Ie. width and hight of the box is using the coordinate frame of the box itself NOT the coordinate frame of the observation. Therefore new axes must be defined when talking about box coordinates,
        Thus the "H" Direction is the hight direction and is always parallel to the hight of the box and the "L" Direction is the Width Direction (The word "Length" is being used instead of width) and is always parallel to the Width of the box
        The rotation angle, "angle" is the rotation angle the box is rotated, Ie. the angle between the two differnt coordinate frames (X & Y axes and L & H axes). It is often necessary in this code to coordinates from one type of coordinate system to another and to do this
        a rotation of axes trasformation is used to change the X and Y coordinates to L and H coordinates and vice versa, The equations used to do this in both direction are listed below

        for X and Y to L and H:

        X_Rot=(X*np.cos(Angle_Tele_Rad))+(Y*np.sin(Angle_Tele_Rad))
        Y_Rot=(-X*np.sin(Angle_Tele_Rad))+(Y*np.cos(Angle_Tele_Rad))

        for L and H to X and Y:

        X=(X_Rot*np.cos(Angle_Tele_Rad))+(-Y_Rot*np.sin(Angle_Tele_Rad)) # X_Rot is L
        Y=(X_Rot*np.sin(Angle_Tele_Rad))+(Y_Rot*np.cos(Angle_Tele_Rad)) # Y_Rot is H

        For more infomation of the rotation of axis vist
        https://en.wikipedia.org/wiki/Rotation_of_axes
        """
        Cur_Midpoint_X_Rot=(Cur_Midpoint_X*np.cos(Angle_Tele_Rad))+(Cur_Midpoint_Y*np.sin(Angle_Tele_Rad)) #Cur_Midpoint_X_Rot:-numpy.float64, Current_Midpoint_X_Rotated, The X value of the midpoint of the Simple CCD region in box coordinates, ie The L value of the midpoint
        Cur_Midpoint_Y_Rot=(-Cur_Midpoint_X*np.sin(Angle_Tele_Rad))+(Cur_Midpoint_Y*np.cos(Angle_Tele_Rad)) #Cur_Midpoint_Y_Rot:-numpy.float64, Current_Midpoint_Y_Rotated, The Y value of the midpoint of the Simple CCD region in box coordinates, ie The H value of the midpoint
        Cur_D=Shape_Data[1] #Cur_D:-numpy.float64, Current_D, The side distance of the current Simple CCD region
        #print type(Cur_D)
        Cur_Rot=Shape_Data[2] #Cur_Rot:-numpy.float64, Current_Rotation, The rotation of the current Simple CCD region
        #print type(Cur_Rot)
        #print "Cur_Midpoint ", Cur_Midpoint
        for i in range(0,len(Shape_Data_L)): # i, i, The 'ith' index in the Shape_Data_L
            if(i!=h): # Makes sure that the Current Simple CCD Region is not the Current Test Simple CCD Region
                Shape_Data_Test=Shape_Data_L[i] #Shape_Data_Test:-List, Shape_Data_Test, The current test Shape_Data in Shape_Data_L
                Cur_Midpoint_Test=Shape_Data_Test[0] #Cur_Midpoint_Test:-List, Current_Midpoint_Test, The midpoint of the current Test Simple CCD Region in Shape_Data_L
                Cur_Midpoint_X_Test=Cur_Midpoint_Test[0] #Cur_Midpoint_X_Test:-numpy.float64, Current_Midpoint_X_Test, The X value of the midpoint of the current test Simple CCD Region in Shape_Data_L in pixels #Need to Rotate
                #print type(Cur_Midpoint_X_Test)
                Cur_Midpoint_Y_Test=Cur_Midpoint_Test[1] #Cur_Midpoint_Y_Test:-numpy.float64, Current_Midpoint_Y_Test, The Y value of the midpoint of the current test Simple CCD Region in Shape_Data_L in pixels #Need to Rotate
                Cur_Midpoint_X_Rot_Test=(Cur_Midpoint_X_Test*np.cos(Angle_Tele_Rad))+(Cur_Midpoint_Y_Test*np.sin(Angle_Tele_Rad)) #Cur_Midpoint_X_Rot_Test:-numpy.float64, Current_Midpoint_X_Rotated_Test, The X value of the midpoint of the Test Simple CCD region in box coordinates, ie The L value of the midpoint
                Cur_Midpoint_Y_Rot_Test=(-Cur_Midpoint_X_Test*np.sin(Angle_Tele_Rad))+(Cur_Midpoint_Y_Test*np.cos(Angle_Tele_Rad)) #Cur_Midpoint_Y_Rot_Test:-numpy.float64, Current_Midpoint_Y_Rotated_Test, The Y value of the midpoint of the Test Simple CCD region in box coordinates, ie The H value of the midpoint
                Cur_D_Test=Shape_Data_Test[1] #Cur_D_Test:-numpy.float64, Current_D_Test, The side distance of the current Test Simple CCD region
                Cur_Rot_Test=Shape_Data_Test[2] #Cur_Rot_Test:-numpy.float64, Current_Rotation_Test, The rotation of the current Test Simple CCD region
                Shape_Dist_X=np.absolute(Cur_Midpoint_X-Cur_Midpoint_X_Test) #Shape_Dist_X:-numpy.float64, Shape_Distance_X, This distance between the Current CCD Simple Region and the Current Test CCD Simple Region in the X-Direction #Change to rotated coordinates
                Shape_Dist_Y=np.absolute(Cur_Midpoint_Y-Cur_Midpoint_Y_Test) #Shape_Dist_Y:-numpy.float64, Shape_Distance_Y, This distance between the Current CCD Simple Region and the Current Test CCD Simple Region in the Y-Direction #Change to rotated coordinates
                Shape_Dist_X_Rot=np.absolute(Cur_Midpoint_X_Rot-Cur_Midpoint_X_Rot_Test) #Shape_Dist_X_Rot:-numpy.float64, Shape_Distance_X_Rotated, This distance between the Current CCD Simple Region and the Current Test CCD Simple Region in the L-Direction #Change to rotated coordinates
                Shape_Dist_Y_Rot=np.absolute(Cur_Midpoint_Y_Rot-Cur_Midpoint_Y_Rot_Test) #Shape_Dist_Y_Rot:-numpy.float64, Shape_Distance_Y_Rotated, This distance between the Current CCD Simple Region and the Current Test CCD Simple Region in the H-Direction #Change to rotated coordinates
                #Shape_Dist_X_Rot_Coords=(Shape_Dist_X*np.cos(Angle_Tele_Rad))+(Shape_Dist_Y*np.sin(Angle_Tele_Rad)) #This is NOT working
                #Shape_Dist_Y_Rot_Coords=(-Shape_Dist_X*np.sin(Angle_Tele_Rad))+(Shape_Dist_Y*np.cos(Angle_Tele_Rad)) #This is NOT working
                Total_Reach=(Cur_D/2.0)+(Cur_D_Test/2.0) #Total_Reach:-numpy.float64, Total_Reach, The total amount of the reach distance both the Current Simple CCD Region and Test CCD Region have away from the center of their Simple CCD region (Since the Simple CCD Regions are sqaures) combined
                #print type(Total_Reach)
                Side_Gap_X=Shape_Dist_X_Rot-Total_Reach #Side_Gap_X:-numpy.float64, Side_Gap_X, The gap in the L direction between the Current Simple CCD Region and the Current Test Simple CCD Region
                Side_Gap_Y=Shape_Dist_Y_Rot-Total_Reach #Side_Gap_Y:-numpy.float64, Side_Gap_Y, The gap in the H direction between the Current Simple CCD Region and the Current Test Simple CCD Region
                #print "Shape_Dist_X ", Shape_Dist_X #I have to reject the cases where the Current and Test Shape are the same shape ie. The same CCD
                #print "Shape_Dist_X ", Shape_Dist_Y #I have to reject the cases where the Current and Test Shape are the same shape ie. The same CCD
                #print i
                #print "Angle_Tele_Rad ", Angle_Tele_Rad
                #print "Shape_Dist_X_Rot_Coords ", Shape_Dist_X_Rot_Coords
                #print "Shape_Dist_Y_Rot_Coords ", Shape_Dist_Y_Rot_Coords
                #print "Cur_Midpoint ", Cur_Midpoint
                #print "Cur_Midpoint_Test", Cur_Midpoint_Test
                #print "Shape_Dist_X_Rot ", Shape_Dist_X_Rot
                #print "Shape_Dist_Y_Rot ", Shape_Dist_Y_Rot
                #print "Total_Reach ", Total_Reach
                #print "Side_Gap_X ", Side_Gap_X
                #print "Side_Gap_Y ", Side_Gap_Y
                if((Side_Gap_X<0.0) and (Shape_Dist_Y_Rot<5.0)): #Checks to see if the Current Simple CCD Region and the Current Test Simple CCD Region are connected in the L direction
                    Cur_Con_Info_X=['L',[h,i],Side_Gap_X] #Cur_Con_Info_X:-List, Current_Connection_Infomation_X, The important infomation about the CCD connection in a list in the form [Direction_String,[h,i],Side_Gap_X], for this line in the code the connection must be made in the L direction, so it is in the form ['L',[h,i],Side_Gap_X], The h index and i index refer to Shape_Data_L
                    CCD_Connection_Info_L.append(Cur_Con_Info_X) #CCD_Connection_Info_L:-Appends the current Current_Connection_Infomation_X to the CCD_Connection_Info_L
                    Connected_Bool=True #Sets Connected_Bool equal to True because a connection for the current CCD was found
                if((Side_Gap_Y<0.0) and (Shape_Dist_X_Rot<5.0)): #Checks to see if the Current Simple CCD Region and the Current Test Simple CCD Region are connected in the H direction
                    Cur_Con_Info_Y=['H',[h,i],Side_Gap_Y] #Cur_Con_Info_Y:-List, Current_Connection_Infomation_Y, The important infomation about the CCD connection in a list in the form [Direction_String,[h,i],Side_Gap_X], for this line in the code the connection must be made in the H direction, so it is in the form ['H',[h,i],Side_Gap_X], The h index and i index refer to Shape_Data_L
                    CCD_Connection_Info_L.append(Cur_Con_Info_Y) #CCD_Connection_Info_L:-Appends the current Current_Connection_Infomation_Y to the CCD_Connection_Info_L
                    Connected_Bool=True #Sets Connected_Bool equal to True because a connection for the current CCD was found
        if(Connected_Bool==False): #Checks to see if the Current CCD Region is not connnected (overlaping) any other Simple CCD Region
            CCD_Not_Connected_Inx_L.append(h) #Apppends the h index (ref. Shape_Data_L) of the current not Unconnected Simple CCD Region
    #print CCD_Connection_Info_L
    #print len(CCD_Connection_Info_L)
    #print "CCD_Not_Connected_Inx_L ", CCD_Not_Connected_Inx_L
    CCD_Connection_Info_L_Cor=CCD_Connection_Info_L #CCD_Connection_Info_L_Cor:-List, CCD_Connection_Infomation_List_Corrected, The CCD_Connection_Info_L with (or for this line to have) the reverse duplicate connections removed, ie. a connection from [h=1,i=2] is the same connection as [h=2,i=1], thus [h=2,i=1] must be removed (i and h ref. Shape_Data_L)
    for CCD_Con_I in CCD_Connection_Info_L: #CCD_Con_I:-List, CCD_Connection_Infomation, The current CCD_Connection_Infomation in the CCD_Connection_Info_L
        Con_Inx=CCD_Con_I[1] #Con_Inx:-List, Connected_Indexs, The connection between the 2 Simple CCD Regions in index form (ref. Shape_Data_L) in the form [h,i](?)
        Con_Inx_Rev=Con_Inx[::-1] #Con_Inx_Rev:-List, Connected_Indexs_Reversed, The reverse duplicate of the current Connected_Indexs in the form [i,h] (ref. Shape_Data_L)
        for CCD_C_I in CCD_Connection_Info_L: #CCD_C_I:-List, CCD_Connection_Infomation, The current CCD_Connection_Infomation in the CCD_Connection_Info_L, This is the test variable
            C_Inx=CCD_C_I[1] #C_Inx:-List, Connected_Indexs, The connection between the 2 Simple CCD Regions in index form (ref. Shape_Data_L) in the form [h,i](?), This is the test variable
            if(C_Inx==Con_Inx_Rev): #Checks to see if the current test CCD_Connection_Infomation is the current reverse duplicate
                CCD_Connection_Info_L_Cor.remove(CCD_C_I) #removes the Test CCD_Connection_Infomation if it is the current reverse duplicate
    #print CCD_Connection_Info_L_Cor
    """
    This part of the code finds what Simple CCD Regions are connected even if they are not connected directly, For example, for this connection [[1,2],[2,3]] there are 2 overlaping connections [1,2] and [2,3]
    but all the Simple CCD Regions (1,2,3,4) are connected together. This part of the code represents these connections by making a high list containing a list of all connections with each connection represented
    by a list of the overlaping connection info that make up that connection. For example,
    Con_CCD_L=[[['H', [0, 6], -89.678830390294934], ['L', [6, 8], -86.701839492347972], ['H', [7, 8], -89.678850781059282], ['L', [0, 7], -86.701827651676012]], [['L', [1, 2], -46.737718388440953], ['L', [2, 3], -45.082838638291832], ['L', [3, 4], -47.718913732848023], ['L', [4, 5], -47.447099197318266]]]
    """
    Con_CCD_L=[] #A list of the lists of connected CCDs
    #for i in range(0,len(CCD_Connection_Info_L_Cor)):
    i=0 # i:-int, i, The "ith" index in CCD_Connection_Info_L_Cor
    Connect_Bool=False #Connect_Bool:-bool, Connect_Boolean, True if there is a connection found (NEED BETTER DISCRIPTION HERE)
    Already_Included_B=False
    while(i<=len(CCD_Connection_Info_L_Cor)-1):
        #print i
        #print "Connect_Bool ", Connect_Bool
        #print "Already_Included_B ", Already_Included_B
        Already_Included_B=False
        #if((i==0) and (Connect_Bool==False)): #To prevent the Con_CCD_L from being wiped when only a single conection of many has been found
        if((i==0) and (Connect_Bool==False)): #These are the starting conditions, The while loop always starts with these conditions and depending on weither a conection is made or not determines what the next condtions are
            #print "Start"
            Cur_Con_CCDs=[] #Cur_Con_CCDs:-List, Current_Connected_CCDs, A list of the currently connected Simple CCD Regions or just "CCDs" for short  #A list of the current connected CCDs
            CCD_Connection_I=CCD_Connection_Info_L_Cor[i] #CCD_Connection_I:-List, CCD_Connection_Info, The current overlaping connection info, this is tested to see if there are any other overlaping connections that share the same CCD and therefore are connected together, For the staring condtions this is just the first overlaping connection in CCD_Connection_Info_L_Cor
            #print "if((i==0) and (Connect_Bool==False)): ", CCD_Connection_I
            Axis_S=CCD_Connection_I[0] #Axis_S:-str, Axis_String, The string that is either "L" or "H" to denote what direction the current overlaping connection is in
            Connection_Inx=CCD_Connection_I[1] #Connection_Inx:-List, Connection_Indexs, The current overlaping conection in index form (ref. Shape_Data_L)
            Overlap=CCD_Connection_I[2] #Overlap:-numpy.float64, Overlap, The Overlap of the current overlaping connection in pixels
            #print type(Overlap)
            Cur_Con_CCDs.append(CCD_Connection_I) #Appends the Current Simple CCD Region Connection Info onto Cur_Con_CCDs
        if(Connect_Bool==True):
            #print "Connected"
            CCD_Connection_I=CCD_Connection_I_Test_Connected #CCD_Connection_I:-List, CCD_Connection_Info, The current overlaping connection info, this is tested to see if there are any other overlaping connections that share the same CCD and therefore are connected together, For the condtions where a previous connection was found (Connect_Bool=True), This is equal to the previous test overlaping connection that was found to be connected (CCD_Connection_I_Test_Connected), This because the code is now trying to find another overlaping connection that is connected to the first 2 overlaping connections, This will keep repeating until no connections are found or when there are no more Simple CCD Regions to test (when, i=(len(CCD_Connection_Info_L_Cor)-1)  # #Keeps selecting ['L', [2, 3], -45.082838638291832], Probablly has somthing to do with CCD_Connection_I_Test_Connected vs CCD_Connection_I_Test
            #print "if(Connect_Bool==True): ", CCD_Connection_I #Keeps selecting ['L', [2, 3], -45.082838638291832], Probablly has somthing to do with CCD_Connection_I_Test_Connected
            Axis_S=CCD_Connection_I[0] #Axis_S:-str, Axis_String, The string that is either "L" or "H" to denote what direction the current overlaping connection is in
            Connection_Inx=CCD_Connection_I[1] #Connection_Inx:-List, Connection_Indexs, The current overlaping conection in index form (ref. Shape_Data_L)
            Overlap=CCD_Connection_I[2] #Overlap:-numpy.float64, Overlap, The Overlap of the current overlaping connection in pixels
            Connect_Bool=False #Resets Connect_Bool back equal to False becuase the current overlaping connection will be assummed to be disconnected until proven otherwise, in which case Connect_Bool will be set equal to True and the if(Connect_Bool==True) condtions will be used again
        elif((i!=0) and (Connect_Bool==False)): #Something is up with this condtional
            #print "New Connection"
            Cur_Con_CCDs=[] #A list of the current connected CCDs
            Already_Included_B=False
            CCD_Connection_I_in_Test=CCD_Connection_Info_L_Cor[i]
            #print "CCD_Connection_I_in_Test ", CCD_Connection_I_in_Test
            CCD_C_Inx_in_Test=CCD_Connection_I_in_Test[1]
            #print "CCD_C_Inx_in_Test ", CCD_C_Inx_in_Test
            for C_C_CCDs in Con_CCD_L:
                for CCD_Info in C_C_CCDs:
                    CCD_C_Inx=CCD_Info[1]
                    #print "CCD_C_Inx", CCD_C_Inx
                    if(CCD_C_Inx==CCD_C_Inx_in_Test):
                        Already_Included_B=True
                        #print "Aready Included ! ! !"
            for Cur_CCD_I in Cur_Con_CCDs:
                Cur_CCD_Inx=Cur_CCD_I[1]
                if(Cur_CCD_Inx==CCD_C_Inx_in_Test):
                    Already_Included_B=True
                    #print "Cur Aready Included ! ! !"
            #print "Already_Included_B ", Already_Included_B
            #if(Already_Included_B==False):
            CCD_Connection_I=CCD_Connection_Info_L_Cor[i]
            #print "if((i!=0) and (Connect_Bool==False)): ", CCD_Connection_I
            Axis_S=CCD_Connection_I[0]
            Connection_Inx=CCD_Connection_I[1]
            Overlap=CCD_Connection_I[2]
            if(Already_Included_B==False): # Only adds the first CCD if it is not already inclued in Cur_Con_CCDs
                Cur_Con_CCDs.append(CCD_Connection_I)
            if(Already_Included_B==True):
                i=i+1
            #if(Already_Included_B==True):
                #index i somehow
                #move on to the next CCD without doing anything
        #print "Already_Included_B ", Already_Included_B
        if(Already_Included_B==False): #need to fix Already inclued test and Connect_Bool Test to work under all condtions
            #print "Testing"
            for Inx in Connection_Inx: #Inx:-int, Index, The current index (ref. Shape_Data_L)
                #print "Inx ", Inx
                for j in range(0,len(CCD_Connection_Info_L_Cor)): #j:-int, j, The "jth" index in CCD_Connection_Info_L_Cor # Make sure that i!=j ?
                    CCD_Connection_I_Test=CCD_Connection_Info_L_Cor[j] #CCD_Connection_I_Test:-List, CCD_Connection_Infomation_Test, The current test overlaping connection infomation
                    Axis_S_Test=CCD_Connection_I_Test[0] #Axis_S_Test:-String, Axis_String_Test, The string that is either "L" or "H" to denote what direction the current test overlaping connection is in
                    Connection_Inx_Test=CCD_Connection_I_Test[1] #Connection_Inx_Test:-List, Connection_Indexs_Test, The current test overlaping conection in index form (ref. Shape_Data_L)
                    Overlap_Test=CCD_Connection_I_Test[2] #Overlap_Test: Overlap_Test, The Overlap of the current test overlaping connection in pixels
                    #print "Connection_Inx_Test ", Connection_Inx_Test
                    #if(i!=j):
                    if(j>i): # To exclude the possiblity of chosing itself and alreay chosen CCD_Infos, Need to fix for case that all CCDs are connected
                        #print "j ", j
                        if Inx in Connection_Inx_Test: #Checks to see if the current Index (ref. Shape_Data_L) is in the current overlaping connection in index from (ref. Shape_Data_L) # Need to exclude the possiblity of chosing itself
                            #print "Inx ", Inx
                            #print "Connection_Inx_Test ", Connection_Inx_Test
                            if(CCD_Connection_I_Test not in Cur_Con_CCDs): #Checks to see if the current overlaping connection has alreay been included in the list of currently connected CCDs, Cur_Con_CCDs
                                Connect_Bool=True #Sets Connect_Bool equal to True to indicate that a connection has been found, this means that the next current overlaping connection will be the current (as in now the the name "current") Current Test Overlaping Connection
                                CCD_Connection_I_Test_Connected=CCD_Connection_I_Test #CCD_Connection_I_Test_Connected:-List, CCD_Connection_Infomation_Test_Connected, The CCD_Connection_I_Test that is conferimed to have a connection with another overlaping connection
                                #print "CCD_Connection_I_Test_Connected ", CCD_Connection_I_Test_Connected
                                #print "Connection Conferimed"
                            else: #Does nothing if the current overlaping connection has alreay been included in the list of currently connected CCDs, Cur_Con_CCDs
                                #print "No"
                                pass
            #print "Connect_Bool After ", Connect_Bool
            if(Connect_Bool==True):
                if(CCD_Connection_I_Test_Connected not in Cur_Con_CCDs): #Checks if the newly found connected overlaping connection has already been included in the current list of connected (CCDs Cur_Con_CCDs). If the newly found connected overlaping connection has been alreay included it does nothing, if the newly found connected overlaping connection has not be already included the newly found connected overlaping connection is appended to Cur_Con_CCDs #I shouldn't do this for every index, instead every connect
                    #print "Connection_Inx_Test ", Connection_Inx_Test
                    Cur_Con_CCDs.append(CCD_Connection_I_Test_Connected) #Appends the newly found connected overlaping connection to Cur_Con_CCDs
                    #Connect_Bool=True
                    #print "One Connected"
                """
                else:
                    Connect_Bool=False
                    #print "One Not Connected"
                """
            #print "Connect_Bool ", Connect_Bool
            #print "Already_Included_B ", Already_Included_B
            if((Connect_Bool==False) and (Already_Included_B==False)):
                #if(len(Cur_Con_CCDs)>1):
                Con_CCD_L.append(Cur_Con_CCDs)
                i=i+1
                #print "One Not Connected"
            #if(Connect_Bool==True):
        #i=i+1
        #print "Cur_Con_CCDs ", Cur_Con_CCDs
        #print "Con_CCD_L ", Con_CCD_L
        #print " "
    #print Con_CCD_L
    """
    """
    Big_Shape_Info_L=[]
    Big_Shape_Str_L=[]
    for Con_CCDs in Con_CCD_L :
        Dir_Str_L=[]
        #print "Con_CCDs ", Con_CCDs
        for Cur_C_CCD_Info in Con_CCDs:
            Cur_Direction_Str=Cur_C_CCD_Info[0]
            Cur_Con_Inxs=Cur_C_CCD_Info[1]
            Cur_CCD_Overlap=Cur_C_CCD_Info[2]
            Dir_Str_L.append(Cur_Direction_Str)
        In_Line_Bool=True
        for i in range(1,len(Dir_Str_L)): #Not sure if starting at i=1 will work
            Start_Dir_Str=Dir_Str_L[0]
            Dir_Str_Test=Dir_Str_L[i]
            if(Start_Dir_Str!=Dir_Str_Test):
                In_Line_Bool=False
        if(In_Line_Bool==True):
            Line_Inx_L=[]
            for Cur_Con_Line_CCD in Con_CCDs:
                #Cur_Line_Dir=Cur_Con_Line_CCD[0]
                Cur_Line_Con_Inxs=Cur_Con_Line_CCD[1]
                #Cur_Line_Overlap=Cur_Con_Line_CCD[2]
                for Line_Inx in Cur_Line_Con_Inxs:
                    if(Line_Inx not in Line_Inx_L):
                        Line_Inx_L.append(Line_Inx)
            #print Line_Inx_L
            Line_Shape_Data_L=[]
            for Line_Index in Line_Inx_L:
                #print len(Shape_Data_L)
                #print "Hello_World"
                Cur_Line_Shape_Data=Shape_Data_L[Line_Index]
                Line_Shape_Data_L.append(Cur_Line_Shape_Data)
            #print Line_Shape_Data_L
            Line_Midpoint_L=[]
            D_Line_List=[]
            for Line_Shape_Data in Line_Shape_Data_L:
                Cur_Line_Midpoint=Line_Shape_Data[0]
                Cur_Line_D=Line_Shape_Data[1]
                Line_Midpoint_L.append(Cur_Line_Midpoint)
                #Total_D=Total_D+Cur_Line_D
                D_Line_List.append(Cur_Line_D)
            Big_Line_Midpoint=np.mean(Line_Midpoint_L, axis=0)
            #print "Big_Line_Midpoint ", Big_Line_Midpoint
            Direction_Str=Dir_Str_L[0]
            #print "Direction_Str ", Direction_Str
            #print "Total_D ", Total_D
            #print D_Line_List
            Total_D=np.sum(D_Line_List)
            #print "Total_D ",Total_D
            Ave_D=np.mean(D_Line_List)
            #print "Ave_D ", Ave_D
            Line_Overlap_L=[]
            for Cur_C_Line_CCD_Info in Con_CCDs:
                Cur_Line_OLap=Cur_C_Line_CCD_Info[2]
                Line_Overlap_L.append(Cur_Line_OLap)
            #print Line_Overlap_L
            Total_Overlap=np.sum(Line_Overlap_L)
            #print "Total_Overlap ", Total_Overlap
            Total_D_Corrected=Total_D+Total_Overlap #Total_Overlap is always negitive
            #print "Total_D_Corrected ", Total_D_Corrected
            if(Direction_Str=="L"):
                Big_Shape_Info=[Big_Line_Midpoint,Total_D_Corrected,Ave_D,Angle_Tele] # I don't know if Angle_Tele is correct
                Big_Shape_Info_L.append(Big_Shape_Info)
                Big_Shape_Str='box('+str(Big_Line_Midpoint[0])+','+str(Big_Line_Midpoint[1])+','+ str(Total_D_Corrected) +','+str(Ave_D)+','+str(Angle_Tele)+')' + '\n'
                Big_Shape_Str_L.append(Big_Shape_Str)
            if(Direction_Str=="H"):
                Big_Shape_Info=[Big_Line_Midpoint,Total_D_Corrected,Ave_D,Angle_Tele] # I don't know if Angle_Tele is correct
                Big_Shape_Info_L.append(Big_Shape_Info)
                Big_Shape_Str='box('+str(Big_Line_Midpoint[0])+','+str(Big_Line_Midpoint[1])+','+ str(Ave_D) +','+str(Total_D_Corrected)+','+str(Angle_Tele)+')' + '\n'
                Big_Shape_Str_L.append(Big_Shape_Str)
            #print Big_Shape_Str_L
        if(In_Line_Bool==False):
            #print "Hello_World"
            if(len(Con_CCDs)==4):
                #Insert Square Code
                #print "Square Con_CCDs ", Con_CCDs
                L_Direction_Square_L=[]
                H_Direction_Square_L=[]
                for Cur_Con_Square_CCD in Con_CCDs:
                    Cur_Direction_Square_Str=Cur_Con_Square_CCD[0]
                    if(Cur_Direction_Square_Str=="L"):
                        L_Direction_Square_L.append(Cur_Con_Square_CCD)
                    if(Cur_Direction_Square_Str=="H"):
                        H_Direction_Square_L.append(Cur_Con_Square_CCD)
                #print "L_Direction_Square_L ", L_Direction_Square_L
                #print "H_Direction_Square_L ", H_Direction_Square_L
                Con_CCDs_Axis_Org=[L_Direction_Square_L,H_Direction_Square_L]
                Cur_Square_Shape_Data_Axis_Org_L=[]
                Cur_Square_Con_Inxs_Axis_Org_L=[]
                for Con_CCD_In_Dir_L in Con_CCDs_Axis_Org: # L is i=0, H is i=1
                    Cur_Square_Shape_Data_In_Dir_L=[]
                    Cur_Square_Con_Inxs_L=[]
                    for Cur_C_Square_CCD in Con_CCD_In_Dir_L:
                        #print "Cur_C_Square_CCD ", Cur_C_Square_CCD
                        #Cur_Square_Direction=Cur_C_Square_CCD[0]
                        Cur_Square_Con_Inxs=Cur_C_Square_CCD[1]
                        Cur_Square_Con_Inxs_L.append(Cur_Square_Con_Inxs)
                        #print "Cur_Square_Con_Inxs ", Cur_Square_Con_Inxs
                        #Cur_Square_Overlap=Cur_C_Square_CCD[2]
                        #print "Cur_Square_Con_Inxs ", Cur_Square_Con_Inxs
                        Cur_Square_Shape_Data_L=[]
                        for Square_Inx in Cur_Square_Con_Inxs:
                            #print "Square_Inx ", Square_Inx
                            Cur_Square_Shape_Data=Shape_Data_L[Square_Inx]
                            #Cur_Square_Shape_Data.append(Square_Inx) #I don't know if I should do this, For some reason it seems to append 2 copies of the same index for each CCD
                            #del Cur_Square_Shape_Data[len(Cur_Square_Shape_Data)-1]
                            Cur_Square_Shape_Data_L.append(Cur_Square_Shape_Data)
                        #print "Cur_Square_Shape_Data_L ", Cur_Square_Shape_Data_L
                        Cur_Square_Shape_Data_In_Dir_L.append(Cur_Square_Shape_Data_L)
                        #Cur_Square_Shape_Data_In_Dir_L.append(Cur_Square_Overlap)
                    #print "Cur_Square_Shape_Data_In_Dir_L ", Cur_Square_Shape_Data_In_Dir_L
                    Cur_Square_Shape_Data_Axis_Org_L.append(Cur_Square_Shape_Data_In_Dir_L)
                    Cur_Square_Con_Inxs_Axis_Org_L.append(Cur_Square_Con_Inxs_L)
                #print "Cur_Square_Shape_Data_Axis_Org_L ", Cur_Square_Shape_Data_Axis_Org_L
                #print "Cur_Square_Con_Inxs_Axis_Org_L ", Cur_Square_Con_Inxs_Axis_Org_L
                Midpoints_Square_Axis_Org_L=[]
                #for CCD_Con_In_Dir_L in Cur_Square_Shape_Data_Axis_Org_L:
                D_Total_Cor_Square_L=[]
                for i in range(0,len(Cur_Square_Shape_Data_Axis_Org_L)):
                    CCD_Con_In_Dir_L=Cur_Square_Shape_Data_Axis_Org_L[i]
                    Cur_Square_Dir_Inxs=Cur_Square_Con_Inxs_Axis_Org_L[i]
                    #print "Cur_Square_Dir_Inxs ", Cur_Square_Dir_Inxs
                    Cur_Con_Square_Total_D_L=[]
                    Cur_Con_Square_Total_D_Cor_L=[]
                    Midpoint_Cur_Dir_L=[]
                    #for Cur_Con_CCDs_Square in CCD_Con_In_Dir_L:
                    for j in range(0,len(CCD_Con_In_Dir_L)):
                        Cur_Con_CCDs_Square=CCD_Con_In_Dir_L[j]
                        Cur_Con_Inxs_Square=Cur_Square_Dir_Inxs[j]
                        #print "Cur_Con_Inxs_Square ", Cur_Con_Inxs_Square
                        Cur_Con_D_Square_L=[]
                        #for Cur_CCD_Square in Cur_Con_CCDs_Square:
                        for k in range(0,len(Cur_Con_CCDs_Square)):
                            Cur_CCD_Square=Cur_Con_CCDs_Square[k]
                            Cur_Inx_Square=Cur_Con_Inxs_Square[k]
                            #print "Cur_CCD_Square ", Cur_CCD_Square
                            #print "Cur_Inx_Square ", Cur_Inx_Square
                            Cur_CCD_Square_Midpoint=Cur_CCD_Square[0]
                            Cur_CCD_Square_D=Cur_CCD_Square[1]
                            Cur_Con_D_Square_L.append(Cur_CCD_Square_D)
                            Midpoint_Cur_Dir_L.append(Cur_CCD_Square_Midpoint)
                        #print "Cur_Con_D_Square_L ", Cur_Con_D_Square_L
                        Cur_Con_Sqaure_Total_D=np.sum(Cur_Con_D_Square_L)
                        Cur_Con_Square_Total_D_L.append(Cur_Con_Sqaure_Total_D)
                        #print "Cur_Con_Sqaure_Total_D ", Cur_Con_Sqaure_Total_D
                        #print "Con_CCDs_Axis_Org ", Con_CCDs_Axis_Org
                        for C_CCD_In_Dir_L in Con_CCDs_Axis_Org: # L is i=0, H is i=1
                            #print "C_CCD_In_Dir_L ", C_CCD_In_Dir_L
                            for C_C_Square_CCD in C_CCD_In_Dir_L:
                                #print "C_C_Square_CCD ", C_C_Square_CCD
                                Cur_Square_Inxs_Test=C_C_Square_CCD[1]
                                Cur_Overlap_Square_Test=C_C_Square_CCD[2]
                                if(Cur_Square_Inxs_Test==Cur_Con_Inxs_Square):
                                    Cur_Overlap_Square=Cur_Overlap_Square_Test
                                    #print "Cur_Square_Inxs_Test ", Cur_Square_Inxs_Test
                                    #print "Cur_Overlap_Square ", Cur_Overlap_Square
                        Cur_Con_Square_Total_D_Cor=Cur_Con_Sqaure_Total_D+Cur_Overlap_Square #Cur_Overlap_Square is always negitive
                        #print "Cur_Con_Square_Total_D_Cor ", Cur_Con_Square_Total_D_Cor
                        Cur_Con_Square_Total_D_Cor_L.append(Cur_Con_Square_Total_D_Cor)
                        #print "Cur_Con_Square_Total_D_Cor_L ", Cur_Con_Square_Total_D_Cor_L
                    Cur_Dir_D_Total_Cor_Square=np.mean(Cur_Con_Square_Total_D_Cor_L)
                    #print "Cur_Dir_D_Total_Cor_Square ", Cur_Dir_D_Total_Cor_Square
                    D_Total_Cor_Square_L.append(Cur_Dir_D_Total_Cor_Square)
                    #print "Midpoints_Square_Axis_Org_L ", Midpoints_Square_Axis_Org_L
                    #print "Midpoints_Square_Axis_Org_L[0] ", Midpoints_Square_Axis_Org_L[0]
                    #print "D_Total_Cor_Square_L ", D_Total_Cor_Square_L
                    #Midpoint_Cur_Dir_L.append()
                    Midpoints_Square_Axis_Org_L.append(Midpoint_Cur_Dir_L)
                #print "Midpoints_Square_Axis_Org_L ", Midpoints_Square_Axis_Org_L
                #print "D_Total_Cor_Square_L ", D_Total_Cor_Square_L
                D_In_L_Direcion=D_Total_Cor_Square_L[0]
                #print "D_In_L_Direcion ", D_In_L_Direcion
                D_In_H_Direcion=D_Total_Cor_Square_L[1]
                #print "D_In_H_Direcion ", D_In_H_Direcion
                Midpoints_Square=Midpoints_Square_Axis_Org_L[0]
                #print "Midpoints_Square ", Midpoints_Square
                Big_Midpoint_Square=np.mean(Midpoints_Square, axis=0)
                #print "Big_Midpoint_Square ", Big_Midpoint_Square
                Big_Shape_Info=[Big_Midpoint_Square,D_In_L_Direcion,D_In_H_Direcion,Angle_Tele] # I don't know if Angle_Tele is correct
                Big_Shape_Info_L.append(Big_Shape_Info)
                Big_Shape_Str='box('+str(Big_Midpoint_Square[0])+','+str(Big_Midpoint_Square[1])+','+ str(D_In_L_Direcion) +','+str(D_In_H_Direcion)+','+str(Angle_Tele)+')' + '\n'
                Big_Shape_Str_L.append(Big_Shape_Str)
                #print "Big_Shape_Info ", Big_Shape_Info
                #print "Big_Shape_Str ", Big_Shape_Str
                #Big_Shape_Str_L.append(Big_Shape_Str)
                #L_Direction_Square_L
                #print "Square"
            if(len(Con_CCDs)==2):
                #print "Corner"
                #print Con_CCDs
                L_Direction_Corner_Con="Null L Direction"
                H_Direction_Corner_Con="Null H Direction"
                #L_Direction_Corner_L=[]
                #H_Direction_Corner_L=[]
                for Cur_Con_Corner_CCD in Con_CCDs:
                    Cur_Corner_Dir_Str=Cur_Con_Corner_CCD[0]
                    #print "Cur_Corner_Dir_Str ", Cur_Corner_Dir_Str
                    Cur_Corner_Con_Inxs=Cur_Con_Corner_CCD[1]
                    #print "Cur_Corner_Con_Inxs ", Cur_Corner_Con_Inxs
                    Cur_Corner_Overlap=Cur_Con_Corner_CCD[2]
                    #print "Cur_Corner_Overlap ", Cur_Corner_Overlap
                    if(Cur_Corner_Dir_Str=="L"):
                        #L_Direction_Corner_L.append(Cur_Con_Corner_CCD)
                        L_Direction_Corner_Con=Cur_Con_Corner_CCD
                        #print "L_Direction_Corner_Con ", L_Direction_Corner_Con
                    if(Cur_Corner_Dir_Str=="H"):
                        #H_Direction_Corner_L.append(Cur_Con_Corner_CCD)
                        H_Direction_Corner_Con=Cur_Con_Corner_CCD
                        #print "H_Direction_Corner_Con ", H_Direction_Corner_Con
                #print "L_Direction_Corner_Con ", L_Direction_Corner_Con
                #print "H_Direction_Corner_Con ", H_Direction_Corner_Con
                L_Dir_Inxs=L_Direction_Corner_Con[1]
                L_Dir_Overlap=L_Direction_Corner_Con[2]
                H_Dir_Inxs=H_Direction_Corner_Con[1]
                H_Dir_Overlap=H_Direction_Corner_Con[2]
                #print "L_Dir_Inxs ", L_Dir_Inxs
                #print "L_Dir_Overlap ", L_Dir_Overlap
                #print "H_Dir_Inxs ", H_Dir_Inxs
                #print "H_Dir_Overlap ", H_Dir_Overlap
                H_Dir_Corner_Shape_Data_L=[]
                for H_Dir_Corner_Inx in H_Dir_Inxs:
                    #print "H_Dir_Corner_Inx ", H_Dir_Corner_Inx
                    Cur_H_Dir_Corner_Shape_Data=Shape_Data_L[H_Dir_Corner_Inx]
                    H_Dir_Corner_Shape_Data_L.append(Cur_H_Dir_Corner_Shape_Data)
                #print "H_Dir_Corner_Shape_Data_L ", H_Dir_Corner_Shape_Data_L
                H_Dir_Corner_Midpoint_L=[]
                H_Dir_Corner_D_L=[]
                for H_Dir_Corner_Shape_Data in H_Dir_Corner_Shape_Data_L:
                    Cur_H_Dir_Corner_Midpoint=H_Dir_Corner_Shape_Data[0]
                    Cur_H_Dir_Corner_D=H_Dir_Corner_Shape_Data[1]
                    H_Dir_Corner_Midpoint_L.append(Cur_H_Dir_Corner_Midpoint)
                    H_Dir_Corner_D_L.append(Cur_H_Dir_Corner_D)
                #print "H_Dir_Corner_Midpoint_L ", H_Dir_Corner_Midpoint_L
                #print "H_Dir_Corner_D_L ", H_Dir_Corner_D_L
                H_Dir_Corner_Big_Midpoint=np.mean(H_Dir_Corner_Midpoint_L, axis=0)
                #print "H_Dir_Corner_Big_Midpoint ", H_Dir_Corner_Big_Midpoint
                H_Dir_Corner_Total_D=np.sum(H_Dir_Corner_D_L)
                #print "H_Dir_Corner_Total_D ", H_Dir_Corner_Total_D
                H_Dir_Corner_Total_D_Cor=H_Dir_Corner_Total_D+H_Dir_Overlap #H_Dir_Corner_Total_D_Cor
                #print "H_Dir_Corner_Total_D_Cor ", H_Dir_Corner_Total_D_Cor
                H_Dir_Corner_Ave_D=np.mean(H_Dir_Corner_D_L)
                #print "H_Dir_Corner_Ave_D ", H_Dir_Corner_Ave_D
                H_Dir_Big_Shape_Info=[H_Dir_Corner_Big_Midpoint,H_Dir_Corner_Ave_D,H_Dir_Corner_Total_D_Cor,Angle_Tele] # I don't know if Angle_Tele is correct
                Big_Shape_Info_L.append(H_Dir_Big_Shape_Info)
                H_Dir_Big_Shape_Str='box('+str(H_Dir_Corner_Big_Midpoint[0])+','+str(H_Dir_Corner_Big_Midpoint[1])+','+ str(H_Dir_Corner_Ave_D) +','+str(H_Dir_Corner_Total_D_Cor)+','+str(Angle_Tele)+')' + '\n'
                Big_Shape_Str_L.append(H_Dir_Big_Shape_Str)
                #print "H_Dir_Big_Shape_Info ", H_Dir_Big_Shape_Info
                #print "H_Dir_Big_Shape_Str ", H_Dir_Big_Shape_Str
                for L_Dir_Corner_Inx in L_Dir_Inxs:
                    if(L_Dir_Corner_Inx in H_Dir_Inxs):
                        Shared_Inx=L_Dir_Corner_Inx
                    else:
                        L_Dir_Inx=L_Dir_Corner_Inx
                #print "Shared_Inx ", Shared_Inx
                Shared_CCD_Shape_Data=Shape_Data_L[Shared_Inx]
                #print "Shared_CCD_Shape_Data ", Shared_CCD_Shape_Data
                Shared_CCD_Midpoint=Shared_CCD_Shape_Data[0]
                #print "Shared_CCD_Midpoint ", Shared_CCD_Midpoint
                Shared_CCD_X=Shared_CCD_Midpoint[0]
                #print "Shared_CCD_X ", Shared_CCD_X
                Shared_CCD_Y=Shared_CCD_Midpoint[1]
                #print "Shared_CCD_Y ", Shared_CCD_Y
                Shared_CCD_X_Rot=(Shared_CCD_X*np.cos(Angle_Tele_Rad))+(Shared_CCD_Y*np.sin(Angle_Tele_Rad))
                #print "Shared_CCD_X_Rot ", Shared_CCD_X_Rot
                Shared_CCD_Y_Rot=(-Shared_CCD_X*np.sin(Angle_Tele_Rad))+(Shared_CCD_Y*np.cos(Angle_Tele_Rad))
                #print "Shared_CCD_Y_Rot ", Shared_CCD_Y_Rot
                Shared_CCD_D=Shared_CCD_Shape_Data[1]
                #print "Shared_CCD_D ", Shared_CCD_D
                #print "L_Dir_Inx ", L_Dir_Inx
                L_Dir_Corner_Shape_Data=Shape_Data_L[L_Dir_Inx]
                #print "L_Dir_Corner_Shape_Data ", L_Dir_Corner_Shape_Data
                L_Dir_Corner_Midpoint=L_Dir_Corner_Shape_Data[0]
                #print "L_Dir_Corner_Midpoint ", L_Dir_Corner_Midpoint
                L_Dir_Corner_X=L_Dir_Corner_Midpoint[0]
                #print "L_Dir_Corner_X ", L_Dir_Corner_X
                L_Dir_Corner_Y=L_Dir_Corner_Midpoint[1]
                #print "L_Dir_Corner_Y ", L_Dir_Corner_Y
                L_Dir_Corner_D=L_Dir_Corner_Shape_Data[1]
                #print "L_Dir_Corner_D ", L_Dir_Corner_D
                L_Dir_Corner_X_Rot=(L_Dir_Corner_X*np.cos(Angle_Tele_Rad))+(L_Dir_Corner_Y*np.sin(Angle_Tele_Rad))
                #print "L_Dir_Corner_X_Rot ", L_Dir_Corner_X_Rot
                L_Dir_Corner_Y_Rot=(-L_Dir_Corner_X*np.sin(Angle_Tele_Rad))+(L_Dir_Corner_Y*np.cos(Angle_Tele_Rad))
                #print "L_Dir_Corner_Y_Rot ", L_Dir_Corner_Y_Rot
                #Insert 3-CCD Corner Shape Code
                D_Prime=L_Dir_Corner_D+L_Dir_Overlap
                #print "D_Prime ", D_Prime
                L_Dir_Overlap_Pos=abs(L_Dir_Overlap)
                #print "L_Dir_Overlap_Pos ", L_Dir_Overlap_Pos
                X_Rot_Shift=3.0
                if(L_Dir_Corner_X_Rot<Shared_CCD_X_Rot):
                    L_Dir_Corner_X_Rot_Prime=L_Dir_Corner_X_Rot-(L_Dir_Overlap_Pos/2.0)-X_Rot_Shift
                    L_Dir_Corner_Midpoint_Rot_Prime=[L_Dir_Corner_X_Rot_Prime,L_Dir_Corner_Y_Rot]
                if(L_Dir_Corner_X_Rot>Shared_CCD_X_Rot):
                    L_Dir_Corner_X_Rot_Prime=L_Dir_Corner_X_Rot+(L_Dir_Overlap_Pos/2.0)+X_Rot_Shift
                    L_Dir_Corner_Midpoint_Rot_Prime=[L_Dir_Corner_X_Rot_Prime,L_Dir_Corner_Y_Rot]
                #print "L_Dir_Corner_Midpoint_Rot_Prime ", L_Dir_Corner_Midpoint_Rot_Prime
                L_Dir_Corner_X_Rot_Prime=L_Dir_Corner_Midpoint_Rot_Prime[0]
                #print "L_Dir_Corner_X_Rot_Prime", L_Dir_Corner_X_Rot_Prime
                L_Dir_Corner_Y_Rot_Prime=L_Dir_Corner_Midpoint_Rot_Prime[1]
                #print "L_Dir_Corner_Y_Rot_Prime ", L_Dir_Corner_Y_Rot_Prime
                L_Dir_Corner_X_Prime=(L_Dir_Corner_X_Rot_Prime*np.cos(Angle_Tele_Rad))+(-L_Dir_Corner_Y_Rot_Prime*np.sin(Angle_Tele_Rad))
                #print "L_Dir_Corner_X_Prime ", L_Dir_Corner_X_Prime
                L_Dir_Corner_Y_Prime=(L_Dir_Corner_X_Rot_Prime*np.sin(Angle_Tele_Rad))+(L_Dir_Corner_Y_Rot_Prime*np.cos(Angle_Tele_Rad))
                #print "L_Dir_Corner_Y_Prime ", L_Dir_Corner_Y_Prime
                L_Dir_Corner_Midpoint_Prime=[L_Dir_Corner_X_Prime,L_Dir_Corner_Y_Prime]
                #print "L_Dir_Corner_Midpoint_Prime ", L_Dir_Corner_Midpoint_Prime
                L_Dir_Big_Shape_Info=[L_Dir_Corner_Midpoint_Prime,D_Prime,L_Dir_Corner_D,Angle_Tele] # I don't know if Angle_Tele is correct
                Big_Shape_Info_L.append(L_Dir_Big_Shape_Info)
                L_Dir_Big_Shape_Str='box('+str(L_Dir_Corner_Midpoint_Prime[0])+','+str(L_Dir_Corner_Midpoint_Prime[1])+','+ str(D_Prime) +','+str(L_Dir_Corner_D)+','+str(Angle_Tele)+')' + '\n' #Need to add the gap in between CCDs
                Big_Shape_Str_L.append(L_Dir_Big_Shape_Str)
                #print "Big_Shape_Str_L ", Big_Shape_Str_L
    #print "Big_Shape_Str_L ", Big_Shape_Str_L
    #for Big_Shape_String in Big_Shape_Str_L:
        #file.write(Big_Shape_String)
    #for Unconnected_CCD_Inx in CCD_Not_Connected_Inx_L:
    Cur_Dia_Con_L=[]
    for i in range(0,len(CCD_Not_Connected_Inx_L)): #This is not working ! ! !
        #print i
        Cur_Dia_Con=[]
        Diagonal_Con_Bool=False
        Testing_Bool=False
        Unconnected_CCD_Inx=CCD_Not_Connected_Inx_L[i]
        #print "Unconnected_CCD_Inx ", Unconnected_CCD_Inx
        Cur_Uncon_Shape_Data=Shape_Data_L[Unconnected_CCD_Inx]
        #print "Cur_Uncon_Shape_Data ", Cur_Uncon_Shape_Data
        Cur_Uncon_Midpoint=Cur_Uncon_Shape_Data[0]
        #print "Cur_Uncon_Midpoint ", Cur_Uncon_Midpoint
        Cur_Uncon_X=Cur_Uncon_Midpoint[0]
        #print "Cur_Uncon_X ", Cur_Uncon_X
        Cur_Uncon_Y=Cur_Uncon_Midpoint[1]
        #print "Cur_Uncon_Y ", Cur_Uncon_Y
        Cur_Uncon_D=Cur_Uncon_Shape_Data[1]
        #print "Cur_Uncon_D ", Cur_Uncon_D
        Cur_Uncon_CCD_Diagonal=(np.sqrt(2.0))*Cur_Uncon_D
        #print "Cur_Uncon_CCD_Diagonal ", Cur_Uncon_CCD_Diagonal
        Cur_Uncon_CCD_Diagonal_Ray=Cur_Uncon_CCD_Diagonal/2.0
        #print "Cur_Uncon_CCD_Diagonal_Ray ", Cur_Uncon_CCD_Diagonal_Ray
        Cur_Uncon_X_Rot=(Cur_Uncon_X*np.cos(Angle_Tele_Rad))+(Cur_Uncon_Y*np.sin(Angle_Tele_Rad))
        #print "Cur_Uncon_X_Rot ", Cur_Uncon_X_Rot
        Cur_Uncon_Y_Rot=(-Cur_Uncon_X*np.sin(Angle_Tele_Rad))+(Cur_Uncon_Y*np.cos(Angle_Tele_Rad))
        #print "Cur_Uncon_Y_Rot ", Cur_Uncon_Y_Rot
        for j in range(0,len(CCD_Not_Connected_Inx_L)):
            #print "j ", j
            #if(i!=j): # Is "if(j>i)"" better?
            if(j>i):
                #print "j ", j
                Testing_Bool=True
                Unconnected_CCD_Inx_Test=CCD_Not_Connected_Inx_L[j]
                #print "Unconnected_CCD_Inx_Test ", Unconnected_CCD_Inx_Test
                Cur_Uncon_Shape_Data_Test=Shape_Data_L[Unconnected_CCD_Inx_Test]
                #print "Cur_Uncon_Shape_Data_Test ", Cur_Uncon_Shape_Data_Test
                Cur_Uncon_Midpoint_Test=Cur_Uncon_Shape_Data_Test[0]
                #print "Cur_Uncon_Midpoint_Test ", Cur_Uncon_Midpoint_Test
                Cur_Uncon_X_Test=Cur_Uncon_Midpoint_Test[0]
                #print "Cur_Uncon_X_Test ", Cur_Uncon_X_Test
                Cur_Uncon_Y_Test=Cur_Uncon_Midpoint_Test[1]
                #print "Cur_Uncon_Y_Test ", Cur_Uncon_Y_Test
                Cur_Uncon_D_Test=Cur_Uncon_Shape_Data_Test[1]
                #print "Cur_Uncon_D_Test ", Cur_Uncon_D_Test
                Cur_Uncon_CCD_Diagonal_Test=(np.sqrt(2.0))*Cur_Uncon_D_Test
                #print "Cur_Uncon_CCD_Diagonal_Test ", Cur_Uncon_CCD_Diagonal_Test
                Cur_Uncon_CCD_Diagonal_Ray_Test=Cur_Uncon_CCD_Diagonal_Test/2.0
                #print "Cur_Uncon_Diagonal_Ray_Test ", Cur_Uncon_CCD_Diagonal_Ray_Test
                Cur_Uncon_X_Diff=np.absolute(Cur_Uncon_X-Cur_Uncon_X_Test)
                #print "Cur_Uncon_X_Diff ", Cur_Uncon_X_Diff
                Cur_Uncon_Y_Diff=np.absolute(Cur_Uncon_Y-Cur_Uncon_Y_Test)
                #print "Cur_Uncon_Y_Diff ", Cur_Uncon_Y_Diff
                Cur_Uncon_Dist=np.sqrt(((Cur_Uncon_X_Diff)**2.0)+((Cur_Uncon_Y_Diff)**2.0))
                #print "Cur_Uncon_Dist ", Cur_Uncon_Dist
                Diagonal_Overlap=Cur_Uncon_Dist-Cur_Uncon_CCD_Diagonal_Ray-Cur_Uncon_CCD_Diagonal_Ray_Test
                #print "Diagonal_Overlap ", Diagonal_Overlap
                Cur_Uncon_X_Rot_Test=(Cur_Uncon_X_Test*np.cos(Angle_Tele_Rad))+(Cur_Uncon_Y_Test*np.sin(Angle_Tele_Rad))
                #print "Cur_Uncon_X_Rot_Test ", Cur_Uncon_X_Rot_Test
                Cur_Uncon_Y_Rot_Test=(-Cur_Uncon_X_Test*np.sin(Angle_Tele_Rad))+(Cur_Uncon_Y_Test*np.cos(Angle_Tele_Rad))
                #print "Cur_Uncon_Y_Rot_Test ", Cur_Uncon_Y_Rot_Test
                Cur_Uncon_X_Diff_Rot=np.absolute(Cur_Uncon_X_Rot-Cur_Uncon_X_Rot_Test)
                #print "Cur_Uncon_X_Diff_Rot ", Cur_Uncon_X_Diff_Rot
                Cur_Uncon_Y_Diff_Rot=np.absolute(Cur_Uncon_Y_Rot-Cur_Uncon_Y_Rot_Test)
                #print "Cur_Uncon_Y_Diff_Rot ", Cur_Uncon_Y_Diff_Rot
                Cur_Abs_Slope_Rot=Cur_Uncon_Y_Diff_Rot/Cur_Uncon_X_Diff_Rot
                #print "Cur_Abs_Slope_Rot ", Cur_Abs_Slope_Rot
                if((Diagonal_Overlap<=0.0) and (Cur_Abs_Slope_Rot>0.95) and(Cur_Abs_Slope_Rot<1.05)):
                    Diagonal_Con_Bool=True
                    Cur_Dia_Con=[i,j]
                    Cur_Dia_Con_L.append(Cur_Dia_Con)
                    #Cur_Uncon_X_Rot_Test=(Cur_Uncon_X_Test*np.cos(Angle_Tele_Rad))+(Cur_Uncon_Y_Test*np.sin(Angle_Tele_Rad))
                    #print "Cur_Uncon_X_Rot_Test ", Cur_Uncon_X_Rot_Test
                    #Cur_Uncon_Y_Rot_Test=(-Cur_Uncon_X_Test*np.sin(Angle_Tele_Rad))+(Cur_Uncon_Y_Test*np.cos(Angle_Tele_Rad))
                    #print "Cur_Uncon_Y_Rot_Test ", Cur_Uncon_Y_Rot_Test
                    Total_Reach_Uncon=(Cur_Uncon_D/2.0)+(Cur_Uncon_D_Test/2.0)
                    #print "Total_Reach_Uncon ", Total_Reach_Uncon
                    #Cur_Uncon_X_Diff_Rot=np.absolute(Cur_Uncon_X_Rot-Cur_Uncon_X_Rot_Test)
                    #print "Cur_Uncon_X_Diff_Rot ", Cur_Uncon_X_Diff_Rot
                    Cur_Uncon_X_Rot_Overlap=Cur_Uncon_X_Diff_Rot-Total_Reach_Uncon
                    #print "Cur_Uncon_X_Rot_Overlap ", Cur_Uncon_X_Rot_Overlap
                    Cur_Uncon_X_Rot_Overlap_Pos=np.absolute(Cur_Uncon_X_Rot_Overlap)
                    #print "Cur_Uncon_X_Rot_Overlap_Pos ", Cur_Uncon_X_Rot_Overlap_Pos
                    if(Cur_Uncon_X_Rot<Cur_Uncon_X_Rot_Test):
                        #Cur_Uncon_X_Rot_Prime=Cur_Uncon_X_Rot-(Cur_Uncon_X_Rot_Overlap/2.0)-1.5
                        Cur_Uncon_X_Rot_Prime=Cur_Uncon_X_Rot-(Cur_Uncon_X_Rot_Overlap_Pos/2.0)-1.5
                        #Cur_Uncon_X_Rot_Test_Prime=Cur_Uncon_X_Rot_Test+(Cur_Uncon_X_Rot_Overlap/2.0)+1.5
                        Cur_Uncon_X_Rot_Test_Prime=Cur_Uncon_X_Rot_Test+(Cur_Uncon_X_Rot_Overlap_Pos/2.0)+1.5
                    if(Cur_Uncon_X_Rot>Cur_Uncon_X_Rot_Test):
                        #Cur_Uncon_X_Rot_Prime=Cur_Uncon_X_Rot+(Cur_Uncon_X_Rot_Overlap/2.0)+1.5
                        Cur_Uncon_X_Rot_Prime=Cur_Uncon_X_Rot+(Cur_Uncon_X_Rot_Overlap_Pos/2.0)+1.5
                        #Cur_Uncon_X_Rot_Test_Prime=Cur_Uncon_X_Rot_Test-(Cur_Uncon_X_Rot_Overlap/2.0)-1.5
                        Cur_Uncon_X_Rot_Test_Prime=Cur_Uncon_X_Rot_Test-(Cur_Uncon_X_Rot_Overlap_Pos/2.0)-1.5
                    #print "Cur_Uncon_X_Rot_Prime ", Cur_Uncon_X_Rot_Prime
                    #print "Cur_Uncon_X_Rot_Test_Prime ", Cur_Uncon_X_Rot_Test_Prime
                    Cur_Uncon_X_Prime=(Cur_Uncon_X_Rot_Prime*np.cos(Angle_Tele_Rad))-(Cur_Uncon_Y_Rot*np.sin(Angle_Tele_Rad))
                    #print "Cur_Uncon_X_Prime ", Cur_Uncon_X_Prime
                    Cur_Uncon_Y_Prime=(Cur_Uncon_X_Rot_Prime*np.sin(Angle_Tele_Rad))+(Cur_Uncon_Y_Rot*np.cos(Angle_Tele_Rad))
                    #print "Cur_Uncon_Y_Prime ", Cur_Uncon_Y_Prime
                    Cur_Uncon_X_Test_Prime=(Cur_Uncon_X_Rot_Test_Prime*np.cos(Angle_Tele_Rad))-(Cur_Uncon_Y_Rot_Test*np.sin(Angle_Tele_Rad))
                    #print "Cur_Uncon_X_Test_Prime ", Cur_Uncon_X_Test_Prime
                    Cur_Uncon_Y_Test_Prime=(Cur_Uncon_X_Rot_Test_Prime*np.sin(Angle_Tele_Rad))+(Cur_Uncon_Y_Rot_Test*np.cos(Angle_Tele_Rad))
                    #print "Cur_Uncon_Y_Test_Prime ", Cur_Uncon_Y_Test_Prime
                    Cur_Uncon_Midpoint_Prime=[Cur_Uncon_X_Prime,Cur_Uncon_Y_Prime]
                    #print "Cur_Uncon_Midpoint_Prime ", Cur_Uncon_Midpoint_Prime
                    Cur_Uncon_Midpoint_Test_Prime=[Cur_Uncon_X_Test_Prime,Cur_Uncon_Y_Test_Prime]
                    #print "Cur_Uncon_Midpoint_Test_Prime ", Cur_Uncon_Midpoint_Test_Prime
                    Diagonal_Big_Shape_Info=[Cur_Uncon_Midpoint_Prime,Cur_Uncon_D,Cur_Uncon_D,Angle_Tele] # I don't know if Angle_Tele is correct
                    #print "Diagonal_Big_Shape_Info ", Diagonal_Big_Shape_Info
                    Big_Shape_Info_L.append(Diagonal_Big_Shape_Info)
                    Diagonal_Big_Shape_Str='box('+str(Cur_Uncon_Midpoint_Prime[0])+','+str(Cur_Uncon_Midpoint_Prime[1])+','+ str(Cur_Uncon_D) +','+str(Cur_Uncon_D)+','+str(Angle_Tele)+')' + '\n'
                    #print "Diagonal_Big_Shape_Str ", Diagonal_Big_Shape_Str
                    Big_Shape_Str_L.append(Diagonal_Big_Shape_Str)
                    Diagonal_Test_Big_Shape_Info=[Cur_Uncon_Midpoint_Test_Prime,Cur_Uncon_D_Test,Cur_Uncon_D_Test,Angle_Tele] # I don't know if Angle_Tele is correct
                    #print "Diagonal_Test_Big_Shape_Info ", Diagonal_Test_Big_Shape_Info
                    Big_Shape_Info_L.append(Diagonal_Test_Big_Shape_Info)
                    Diagonal_Test_Big_Shape_Str='box('+str(Cur_Uncon_Midpoint_Test_Prime[0])+','+str(Cur_Uncon_Midpoint_Test_Prime[1])+','+ str(Cur_Uncon_D_Test) +','+str(Cur_Uncon_D_Test)+','+str(Angle_Tele)+')' + '\n'
                    #print "Diagonal_Test_Big_Shape_Str ", Diagonal_Test_Big_Shape_Str
                    Big_Shape_Str_L.append(Diagonal_Test_Big_Shape_Str)
        #print "Cur_Dia_Con_L ", Cur_Dia_Con_L
        #if((Diagonal_Con_Bool==False) and (Testing_Bool==True)): #Need to exclude case where a CCD is never tested at all
    for Uncon_Inx in CCD_Not_Connected_Inx_L:
        Inx_Included_Bool=False
        #print "Uncon_Inx ", Uncon_Inx
        for Dia_Con_Inxs in Cur_Dia_Con_L:
            #if(Uncon_Inx not in Dia_Con_Inxs): # This is flat out wrong! I need to check all the Diagonal Connections NOT just ONE ! ! !
            #if(Uncon_Inx in Dia_Con_Inxs): #This is wrong, I am comparing two differnt sets of indexs
            Cur_Isolated_CCD_Inxs_L=[]
            for Dia_Con_Inx in Dia_Con_Inxs:
                #print "Dia_Con_Inx ", Dia_Con_Inx
                Cur_Isolated_CCD_Inx=CCD_Not_Connected_Inx_L[Dia_Con_Inx]
                #print "Cur_Isolated_CCD_Inx ", Cur_Isolated_CCD_Inx
                Cur_Isolated_CCD_Inxs_L.append(Cur_Isolated_CCD_Inx)
            #print "Cur_Isolated_CCD_Inxs_L ", Cur_Isolated_CCD_Inxs_L
            if(Uncon_Inx in Cur_Isolated_CCD_Inxs_L):
                Inx_Included_Bool=True
        if(Inx_Included_Bool==False):
            #print "Uncon_Inx_Iso ", Uncon_Inx
            #print "Unconnected i ", i
            Cur_Isolated_Info=Shape_Data_L[Uncon_Inx]
            #print "Cur_Isolated_Info ", Cur_Isolated_Info
            Cur_Isolated_Midpoint=Cur_Isolated_Info[0]
            #print "Cur_Isolated_Midpoint ", Cur_Isolated_Midpoint
            Cur_Isolated_X=Cur_Isolated_Midpoint[0]
            #print "Cur_Isolated_X ", Cur_Isolated_X
            Cur_Isolated_Y=Cur_Isolated_Midpoint[1]
            #print "Cur_Isolated_Y ", Cur_Isolated_Y
            Cur_Isolated_D=Cur_Isolated_Info[1]
            #print "Cur_Isolated_D ", Cur_Isolated_D
            Uncon_Big_Shape_Info=[Cur_Isolated_Midpoint,Cur_Isolated_D,Cur_Isolated_D,Angle_Tele] # I don't know if Angle_Tele is correct
            Big_Shape_Info_L.append(Uncon_Big_Shape_Info)
            Uncon_Big_Shape_Str='box('+str(Cur_Isolated_Midpoint[0])+','+str(Cur_Isolated_Midpoint[1])+','+ str(Cur_Isolated_D) +','+str(Cur_Isolated_D)+','+str(Angle_Tele)+')' + '\n'
            Big_Shape_Str_L.append(Uncon_Big_Shape_Str)
            #print "THERE IS UNCONNECTED"
            #print "Uncon_Big_Shape_Str ", Uncon_Big_Shape_Str
    #print "Big_Shape_Str_L ", Big_Shape_Str_L
    for Big_Shape_String in Big_Shape_Str_L:
        file.write(Big_Shape_String)
        file_2.write(Big_Shape_String)





#Simple_Region_Generator('foo2','acisf03931_repro_evt2.fits')
#Simple_Region_Generator('h_Axis_Test.reg','acisf03931_repro_evt2.fits')
#Simple_Region_Generator('h_and_L_Axis_Test.reg','acisf03931_repro_evt2.fits')
#Simple_Region_Generator('3_CCD_L_Shape_Test.reg','acisf03931_repro_evt2.fits')
#Simple_Region_Generator('3_CCD_L_Shape_6_Missing_Test.reg','acisf03931_repro_evt2.fits')
#Simple_Region_Generator('Diagonal_Test.reg','acisf03931_repro_evt2.fits')
#Simple_Region_Generator('foo3','acisf13830_repro_evt2.fits')
#Simple_Region_Generator('acisf13830_Corner','acisf13830_repro_evt2.fits')
#Simple_Region_Generator('acisf13830_Unconnnected','acisf13830_repro_evt2.fits')
#Simple_Region_Generator('acisf13830_Unconnected_Alt','acisf13830_repro_evt2.fits')
#Simple_Region_Generator('The_Torture_Test.txt','acisf03931_repro_evt2.fits') #This does not work, I guess that means for subarrays all bets are off
#Simple_Region_Generator('The_Torture_Test_2.txt','acisf03931_repro_evt2.fits') #This works, but I still wouldn't bet on subarrays working
#Simple_Region_Generator('Missing_One_Square.txt','acisf03931_repro_evt2.fits')
#Simple_Region_Generator('Missing_One_Corner_Left.txt','acisf03931_repro_evt2.fits')
#Simple_Region_Generator('Missing_One_Diagonal.txt','acisf03931_repro_evt2.fits')
#Simple_Region_Generator('Missing_Two_Diagonal.txt','acisf03931_repro_evt2.fits')
#Simple_Region_Generator('The_Ultimate_Torture_Test.txt','acisf03931_repro_evt2.fits')
#Simple_Region_Generator('The_Ultimate_Torture_Test_2.txt','acisf03931_repro_evt2.fits')
#Simple_Region_Generator('acisf03931_repro_CCD_Regions','acisf03931_repro_evt2.fits')
Simple_Region_Generator('acisf13830_repro_CCD_Regions','acisf13830_repro_evt2.fits')
