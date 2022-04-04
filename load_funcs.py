import numpy as np

def load_21cmfast(path):
    try:
        with open(path, "rb") as f:
            numpy_data = np.fromfile(f,dtype=np.float32)
            print(numpy_data.shape)
    except IOError:
        print('Error While Opening the file!') 
    
    return numpy_data.reshape((200,200,200))