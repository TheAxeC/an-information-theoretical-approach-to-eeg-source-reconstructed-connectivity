import numpy as np
import sys

# convert a nested list with strings into a nested list of floats
def convert_to_float(lists):
  return [float(el) if not isinstance(el,list) else convert_to_float(el) for el in lists]

# load a json file containing the neural data
def load_json(loc, name):
    # load the json file (in matlab: converted mat into json)
    import json
    data = json.load(open(loc + name + '.json'))
    # all values in the data file are loaded as strings
    # thus first convert them back into floats
    data = convert_to_float(data)
    # Convert to numpy array for indexing convenience
    data = np.array([np.array(xi) for xi in data])
    # print(type(data)) # <class 'numpy.ndarray'>
    # print(data.shape) # same dimensions as in matlab
    # print(data.dtype) # float64
    return data

# Convert the json files into a faster python specific format
def jsonconverter(loc, name, names):
    import pickle
    data = {n : load_json(loc, n) for n in names}
    with open(loc + name + '.pickle', 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

# Read the pickle file containing all data
def picklereader(loc, name):
    import pickle
    with open(loc + name + '.pickle', 'rb') as f:
        data = pickle.load(f)
    return data

# Used in order to use the same bins for all data
def bin_edges(bins, data):
    return np.histogram(data, bins)[1]


# We want to use the same amount of bins for all timeseries
# The histogram function we use for binning will make each bin the same size
# Thus it could be possible that the start and end point of bins differs between different time series
# Therefor, this function is used
# All data points are flattened (to get a single array containing all points)
# This array is used to calculate the bin edges (which are then used in the actual experiments)
def calculate_bins(bins, data):
    vals = list(data.values())
    total = np.array([])
    for i in vals:
        total = np.concatenate((total, i.flatten()))
    return bin_edges(bins, total)

# def entropy(data):
    # from scipy.stats import entropy as entr
    # return entr(data)/np.log(2)
    # return np.sum(-data * np.log2(data+sys.float_info.epsilon))
def entropy(bins, *X):
    # Binning of the data
    data = np.histogramdd(X, bins=bins)
    # Calculate probabilities
    data = data[0].astype(float)/data[0].sum()
    # Compute H(X, Y, ..., Z) = sum(P(x, y, ..., z) * log2(P(x, y, ..., z)))
    return np.sum(-data * np.log2(data+sys.float_info.epsilon))
    
def conditionalEntropy(bins, X, Y):
    entro2 = entropy(bins, Y)
    entroJoint = entropy(bins, X, Y)
    return entroJoint - entro2

def mutualInformation(bins, X, Y):
    entro1 = entropy(bins, X)
    entro2 = entropy(bins, Y)
    entroJoint = entropy(bins, X, Y)
    return entro1 + entro2 - entroJoint

def conditionalEntropyMulti(bins, X, Y):
    assert False

def mutualInformationConditionalMulti(bins, Z, *X):
    H = 0
    for x in X:
        H += entropy(bins, x, Z)
    H -= entropy(bins, Z)
    H -= entropy(bins, Z, *X)
    return H

def mutualInformationMulti(bins, *X):
    if len(X) == 2:
        return mutualInformation(bins, X[0], X[1])
    else:
        return mutualInformationMulti(bins, *(X[:-1])) - mutualInformationConditionalMulti(bins, X[-1], *(X[:-1]))

def process_samples(data):
    return data.mean(axis=0)

# def get_timed_data(data):


def main():
    name = 'pydata'
    loc = '../../../../../Documents/data-ai-thesis/'
    names = ['CommonAbstractness_TimeSeries', 
            'Abstractness_TimeSeries', 
            'Concreteness_TimeSeries', 
            'CommonConcreteness_TimeSeries', 
            'Abstractness_TimeSeries_rest', 
            'Common_TimeSeries_rest', 
            'Concreteness_TimeSeries_rest']
    
    # Matlab is needed to convert the mat files into python
    # Use this once in order to convert the json files into pickle which loads much faster
    jsonconverter(loc, name, names)
    # After using the previous line of code, we can simply read the pickle file to get our data
    data = picklereader(loc, name)

    # the actual experiments
    bins = calculate_bins(200, data)
    commonAbs = process_samples(data['CommonAbstractness_TimeSeries'])
    commonCon = process_samples(data['CommonConcreteness_TimeSeries'])
    common = process_samples(data['Common_TimeSeries_rest'])

    entropies = [0] * 4
    for i in range(0,4):
        print("Region " + str(i))
        print(mutualInformationMulti(200, commonAbs[:,i], commonCon[:,i], common[:,i]))
        print(mutualInformationMulti(200, commonAbs[:,i], commonCon[:,i]))
        print(mutualInformationMulti(200, commonCon[:,i], common[:,i]))
        print(mutualInformationMulti(200, commonAbs[:,i], common[:,i]))
    
    # commonAbs
    # commonCon
    # common

    # time = 220
    # print(mutualInformationMulti(2, np.transpose(commonAbs[time,0:4]), np.transpose(commonCon[time,0:4]), np.transpose(common[time,0:4])))
    # print(mutualInformationMulti(2, np.transpose(commonAbs[time,0:4]), np.transpose(commonCon[time,0:4])))
    # print(mutualInformationMulti(2, np.transpose(commonCon[time,0:4]), np.transpose(common[time,0:4])))
    # print(mutualInformationMulti(2, np.transpose(commonAbs[time,0:4]), np.transpose(common[time,0:4])))



def tests():
    data = np.array([1, 1, 1, 1, 2, 2, 2, 2, 2, 2])
    data2 = np.array([1, 1, 1, 2, 2, 2, 2, 2, 2, 2])
    data3 = np.array([1, 1, 1, 1, 2, 2, 2, 2, 1, 2])
    # print(mutualInformation(2, data, data))
    # print(entropy(2, data))
    # print(conditionalEntropy(2, data, data2))
    # print(mutualInformationMulti(2, data, data2, data3))

    # data = np.array([1, 1, 1, 1, 1, 2, 2, 2, 2, 2])
    # data2 = np.array([1, 1, 1, 1, 1, 2, 2, 2, 2, 2])
    # print(mutualInformation(2, data, data2))

if __name__ == "__main__":
    main()
    tests()