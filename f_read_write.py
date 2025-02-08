import pickle

def write(path, data):
    file = open(path, 'wb')
    pickle.dump(data, file)
    file.close()

def read(path):
    with open(path, 'rb') as file:
        data = pickle.load(file)
    return data

#USE
#write("test", [1,2,3,4,5])
#read("color_calibration")