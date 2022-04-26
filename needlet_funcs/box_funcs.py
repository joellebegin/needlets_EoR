import numpy as np
from numpy.fft import fftn
from scipy.linalg import norm
from astropy.cosmology import Planck15

def load_21cmfast(path):
    try:
        with open(path, "rb") as f:
            numpy_data = np.fromfile(f,dtype=np.float32)
    except IOError:
        print('Error While Opening the file!') 
    
    return numpy_data.reshape((200,200,200))

class Box:

    def __init__(self, box,z,L=300):

        #initializing some attributes
        self.box = box
        self.L = L
        self.z = z

        self.NU_21 = 1420 #MHz
        
        #----------------------------- box specs ------------------------------#
        self.dims = len(box.shape) #dimensions of box
        self.N = box.shape[0] #number of pixels along one axis
        self.origin = self.N//2 #origin by fft conventions


        self.delta_k = 2*np.pi/self.L #kspace resolution of 1 pixel
        self.rmax = (self.N - self.origin)*self.delta_k #max radius

        #------------------------- fourier transform --------------------------#
        
    
    #======================= fourier functions ====================#
    def fourier(self, ret = True):
        self.box_fourier = fftn(self.box)
        
        if ret:
            return self.box_fourier
    
    def grid_dimless(self):
        '''
        Generates a fourier space dimensionless grid, finds 
        radial distance of each pixel from origin.
        '''
 
        self.indices = (np.indices(self.box.shape) - self.origin)
        self.radii = norm(self.indices, axis = 0) #dimensionless kspace radius of each pix
        return self.radii


    #====================== cosmo functions =====================#
    def angle_subtended(self):
        DA = Planck15.angular_diameter_distance(self.z)
        return (self.L*180)/(DA*np.pi)

    def nu_obs(self):
        return self.NU_21/(1 + self.z)


        