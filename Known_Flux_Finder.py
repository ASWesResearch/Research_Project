from astroquery.ned import Ned
from ciao_contrib.runtool import *
from astropy.io.fits import Header
from astropy.io import fits
import pandas as pd
def Known_Flux_Finder(gname,evtfname,PIMMSfname):
    G_Data = Ned.query_object(gname) #G_Data:-astropy.table.table.Table, Galaxy_Data, The queryed data of the galaxy from NED in the form of a astropy table
    #print G_Data
    #print type(G_Data)
    raGC=float(G_Data['RA(deg)']) #raGC:-float, Right Ascension of Galatic Center, The right ascension of the galatic center of the current galaxy in degrees.
    decGC=float(G_Data['DEC(deg)']) #decGC:-float, Declination of Galatic Center, The declination of the galatic center of the current galaxy in degrees.
    dmcoords(infile=str(evtfname),ra=str(raGC), dec=str(decGC), option='cel', verbose=0, celfmt='deg') # Runs the dmcoords CIAO tool, which converts coordinates like CHIP_ID to SKY, the tool is now being used to convert the RA and Dec of the GC to SKY coodinates in pixels (?)
    X_Phys=dmcoords.x #X_Phys:-float, X_Physical, The sky plane X pixel coordinate in units of pixels of the galatic center
    Y_Phys=dmcoords.y #Y_Phys:-float, Y_Physical, The sky plane Y pixel coordinate in units of pixels of the galatic center
    Chip_ID=dmcoords.chip_id #Chip_ID:-int, Chip_ID, The Chip ID number the GC is on
    hdulist = fits.open(evtfname)
    Obs_Date_Str=hdulist[1].header['DATE-OBS']
    #print Obs_Date_Str
    #print type(Obs_Date_Str)
    Obs_Date_L=Obs_Date_Str.split("-")
    #print Obs_Date_L
    Obs_Year_Str=Obs_Date_L[0]
    Obs_Year=int(Obs_Year_Str)
    PIMMS_A=pd.read_csv('~/Desktop/PIMMS/'+PIMMSfname)
    #print PIMMS_A
    Cycle_A=PIMMS_A['Cycle']
    #print Cycle_A
    Year_A=PIMMS_A['Year']
    #print Year_A
    ACIS_I_A=PIMMS_A['ACIS-I(erg/cm**2/s)']
    #print ACIS_I_A
    ACIS_S_A=PIMMS_A['ACIS-S(erg/cm**2/s)']
    #print ACIS_S_A
    Year_L=list(Year_A)
    #print Year_L
    #Obs_Year=2006 #This is a test value
    for i in range(0,len(Year_L)):
        #print i
        if(Year_L[i]==Obs_Year):
            Row_Inx=i
            break
    #print Row_Inx
    #if((Chip_ID==3) or (Chip_ID==7)): #For Front illuminated?
    #Chip_ID=0 #This is a test value
    if(Chip_ID<4):
        Flux_A=ACIS_I_A
    if(Chip_ID>=4):
        Flux_A=ACIS_S_A
    #print Flux_A
    Flux=Flux_A[Row_Inx]
    return Flux

#Known_Flux_Finder('NGC2403','acisf02014_repro_evt2.fits','PIMMS_Data.csv')
print Known_Flux_Finder('NGC2403','acisf02014_repro_evt2.fits','PIMMS_Data.csv')
