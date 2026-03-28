##Base file from Met office (via H. Webster) and adapted by Eva Siney Jones (ESJ)
'''
PlotNAMEPlumes.py

Program for plotting inversionplumes

Loops through multiple files with different output times. 
 
Options to vary:

   * Contour levels
   * Extent of axes
   * Lat and Long Grid lines
   * Ticks on ColorBar
'''

import iris
import numpy 
import matplotlib.pyplot as plt
from matplotlib import colors
import cartopy.feature as cfeature
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import os, sys
import datetime as dt
from matplotlib.colors import BoundaryNorm
import iris.plot as iplot
from matplotlib.ticker import FormatStrFormatter, MaxNLocator

UTC_format = '%H%M%Z %d/%m/%Y'

def find_files(dir):
    ''' finds and orders the files in a directory
       returns a 2d list of file names and times for plume in datetime format
    '''

    file_list = []
    time_list = []

    for root,dirs,files in os.walk(dir):
        for name in files:
            if 'Fields_grid' in name:
               		
                file_list.append([os.path.join(root,name)])

    file_list = sorted(file_list)
    		
    return file_list
def setup_contours():      # ASH COLOUMN LOADING    

    #Contours have been changed by Eva Siney Jones (ESJ) to account for negative and positive values
    colours =[[0, 0, 255],   # blue (correspond to max negative difference)              
              [32,32,255], 
              [48,48,255], 
              [64,64,255], 
              [80,80,255], 
              [96,96,255], 
              [112,112,255], 
              [128,128,255],  
              [143,143,255], 
              [159,159,255],
              [175,175,255], 
              [191,191,255], 
              [207,207,255], 
              [223,223,255],                
              [239,239,255], 
              [255, 255, 255],   #white -> no difference in the plumes 
              [255, 255, 255],   #white -> no difference in the plumes
              [255, 239, 239],   
              [255,223,223], 
              [255,207,207], 
              [255,191,191], 
              [255,175,175], 
              [255,159,159], 
              [255,143,143], 
              [255,128,128], 
              [255,112,112], 
              [255,96,96],
              [255,80,80], 
              [255,64,64], 
              [255,48,48], 
              [255,32,32], 
              [255,16,16], 
              [255,   0,   0]] # red  (correspond to maximum positive difference)
      	       
    colours = numpy.array(colours)/255.    
    cmap = colors.ListedColormap(colours)
    #levels changed by ESJ to account for positve and negative values
    levels = [ -1000.0, -100.0, -10.0, -7.5, -5.0, -4.5, -4.0, -3.5, -3.0, -2.5, -2.0, -1.5, -1.0, -0.75, -0.5,-0.25, 0.0, 0.25, 0.5, 0.75,
             1.0, 1.5, 2.0, 2.5, 3.0,  3.5, 4.0,  4.5, 5.0, 7.5, 10.0, 100.0, 1000.0] 
    pos_norm = BoundaryNorm(levels,32) 
   
    return( cmap, levels, pos_norm)


def PlotInversionPlumes(cube1, date_object, run_date_object, timestamp, f, Tplus, PlotDir):

        plt.figure()
	# Set up axes
        ax = plt.axes(projection=ccrs.PlateCarree())


	# set map extent
        ax.set_extent([140.0, 180.0, 45.0, 65.0])        


	# Set up country outlines
        countries = cfeature.NaturalEarthFeature(
	    category='cultural',
	    name='admin_0_countries',
	    scale='50m',
	    facecolor='none')
        ax.add_feature(countries, edgecolor='black',zorder=2)

	# Set-up the gridlines
        gl = ax.gridlines(draw_labels=True, 
			  linewidth=0.8, 
			  alpha=0.9)
	
        gl.top_labels = False
        gl.right_labels = False
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER

	# Plot
        contours = setup_contours()
        cmap=contours[0]
        norm=contours[2]
        invplot = iplot.pcolormesh(cube1,cmap=cmap,norm=norm,
                           edgecolors='None',rasterized=True)
    
        cb = plt.colorbar(invplot, orientation='vertical',shrink=0.9, ticks=	[-1000.0, -100.0, -10.0, -5.0,-4.0, -3.0,-2.0,-1.0,0.0,1.0, 2.0,3.0,4.0,5.0,10.0,100.0,1000.0])	
        cb.set_label('Ash column loading difference [gm-2]', fontsize = 10)
	
        #plot location of volcano
        plt.scatter(159.44, 54.05, s=80, c='black',edgecolors='black', linewidths=0.5, marker='^', alpha=0.8,transform=ccrs.PlateCarree()) #alpha: 0 (transparent) and 1 (opaque).

        #Section below coded by ESJ
        #Find maximum ash difference value 
        max_positive=cube1.data.max() #finds largest positive difference
        max_negative=cube1.data.min() #finds largest negative difference
        max_diff=max(abs(max_positive), abs(max_negative)) #returns difference with largest magnitude

        
        text1  = "Maximum ash loading absolute difference= {:.2f}".format(max_diff) #need to find absolute difference (maximum of all differences - negative nad positive!!
        areas = iris.analysis.cartography.area_weights(cube1) # calculate grid cell areas                                     
        totalmass_g=numpy.nansum(numpy.nansum(cube1.data*areas))
        totalmass_kt = totalmass_g/1E9
        text2  = "Total mass difference = {:.2f}".format(totalmass_kt)



        plt.title('NAME plumes Difference \n Inversion run: '+run_date_object+'\n Validity time  ' + date_object + ' UTC \n ' +text2+' kt \n'+ text1+' gm-2', fontsize=10) #adjusted slightly by ESJ to include the inversion run cut-off time in plot title


        output_filename=PlotDir+'Difference_Forecast_'+f+'_inversion_plumes_'+Tplus+'_'+timestamp+'.png'
        
        print(output_filename)

        plt.savefig(output_filename,dpi=150,bbox_inches='tight')
        plt.close()

        del cube1



if __name__ == '__main__':


    InDir = sys.argv[1]
    f = sys.argv[2]
    InDir2 = sys.argv[3]
    obs='obs2'

    # ------------------------------------------------------------   
    # Inversion plumes
    # ------------------------------------------------------------    
    
    file_list = find_files(InDir)
    file_list2 = find_files(InDir2)
    print(InDir)
    print(InDir2)
    for filename, filename2 in zip(file_list,file_list2):
        filename=filename[0]
        filename2=filename2[0]
        print(filename)
        print(filename2)

        # find time from filename
        filesuffix = filename.rpartition(".")[0]
        timestamp = filesuffix.split('_')[-1]
        Tplus = filesuffix.split('_')[-2]
        date_object_num = dt.datetime.strptime(timestamp, '%Y%m%d%H%M')
        date_object = str(date_object_num)  
        print(date_object)

        #Section added by ESJ to be able to include inversion cut-off time in plot title
        run_timestamp=f.split('_')[-2]
        run_date_object_num = dt.datetime.strptime(run_timestamp, '%Y%m%d%H%M')
        run_date_object = str(run_date_object_num)  
        print(run_date_object)
        

        #load data into cube
        cube = iris.load_cube(filename) 
        cube2 = iris.load_cube(filename2) #added by ESJ - creates iris cube for second resolution run

        #Rest of code (apart from bottom line) done by ESJ
        diff=cube.data-cube2.data
        #Finds dimensions of the cube
        xlen1=cube.data.shape[0] 
        ylen1=cube.data.shape[1] 

        a=0 #start number of intersection points as 0
        b=0 #start cube points over threshold equal to 0
        c=0 #start cube2 points over threshold equal to 0

        #add number of points above the threshold - is this a+b+c
        #change threshold to 2 and see what happens

        threshold=2 #or 0.5 if looking at 0.5 g m-2 threshold

        for i in range(xlen1):
            for j in range(ylen1):
                if cube.data[i,j]>=threshold and cube2.data[i,j]>=threshold: #if point higher than threshold for both models
                    a+=1
                else:
                    if cube.data[i,j]>=threshold and cube2.data[i,j]<threshold: #if point higher than threshold for model 1 only
                        b+=1
                    else:
                        if cube2.data[i,j]>=threshold and cube.data[i,j]<threshold: #if point higher than threshold for model 2 only
                            c+=1

        num_pts=a+b+c #finds total number of points where the spatial point is over the threshold for at least one model

        #Finds FMS value
        if (a+b+c)!=0:
            FMS=(a/(a+b+c))*100
        else:
            FMS=0

        print(num_pts)
        print(FMS)

        cube.data=diff #sets cube data to the difference so the difference plume is plotted
            
        #plot
        PlotInversionPlumes(cube, date_object, run_date_object, timestamp, f, Tplus, InDir)



 
