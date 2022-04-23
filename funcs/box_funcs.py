import numpy as np

def load_21cmfast(path):
    try:
        with open(path, "rb") as f:
            numpy_data = np.fromfile(f,dtype=np.float32)
            print(numpy_data.shape)
    except IOError:
        print('Error While Opening the file!') 
    
    return numpy_data.reshape((200,200,200))

class FourierSpace:

    def __init__(self, box,L=300):

        #initializing some attributes
        self.box = box
        self.L = L
        
        #----------------------------- box specs ------------------------------#
        self.dims = len(box.shape) #dimensions of box
        self.N = field.shape[0] #number of pixels along one axis
        self.origin = self.N//2 #origin by fft conventions


        self.delta_k = 2*np.pi/self.L #kspace resolution of 1 pixel
        self.rmax = (self.n - self.origin)*self.delta_k #max radius
    
    
    def grid_dimless(self):
        '''
        Generates a fourier space dimensionless grid, finds 
        radial distance of each pixel from origin.
        '''

        indices = (np.indices(self.box.shape) - self.origin)
        self.radii = norm(indices, axis = 0) #dimensionless kspace radius of each pix
        