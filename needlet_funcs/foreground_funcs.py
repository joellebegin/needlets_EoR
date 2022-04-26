
from pygsm import GlobalSkyModel2016
import healpy as hp
from healpy.newvisufunc import projview, newprojplot
import matplotlib.pyplot as plt
import numpy as np
from functools import partial 


def get_gsm_slice(freq, center, delta_ang, npix=200, sanity_check = False, plot_min = 0, plot_max = 100):
    '''
    gets chunck of gsm map at given freq, of given angular scale, of given dimensions

    Parameters:
    -----------

    freq: float
        frequency desired

    center: np array (len 2)
        [theta, phi] in colat,lat

    delta_ang: np array (len 2)
        [delta theta, delta phi] 

    '''
    
    print("generating map")
    gsm = GlobalSkyModel2016(freq_unit = 'MHz', unit = "TCMB")
    map = gsm.generate(freq)
    print("done generating map")

    len_map = len(map)
    nside = hp.npix2nside(len_map)
    center_lonlat = np.array([90,0]) - center # in lat,lon
    
    # bds = [[min theta, max theta],
    #        [min phi, max phi],]
    #
    # so essentially the colat/lon lines bounding the square

    bds = np.array([[center[0] - delta_ang[1]/2, center[0] + delta_ang[1]/2],
                        [center[1]-delta_ang[0]/2, center[1]+delta_ang[0]/2]])
                    

    # bds_lonlat = [[min lon, max lon],
    #               [min lat, max lat],]
    #
    bds_lonlat = np.array([[center_lonlat[1]-delta_ang[1]/2, center_lonlat[1]+delta_ang[1]/2],
                        [center_lonlat[0] - delta_ang[0]/2, center_lonlat[0] + delta_ang[0]/2]])


    proj = hp.projector.CartesianProj(lonra=bds_lonlat[0], latra=bds_lonlat[1], xsize=npix, ysize=npix)
    reproj = proj.projmap(map, vec2pix_func=partial(hp.vec2pix,nside))
    return reproj

    if sanity_check:
        #corners
        ang_bd_0 = np.array([bds[0][0], bds[1][0]]) #top right
        ang_bd_1 = np.array([bds[0][0], bds[1][1]]) #top left
        ang_bd_2 = np.array([bds[0][1], bds[1][0]]) #bottom right
        ang_bd_3 = np.array([bds[0][1], bds[1][1]]) #botoom left
        
        fig,ax=plt.subplots()
        projview(map, coord=["G"],cmap = plt.cm.jet, min=plot_min,max=plot_max,graticule=True, graticule_labels=True,projection_type="mollweide", hold = True)

        #theta,phi in colat,lon
        newprojplot(theta = np.radians(np.array([ang_bd_0[0],ang_bd_1[0]])), phi=np.radians(np.array([ang_bd_0[1],ang_bd_1[1]])), color = "k", linestyle = "-")
        newprojplot(theta = np.radians(np.array([ang_bd_0[0],ang_bd_2[0]])), phi=np.radians(np.array([ang_bd_0[1],ang_bd_2[1]])), color = "k", linestyle = "-")
        newprojplot(theta = np.radians(np.array([ang_bd_2[0],ang_bd_3[0]])), phi=np.radians(np.array([ang_bd_2[1],ang_bd_3[1]])), color = "k", linestyle = "-")
        newprojplot(theta = np.radians(np.array([ang_bd_1[0],ang_bd_3[0]])), phi=np.radians(np.array([ang_bd_1[1],ang_bd_3[1]])), color = "k", linestyle = "-", marker = "None")

        plt.savefig("sanity_check1.png", bbox_inches = "tight")
        
        
        fig,ax=plt.subplots()
        ax.imshow(reproj, origin="lower", cmap = plt.cm.jet, vmin = plot_min, vmax = plot_max)
        plt.savefig("sanity_check2.png", bbox_inches = "tight")
        
