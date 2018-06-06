import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import shapefile

def add_maritimes_region(m):
    sf = shapefile.Reader("shapefiles/MaritimesRegionPolygon_UpdatedSept2015_wgs84")
    for shape in list(sf.iterShapes()):
        npoints=len(shape.points) # total points
        nparts = len(shape.parts) # total parts

        if nparts == 1:
           poly_lons = np.zeros((len(shape.points),1))
           poly_lats = np.zeros((len(shape.points),1))
           for ip in range(len(shape.points)):
               poly_lons[ip] = shape.points[ip][0]
               poly_lats[ip] = shape.points[ip][1]

           plot_polygon(poly_lons, poly_lats)

        else: # loop over parts of each shape, plot separately
            for ip in range(nparts): # loop over parts, plot separately
                i0=shape.parts[ip]
                if ip < nparts-1:
                    i1 = shape.parts[ip+1]-1
                else:
                    i1 = npoints

            seg=shape.points[i0:i1+1]
            poly_lons = np.zeros((len(seg),1))
            poly_lats = np.zeros((len(seg),1))
            for ip in range(len(seg)):
                poly_lons[ip] = seg[ip][0]
                poly_lats[ip] = seg[ip][1]

            plot_polygon(poly_lons, poly_lats,m, edgecolor='#ff0000',linewidth=1.0,alpha=0.6,zorder=40)
    return





def plot_polygon(poly_lons, poly_lats, m, edgecolor='#a6a6a6',linewidth=0.5,alpha=0.3,zorder=2):
    poly_x, poly_y = m(poly_lons, poly_lats)
    poly_xy = np.transpose(np.array((poly_x[:,0], poly_y[:,0])))
    
    # Ad polygon
    poly = Polygon(poly_xy,
                   closed=True,
                   edgecolor=edgecolor,
                   linewidth=linewidth,
                   alpha=alpha,
                   fill=False,
                   zorder=zorder)
    
    plt.gca().add_patch(poly)
    return






def add_NAFO_areas(m):
    sf = shapefile.Reader("shapefiles/NAFO_SubUnits_CanAtlantic")
    
    for shape in list(sf.iterShapes()):
        npoints=len(shape.points) # total points
        nparts = len(shape.parts) # total parts

        if nparts == 1:
           poly_lons = np.zeros((len(shape.points),1))
           poly_lats = np.zeros((len(shape.points),1))
           for ip in range(len(shape.points)):
               poly_lons[ip] = shape.points[ip][0]
               poly_lats[ip] = shape.points[ip][1]

           plot_polygon(poly_lons, poly_lats,m, edgecolor='#a6a6a6',linewidth=0.5,alpha=0.5,zorder=20)

        else: # loop over parts of each shape, plot separately
            for ip in range(nparts): # loop over parts, plot separately
                i0=shape.parts[ip]
                if ip < nparts-1:
                    i1 = shape.parts[ip+1]-1
                else:
                    i1 = npoints

            seg=shape.points[i0:i1+1]
            poly_lons = np.zeros((len(seg),1))
            poly_lats = np.zeros((len(seg),1))
            for ip in range(len(seg)):
                poly_lons[ip] = seg[ip][0]
                poly_lats[ip] = seg[ip][1]

            plot_polygon(poly_lons, poly_lats, m, edgecolor='#a6a6a6',linewidth=0.5,alpha=0.5,zorder=20)
    
   # NAFO labels
    nafo = pd.read_csv('NAFO_subunit_centroids.csv')

    zones = pd.unique(nafo['UnitArea'].values)


    for zone in zones:
        zone_points = nafo[nafo['UnitArea'] == zone]
        lat = zone_points['ddlat'].values[0]
        lon = zone_points['ddlong'].values[0]
        if lat > 39.9 and lat < 48.3 and lon > -69 and lon < -54.7:
            plot_label(lon, lat, zone, m)

    return
        
        
        



def plot_label(lon, lat, zone, m):
    x, y = m(lon, lat)
    plt.text(x, y, zone, fontsize=9,color='#a6a6a6',zorder=35)
    return



def plot_CriticalHabitats(m):
    nafo = pd.read_csv('NorthAtlanticRightWhale_CH_coords.csv')

    zones = pd.unique(nafo['Polygon_ID'].values)

    for zone in zones:
        zone_points = nafo[nafo['Polygon_ID'] == zone]

        poly_lats = zone_points['lat'].values

        poly_lons = zone_points['lon'].values

        poly_x, poly_y = m(poly_lons, poly_lats)
        poly_xy = np.transpose(np.array((poly_x, poly_y)))

        # Ad polygon
        poly = Polygon(poly_xy,
                       closed=True,
                       edgecolor='#00cc00',
                       facecolor='#00cc00',
                       linewidth=0.5,
                       alpha=0.2,
                       fill=True,
                       zorder=5)

        plt.gca().add_patch(poly)
    return






def distance(lat1,lon1,lat2,lon2):
    '''
    Estimates distance between 2 points on Earth.
    Assumes earth is a sphere (up to 0.5% error).
    Output is in meters
    '''
    import math

    R=6371000  # radius of Earth in meters
    phi_1=math.radians(lat1)
    phi_2=math.radians(lat2)
    
    delta_phi=math.radians(lat2-lat1)
    delta_lambda=math.radians(lon2-lon1)
    
    a=math.sin(delta_phi/2.0)**2+\
       math.cos(phi_1)*math.cos(phi_2)*\
       math.sin(delta_lambda/2.0)**2
    c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))
    
    return R*c # output distance in meters