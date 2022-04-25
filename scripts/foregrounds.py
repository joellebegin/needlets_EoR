from pygsm import GlobalSkyModel2016
import healpy as hp
import matplotlib.pyplot as plt
import numpy as np
from functools import partial 

# gsm = GlobalSkyModel2016(freq_unit = 'MHz')
# map = gsm.generate(400)

len_map = len(map)
nside = hp.npix2nside(len_map)

# center = hp.ang2pix(nside,np.pi/2,np.pi/2)
delta_ang = np.array([14.,14.]) #degree
delta_ang_rad = delta_ang*(np.pi/180)
center = np.array([np.pi/3,np.pi/3])

bds = np.array([[center[0]-delta_ang_rad[0]/2, center[0]+delta_ang_rad[0]/2],
                [center[1] - delta_ang_rad[1]/2, center[1] + delta_ang_rad[1]/2]])

# THIS CODE IS DISGUSTING AND I'M ASHAMED

#corners
ang_bd_0 = np.array([bds[0][0], bds[1][0]]) #top right
ang_bd_1 = np.array([bds[0][0], bds[1][1]]) #top left
ang_bd_2 = np.array([bds[0][1], bds[1][0]]) #bottom right
ang_bd_3 = np.array([bds[0][1], bds[1][1]]) #botoom left


cut_width= hp.ang2pix(nside, ang_bd_1[0], ang_bd_1[1] ) - hp.ang2pix(nside, ang_bd_0[0], ang_bd_0[1] )

angs = hp.pix2ang(nside=nside, ipix = np.arange(len_map))

theta_mask1 = angs[0]>bds[0][0]
theta_mask2 = angs[0]<bds[0][1]
theta_mask = theta_mask1*theta_mask2
theta_inds = np.argwhere(theta_mask==1).flatten()

phi_mask1 = angs[1]>bds[1][0]
phi_mask2 = angs[1]<bds[1][1]
phi_mask = phi_mask1*phi_mask2
phi_inds= np.argwhere(phi_mask==1).flatten()

inds = np.intersect1d(theta_inds,phi_inds)

good_pix = hp.ang2pix(nside, angs[0][inds], angs[1][inds])
cut_map = map[good_pix]
cut_len = len(cut_map)

#this is so gross I hate it
# def find_best_divisor(size, low, high, step=1):
#     minimal_truncation, best_divisor = min((size % divisor, divisor)
#         for divisor in range(low, high, step))
#     return best_divisor

# pad = 100
# divisor = find_best_divisor(cut_len, cut_width - pad, cut_width+pad)
# cut_map = np.reshape(cut_map, (divisor, cut_len//divisor))

# plt.imshow(cut_map)
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='mollweide')

def mollweid_vec(lat_start,long_start,lat_end,long_end,color,width,headwidth=0.001,headlength=0.001):
    # proj = hp.projector.MollweideProj()
    proj = hp.projector.CartesianProj()
    plt.annotate('', xy=(proj.ang2xy(lat_end, long_end)), xytext=(proj.ang2xy(lat_start, long_start)),   arrowprops=dict(color=color,width=width,headwidth=headwidth,headlength=headlength))
 

# fig,ax=plt.subplots(nrows=1,ncols=2)

# fig = plt.figure()
# hp.visufunc.cartview(map, fig=fig, cmap = plt.cm.jet,min=0,max=100)

# w=0.1

# mollweid_vec(ang_bd_0[0],ang_bd_1[0],ang_bd_0[1],ang_bd_1[1],'black',0.1)
# mollweid_vec(ang_bd_2[0],ang_bd_0[0],ang_bd_2[1],ang_bd_0[1],'black',0.1)
# mollweid_vec(ang_bd_3[0],ang_bd_2[0],ang_bd_3[1],ang_bd_2[1],'black',0.1)
# mollweid_vec(ang_bd_1[0],ang_bd_3[0],ang_bd_1[1],ang_bd_3[1],'black',0.1)


# im = ax[1].imshow(new_map, cmap = plt.cm.jet)

# hp.projscatter(center, color = "k")

# hp.projscatter(ang_bd_0)
# hp.projscatter(ang_bd_1)
# hp.projscatter(ang_bd_2)
# hp.projscatter(ang_bd_3)
# hp.graticule()


 


# for i,j in enumerate(angs[0]):
#     if theta_mask[i] ==1 and phi_mask[i]==1:
#         hp.projscatter([angs[0][i],angs[1][i]], color = "k")

# plt.show()


#check out https://github.com/healpy/healpy/issues/568

lonra = [30,40]
latra = [-10,10]
npix=200

proj = hp.projector.CartesianProj(lonra=lonra, latra=latra, coord="G", xsize=npix, ysize=npix)
reproj = proj.projmap(map, vec2pix_func=partial(hp.vec2pix,nside))