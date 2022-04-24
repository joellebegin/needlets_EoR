import numpy as np 
from numpy.fft import fftn, fftshift, ifftn
from scipy.special import eval_legendre
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from funcs.box_funcs import *

class NeedletFilters:
    '''Adapted from https://github.com/javicarron/mtneedlet'''

    def __init__(self, js, B, kmax):
        '''
        Init function. 

        Parameters:
        -----------
        j: int or array of ints
            Resolution parameter; effectively sets central location of bandpass
            filter. Can give an int (will give only one filter), or array (will
            give a bunch of filters).

        B : float
            The parameter B of the needlet which controls the width of the filters. 
            Should be larger that 1.

        kmax : int
            The maximum k mode for which the filters will be constructed.
        '''
        self.js =np.array(js,ndmin=1)
        self. B = B
        self.kmax = kmax

    def __f_need(self,t):
        '''Auxiliar function f to define the standard needlet'''
        if t <= -1.:
            return(0.)
        elif t >= 1.:
            return(0.)
        else:
            return(np.exp(1./(t**2.-1.)))
        
    def __psi(self,u):
        '''Auxiliar function psi to define the standard needlet'''
        return(integrate.quad(self.__f_need,-1,u)[0]/integrate.quad(self.__f_need,-1,1)[0])

    def __phi(self,q):
        '''Auxiliar function phi to define the standard needlet'''
        B=float(self.B)
        if q < 0.:
            raise ValueError('The multipole should be a non-negative value')
        elif q <= 1./B:
            return(1.)
        elif q >= 1.:
            return(0)
        else:
            return(self.__psi(1.-(2.*B/(B-1.)*(q-1./B))))
        
    def __b2_need(self,xi):
        '''Auxiliar function b^2 to define the standard needlet'''
        b2=self.__phi(xi/self.B)-self.__phi(xi)
        return(np.max([0.,b2])) 
        ## np.max in order to avoid negative roots due to precision errors

    def needlet_filters_1d(self,k_arr=None, j_val = None):
        '''
        k_arr: None or array
            if k_arr==None, will compute for all available k modes.
            Else, give array of ks you want to compute. 

        j_val: None or int
            If j_val==None, will compute for all js in self.js. Else,
            give an int and will compute for a certain j value
        '''
        
        if k_arr is not None:
            ks = k_arr
        else:
            ks=np.arange(self.kmax+1)

        
        needs=[]
        bl2=np.vectorize(self.__b2_need)

        if j_val is not None:
            xi=(ks/self.B**j_val)
            bl=np.sqrt(bl2(xi))
            needs.append(bl)
        
        else:
            for j in self.js:
                    xi=(ks/self.B**j)
                    bl=np.sqrt(bl2(xi))
                    needs.append(bl)

        return(np.squeeze(needs))

    def needlet_filters_2d(self,j,fourier_radii):
        filter_2d = []

        for slice in fourier_radii:
            filter_2d.append(self.needlet_filters_1d(k_arr=slice,j_val=j))

        return np.array(filter_2d)
    

    def filter_box(self, box, j):

        Fourier = FourierSpace(box)
        k_grid = Fourier.grid_dimless()
        filters = self.needlet_filters_2d(j, k_grid)

        fourier_filtered = fftshift(filters)*Fourier.box_fourier

        return ifftn(fourier_filtered)
    




