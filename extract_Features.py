"""Importing all the module"""

import pywt
import numpy as np
import pandas as pd
import glob
from scipy.stats import entropy
from scipy.stats import kurtosis
from scipy.stats import skew
import numpy.ma as ma
import itertools as it


"""Defining Global variables: """
electrodes = {"AF3": [], "F7": [], "F3": [], "FC5": [], "T7": [], "P7": [], "O1": [],
              "O2": [], "P8": [], "T8": [], "FC6": [], "F4": [], "F8": [], "AF4": [], }
band = ['gamma', 'beta', 'alpha', 'theta', 'delta']
level = ['l1', 'l2', 'l3']
elec = ["EEG." + i for i in electrodes.keys()]


def readCSV(eeg_path, marker_path):
    '''
    extract specific segments of EEG data corresponding to the trials
    '''
    eeg = pd.read_csv(eeg_path, skiprows= [0])
    eeg_marker = pd.read_csv(marker_path)
    data = eeg.copy()
    sep = data[elec]
    start = eeg_marker['Start']
    end = eeg_marker['End']
    
    class_label = []
    class_data = []
    for idx, label in enumerate(eeg_marker['Value']):
        class_label.append(label)
        start_idx = int(np.where(round(eeg['Timestamp'], 2) == round(start[idx], 2))[0][0])
        end_idx = int(np.where(round(eeg['Timestamp'], 2) == round(end[idx], 2))[0][0])
        class_data.append(sep.iloc[start_idx:end_idx, :])

    return class_label, class_data


def moving_window(x, time, step=1):
    """Windowing the raw EEG data"""
    fs = 128
    sample = fs*time
    streams = it.tee(x, sample)
    return zip(*[it.islice(stream, i, None, step*sample) for stream, i in zip(streams, it.count(step=step))])



def dwt(signal):
    """Four level decomposition of Discrete Wavelet Transform"""
    AC = signal
    dwt_coeff = {}
    for i in level:
        AC, DC = pywt.dwt(AC, "db4")
        if i in 'l1':
            AC1, DC1 = pywt.dwt(DC, "db4")
            dwt_coeff["Gamma"] = AC1
            AC2, DC2 = pywt.dwt(AC, "db4")
            dwt_coeff["Beta"] = DC2
            AC = AC2
        elif i in 'l2':
            AC3, DC3 = pywt.dwt(DC, "db4")
            dwt_coeff["SMR"] = DC3
            dwt_coeff["Alpha"] = AC3
            AC4, DC4 = pywt.dwt(AC, "db4")
            dwt_coeff["Theta"] = DC4
    return dwt_coeff


"""Shannon_Entropy feature:"""
def shan_entropy(signal):
    pA = abs(signal / (signal.sum()))
    Shannon = -np.sum(pA * np.log2(pA))
    return Shannon


"""Calculating five statistcal features:"""
def feature(channel, count=np.array([1, 1, 0, 1, 1])):
    dict_freq = ['Gamma', 'Beta', 'SMR', 'Alpha', 'Theta']
    feat_channel = []
    df = {}
    for i in dict_freq:
        masked = ma.masked_array([np.mean(channel[i]), np.std(channel[i]), shan_entropy(channel[i]),
                                  skew(channel[i]), kurtosis(channel[i])], mask=count)
        df[i] = masked.compressed()
    feature = pd.DataFrame(df)
    return feature


def feat_extraction(dataset, count=np.array([1, 1, 0, 1, 1]), time=5):
    time = time
    label, data = dataset
    count = count
    n = len(data)
    features = []
    clas_la = []
    for j in range(len(data)):
        signal = data[j]
        classlabel = label[j]
        frame_signal = list(moving_window(signal['EEG.AF3'], time=time))
        """Calculating the len of windowed signal and creating two empty list to append all the windowed signals"""
        len_sig = [[] for i in range(len(frame_signal))]
        temp = [[] for i in range(len(frame_signal))]

        """Windowing for each electrodes so that new signal contains 14 electrode windowed signal and added to a list"""
        for i in elec:
            window_sig = list(moving_window(signal[i], time=time))
            for s in range(len(len_sig)):
                len_sig[s].append(window_sig[s])

        """Calculating features for each windowed signal and added to new empty list"""
        for u in range(len(temp)):
            for t in len_sig[u]:
                DWT = dwt(t)
                temp[u].append(feature(DWT, count))

        """Appending all the calculated features of each windowed signal to the empty list"""
        for v in range(len(temp)):
            clas_la.append(classlabel)
            features.append(np.array(temp[v]).ravel())

    return (clas_la, np.array(features))


def prepare(lda_data):

    """Concatenate all the labels and raw EEG of multiple lists to one list """

    labels = []
    features = []

    for i in range(len(lda_data)):
        labels.append(lda_data[i][0])
        features.append(lda_data[i][1])

    flat_labels = [item for sublist in labels for item in sublist]
    flat_features = [item for sublist in features for item in sublist]

    print(f"features shape {np.shape(np.array(flat_features))}")

    return flat_features, flat_labels


def main(eeg_path, marker_path, count=np.array([1, 0, 0, 1, 0]), time=10):
    time = time
    count = count
    lda_features = []
    raw_data = readCSV(eeg_path, marker_path)
    feature_extraction = feat_extraction(raw_data, count, time)
    lda_features.append(feature_extraction)
    return prepare(lda_features)



def test_feature(live_data, count=np.array([1,1,0,1,1])):
    """Live mode feature extraction"""
    data = np.array(live_data)
    #print(data)
    transpose = np.transpose(data)
    np.shape(transpose)
    Test_features = []
    for i in transpose:
        DWT = dwt(i)
        Test_features.append(feature(DWT, count))

    #print(np.shape(Test_features))

    feat =np.array(Test_features).ravel()
    #print(f"feat shape : {np.shape(feat)}")

    return feat.reshape(1, -1)