import numpy as np 
from scipy.special import eval_legendre
import matplotlib.pyplot as plt
import scipy.integrate as integrate


class NeedletFilters:
    '''Adapted from https://github.com/javicarron/mtneedlet'''

    def __init__(self, j, B, kmax):
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
        self.j = j
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

    def needlet_filters(self):
        
        ks=np.arange(self.kmax+1)
        j=np.array(self.j,ndmin=1)
        needs=[]
        bl2=np.vectorize(self.__b2_need)

        for jj in j:
            xi=(ks/self.B**jj)
            bl=np.sqrt(bl2(xi))
            needs.append(bl)
            
        return(np.squeeze(needs))


js = [0,1,2,3]
Need = NeedletFilters(js, 2, 10)
filters = Need.needlet_filters()


fig, ax = plt.subplots()
for j in js:
    ax.plot(filters[j], label = str(j))
    
plt.show()