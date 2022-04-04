import numpy as np

dtype = np.dtype('B') #i think issue might be here -- this isn't the right dtype??
try:
    with open("delta_T_v3_z009.50_nf0.834376_useTs0_200_300Mpc", "rb") as f:
        numpy_data = np.fromfile(f,dtype)
        print(numpy_data.shape)
except IOError:
    print('Error While Opening the file!') 


test = numpy_data.reshape((200,200,200)) #fails here. I know for a fact that if it works properly, it should be (200,200,200)

import matplotlib.pyplot as plt

plt.imshow(test[0])
plt.show()
