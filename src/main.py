#!/usr/bin/env python

"""Installation instructions
    python matlab engine
        https://nl.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html
        On Windows systems -
            cd "matlabroot\extern\engines\python"
            python setup.py install
        On Mac or Linux systems -
            cd "matlabroot/extern/engines/python"
            python setup.py install
    matplotlib
        python -m pip install matplotlib
    numpy
        python -m pip install numpy
"""

import os
import sys
import pickle
import random

import numpy as np
import matplotlib.pyplot as plt
import matlab.engine

"""The following functions are used to 
    load the data into python
"""

# Convert the matlab data files into a json format
def convert_mat_to_json(loc_mat, loc_json, mat):
    names = [json_file for name_mat in mat for _, json_file in mat[name_mat]]

    # check if json files exist
    if all(os.path.isfile(loc_json + json_file + ".json") for name_mat in mat for _, json_file in mat[name_mat]):
        print("JSON files already exist")
        return names, False

    # check if mat files exist
    if not all(os.path.isfile(loc_mat + mat_file) for mat_file in mat):
        print('ERROR: mat files do not exist: expected ' + str(mat.keys()))
        return [], False
    
    print("Starting matlab engine")
    eng = matlab.engine.start_matlab()
    for name_mat in mat:
        datasets = mat[name_mat]
        for name_data, name_json in datasets:
            # Check if the json file has been generated already
            if not os.path.isfile(loc_json + name_json + ".json"):
                print('Generating ' + name_json + '...')
                eng.convertToJSON(loc_mat, name_mat, name_data, loc_json, name_json, nargout=0)
    return names, True

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
    try:
        data = convert_to_float(data)
    except: 
        pass
    # Convert to numpy array for indexing convenience
    data = np.array([np.array(xi) for xi in data])
    # print(type(data)) # <class 'numpy.ndarray'>
    # print(data.shape) # same dimensions as in matlab
    # print(data.dtype) # float64
    return data

# Convert the json files into a faster python specific format
def jsonconverter(loc, name, names):
    data = {n : load_json(loc, n) for n in names}
    picklewriter(loc, name, data)

# Write the pickle file containing data
def picklewriter(loc, name, data):
    with open(loc + name + '.pickle', 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
    return data

# Read the pickle file containing all data
def picklereader(loc, name):
    with open(loc + name + '.pickle', 'rb') as f:
        data = pickle.load(f)
    return data

"""The following functions are used to 
    implement the information theoretical framework

    inputs are generally required to be 1D arrays containing sample points
    inputs are expected to be continuous in nature
"""

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
    if len(X) == 1:
        return entropy(bins, X[0])
    elif len(X) == 2:
        return mutualInformation(bins, X[0], X[1])
    else:
        return mutualInformationMulti(bins, *(X[:-1])) - mutualInformationConditionalMulti(bins, X[-1], *(X[:-1]))

"""The following functions are used to 
    manipulate the input data
    the data is assumed to be a 3D matrix (trials x time x channels)
"""

# Average all trials into a single value
# Output is a 2D matrix (time x channels)
def process_samples_mean(data):
    return data.mean(axis=0)

# Used to perform experiments across the different channels
# Input data is expected to be a 3D matrix (trials x time x channels)
# Can be used like
#   loop_channels(200, range(0,4), (lambda bins, *X : ...), inputdata)
# The lambda function has several inputs, the bins and all the data
# The data in the lambda function is a 2D matrix (trials x time)
def loop_channels(bins, channels, func, *X):
    return np.array([func(bins, *[d[:,:,c] for d in X]) for c in channels])

# Input data is expected to be a 2D matrix (trials x time)
def loop_time(bins, time, func, *X):
    return np.array([func(bins, *[d[:,t] for d in X]) for t in time])

def generate_timeseries_per_channel(bins, channels, time, func, *X):
    return loop_channels(bins, channels, (lambda bins, *X : 
        loop_time(bins, time, (lambda bins, *X: 
            func(bins, *X)
        ), *X)
    ), *X)

"""The following functions are used to 
    start the script
    load the data files
    and start the experiments
"""

def compare_common(loc, tmp, fig, data):
    # Compare the common time series between abstract, concrete and resting state
    # gen = lambda *X: generate_timeseries_per_channel(200, range(0, 4), range(0, 340), (lambda bins, *X: 
    #     mutualInformationMulti(bins, *[random.sample(set(x), 490) for x in X])), *X)
    gen = lambda *X: generate_timeseries_per_channel(200, range(0, 4), range(0, 340), (lambda bins, *X: 
        mutualInformationMulti(bins, *[x[0:490] for x in X])), *X)
    
    commonAbs = data['CommonAbstractness_TimeSeries']
    commonCon = data['CommonConcreteness_TimeSeries']
    common = data['Common_TimeSeries_rest']

    exp1 = perform_experiment(loc, tmp, 'CommonAbsCon', lambda: gen(commonAbs, commonCon))
    exp2 = perform_experiment(loc, tmp, 'CommonAbsRest', lambda: gen(commonAbs, common))
    exp3 = perform_experiment(loc, tmp, 'CommonConRest', lambda: gen(commonCon, common))

    rest = perform_experiment(loc, tmp, 'CommonRest', lambda: gen(common))
    absract = perform_experiment(loc, tmp, 'commonAbs', lambda: gen(commonAbs))
    concrete = perform_experiment(loc, tmp, 'commonCon', lambda: gen(commonCon))

    for i in range(0, 4):
        visualize_common(loc, fig, [exp1[i], exp2[i], exp3[i]], ['AbsCon', 'AbsRest', 'ConRest'], 'channel-' + str(i), 'Comparison of bivariate mutual information')
        visualize_common(loc, fig, [rest[i], absract[i], concrete[i]], ['Rest', 'Abs', 'Con'], 'entropy-' + str(i), 'Entropy')
        visualize_common(loc, fig, [exp1[i], exp2[i], exp3[i], rest[i], absract[i], concrete[i]], ['AbsCon', 'AbsRest', 'ConRest', 'Rest', 'Abs', 'Con'], 'all-channel-' + str(i), 'Comparison of bivariate mutual information')
        visualize_common(loc, fig, [100*exp1[i]/absract[i], 100*exp1[i]/concrete[i]], ['Abs', 'Con'], 'comp-' + str(i), 'Comparison', ylabel='percentage (%)')
    
def visualize_common(loc, fig, data, names, channel, title, xlabel='time', ylabel='information (bits)'):
    plt.figure(channel)
    for i in range(0, len(data)): 
        plt.plot(data[i], label=names[i])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.savefig(loc + fig + channel + ".png")
    plt.draw()

# The actual experiments
def experiments(loc, tmp, fig, data):
    compare_common(loc, tmp, fig, data)

# Perform an experiment and use caching
def perform_experiment(loc, tmp, name, func, ignore_tmp=False):
    if ignore_tmp or not os.path.isfile(tmp + name + '.pickle'):
        return picklewriter(loc+tmp, name, func())
    else:
        return picklereader(loc+tmp, name)

# Create a directory if it does not exist yet
def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

# The main execution function
def main():
    loc = '../../../../../Documents/data-ai-thesis/'
    loc_mat = '../../../../../Documents/data-ai-thesis/'
    mat = {'FinalTimeSeries_Data_withDescription.mat' : [('CommonAbstractness_TimeSeries', 'CommonAbstractness_TimeSeries'), 
                                    ('Abstractness_TimeSeries', 'Abstractness_TimeSeries'),
                                    ('Concreteness_TimeSeries', 'Concreteness_TimeSeries'),
                                    ('CommonConcreteness_TimeSeries', 'CommonConcreteness_TimeSeries'),
                                    ('CommonAbstractness_Description', 'CommonAbstractness_Description'), 
                                    ('Abstractness_Description', 'Abstractness_Description'),
                                    ('Concreteness_Description', 'Concreteness_Description'),
                                    ('CommonConcreteness_Description', 'CommonConcreteness_Description')
                                    ],
            'RSFinalTimeSeries_Alldata.mat' : [('Abstractness_TimeSeries', 'Abstractness_TimeSeries_rest'), 
                                    ('Common_TimeSeries', 'Common_TimeSeries_rest'),
                                    ('Concreteness_TimeSeries', 'Concreteness_TimeSeries_rest')
                                    ]
            }
    
    # Names used for intermediary files
    name = 'pydata'
    tmp = 'tmp/'
    fig = 'fig/'

    # Use matlab (if required) in order to convert all data into json format
    print('Start of the program')
    names, new = convert_mat_to_json(loc_mat, loc, mat)
    if len(names) == 0: return
    
    # Matlab is needed to convert the mat files into python
    # Convert the json files into pickle which loads much faster
    # Conversion is only done if the pickle file does not exist yet
    if new or not os.path.isfile(loc + name + '.pickle'):
        print('Converting json files into pickle format')
        jsonconverter(loc, name, names)

    # After using the previous line of code, we can simply read the pickle file to get our data
    print('Reading the pickle file: "' + name + '.pickle"')
    data = picklereader(loc, name)

    # Make sure the intermediary folders exist
    ensure_dir(loc + tmp)
    ensure_dir(loc + fig)

    # Now we can start the experiments with the data
    print('Starting the experiments')
    experiments(loc, tmp, fig, data)
    print('Ending the experiments')

    # Runs some tests
    print('Starting the tests')
    tests(data)
    print('Ending the tests')

    # And we are finished
    print('End of the program')

# Used for basic tests to check whether functions are implemented correctly
def tests(data):
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

    # commonAbs = process_samples(data['CommonAbstractness_TimeSeries'])
    # commonCon = process_samples(data['CommonConcreteness_TimeSeries'])
    # common = process_samples(data['Common_TimeSeries_rest'])

    # entropies = [0] * 4
    # for i in range(0,4):
    #     print("Region " + str(i))
    #     print(mutualInformationMulti(200, commonAbs[:,i], commonCon[:,i], common[:,i]))
    #     print(mutualInformationMulti(200, commonAbs[:,i], commonCon[:,i]))
    #     print(mutualInformationMulti(200, commonCon[:,i], common[:,i]))
    #     print(mutualInformationMulti(200, commonAbs[:,i], common[:,i]))

    # time = 220
    # print(mutualInformationMulti(2, np.transpose(commonAbs[time,0:4]), np.transpose(commonCon[time,0:4]), np.transpose(common[time,0:4])))
    # print(mutualInformationMulti(2, np.transpose(commonAbs[time,0:4]), np.transpose(commonCon[time,0:4])))
    # print(mutualInformationMulti(2, np.transpose(commonCon[time,0:4]), np.transpose(common[time,0:4])))
    # print(mutualInformationMulti(2, np.transpose(commonAbs[time,0:4]), np.transpose(common[time,0:4])))


# Entry point for our program
if __name__ == "__main__":
    main()
    
    