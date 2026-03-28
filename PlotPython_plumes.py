#####File from Met Office (via H. Webster) and adapted by Eva Siney Jones (ESJ)
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

    colours = [[255, 255, 255],   #0 white
  	       [255, 219, 233],   #1 pale pink
  	       [255, 179, 255],   #2 pink
  	       [204, 153, 255],   #3
  	       [179, 170, 253],	  #4 
  	       [153, 153, 255],   #5
  	       [128, 170, 255],   #6
  	       [ 77, 210, 255],   #7
  	       [  0, 255, 255],   #8 cyan
  	       [  0, 232, 204],   #9
  	       [128, 255, 128],   #10 light green
	       [154, 225,   0],   #11 yellowgreen
  	       [204, 255,  51],   #12
  	       [255, 255,   0],   #13 yellow
  	       [255, 204,  36],   #14 orange
  	       [255, 153,  51],   #15
  	       [255, 102,   0],   #16
  	       [255,   0,   0],   #17 red
 	       [179,   0,   0],   #18 	       
      	       [154,   0,   0],   #19 
      	       [128,    0,  0]]  #20 maroon	   
      	       
    colours = numpy.array(colours)/255.    
    cmap = colors.ListedColormap(colours)
    levels = [ 0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5,2.75, 
               3.0,  3.5, 4.0,  4.5, 5.0, 7.5, 10.0, 100.0, 1000.0] 
    pos_norm = BoundaryNorm(levels,21)
   
    return( cmap, levels, pos_norm)

def PlotInversionPlumes(cube1, date_object,run_date_object, timestamp, f, Tplus, PlotDir):

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
    
        cb = plt.colorbar(invplot, orientation='horizontal',shrink=0.9, ticks=	[0.5,1.0,1.5, 2.0,2.5,3.0,4.0,5.0,10.0,1000.0])	
    
        cb.set_label('Ash column loading [gm-2]', fontsize = 10)
	
        #plot location of volcano
        plt.scatter(159.44, 54.05, s=80, c='black',edgecolors='black', linewidths=0.5, marker='^', alpha=0.8,transform=ccrs.PlateCarree()) #alpha: 0 (transparent) and 1 (opaque).

        # find maximum ash value 
        text1  = "Maximum ash loading = {:.2f}".format(cube1.data.max())
        areas = iris.analysis.cartography.area_weights(cube1) # calculate grid cell areas                                     
        totalmass_g=numpy.nansum(numpy.nansum(cube1.data*areas))
        totalmass_kt = totalmass_g/1E9
        text2  = "Total mass = {:.2f}".format(totalmass_kt)

        plt.title('NAME plumes \n Inversion run: '+run_date_object+'\n Validity time  ' + date_object + ' UTC \n ' +text2+' kt \n'+ text1+' gm-2', fontsize=10) #title adjusted by ESJ to include the inversion run cut-off time in plot title

        output_filename=PlotDir+'Forecast_'+f+'_inversion_plumes_'+Tplus+'_'+timestamp+'.png'
        
        print(output_filename)

        plt.savefig(output_filename,dpi=150,bbox_inches='tight')
        plt.close()

        del cube1


if __name__ == '__main__':


    InDir = sys.argv[1]
    f = sys.argv[2]
    obs='obs2'

    # ------------------------------------------------------------   
    # Inversion plumes
    # ------------------------------------------------------------    
    
    file_list = find_files(InDir)
    print(InDir)
    for filename in file_list:
        filename=filename[0]
        print(filename)
            
        # find time from filename
        filesuffix = filename.rpartition(".")[0]
        timestamp = filesuffix.split('_')[-1]
        Tplus = filesuffix.split('_')[-2]
        date_object_num = dt.datetime.strptime(timestamp, '%Y%m%d%H%M')
        date_object = str(date_object_num)     
        print(date_object)

        #This section added by ESJ to be able to include inversion cut-off time in plot title
        run_timestamp=f.split('_')[-2] #note: use [-1] for 4km3hr runs 
        run_date_object_num = dt.datetime.strptime(run_timestamp, '%Y%m%d%H%M')
        run_date_object = str(run_date_object_num)  
        print(run_date_object)

        #load data into cube
        cube = iris.load_cube(filename) 
            
        #plot
        PlotInversionPlumes(cube, date_object, run_date_object, timestamp, f, Tplus, InDir)

 
