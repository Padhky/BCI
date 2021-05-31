
import extract_Features_temp as Feature
import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.pipeline import make_pipeline
from get_trial_data import make_feature_vec, update_feature_vec
import pandas as pd
import extract_Features_temp as Feature
import time
import os
from joblib import dump, load
CURR_DIR = os.getcwd()
print(CURR_DIR)

class Model():
    '''
    This is model without hyperparameter tuning.

    '''

    def __init__(self, name):
        self.name = name
        self.NO_Training = 0                   # keeps count of trainings
        #self.path = [path_EEG, path_marker]
        #self.Name = profile_name
        self.sc = StandardScaler()
        self.lda = LDA(n_components=3)
        self.Test_data = None
        self.window_size = 10 #default (in s)
        self.train_threshold = 3 #dummy number
        self.mask = np.array([0, 0, 1, 1, 1])  #dummy mask [mean, std, shannon, kurtosis, skewness]

    def train(self):

        if self.NO_Training == 0:
            print("Error - you must train first")

        else:
            train_data = self.df.iloc[:,:-1]
            train_label = self.df.iloc[:,-1]
            print(np.shape(train_data))
            print(train_label)

        self.clf = SVC(kernel='linear', C= 1)
        train_data = self.sc.fit_transform(train_data)
        print(train_data)
        #features = self.lda.fit_transform(train_data_norm, train_label)

        self.clf.fit(train_data, train_label)
        print(self.clf.score(train_data, train_label))
        #self.clf = clf

        print("Training Success")

    def extract_TestFeatures(self, Test_data):
        Testfeatures = Feature.test_feature(Test_data, self.mask)

        return Testfeatures

    def run(self, Test_data):
        """
        Feed me Test Data and I shall predict!

        """
        '''if self.NO_Training == 0:
            print("Error you must train first!")

        elif self.NO_Training < self.train_threshold:
            print("Insufficient training!")

        else:'''
        if True:
            #self.clf = make_pipeline(StandardScaler(), LDA(n_components=2), SVC(kernel='linear'))
            Test_features = self.extract_TestFeatures(Test_data)

            Test_features = self.sc.fit_transform(Test_features)
            prediction = self.clf.predict(Test_features)
            print(prediction)
            return prediction[0]

    def extract_features(self, EEG_path, marker_path):
        """
        extract features each trial sequence and append to features list

        """
        train_data, train_label = Feature.main(EEG_path, marker_path, self.mask, self.window_size)
        df_new = make_feature_vec(train_data, train_label)

        if self.NO_Training == 0:
            #assign feature list if it is the first run
            self.df = df_new
        else:
            #append to the feature list if it is a subsequent run
            self.df = update_feature_vec(self.df, df_new)

        self.NO_Training += 1

        print(self.df)
        print("Extract_feature flag")
        return train_data

# def main():
#     marker = 'T:\Proj_WS20\Data\Alex\Code_GUI_MARKERS_Alexander_13_09_36_2021-02-19.csv'
#     data =  'T:\Proj_WS20\Data\Alex\Code_GUI_EEG_Alexander_13_09_34_2021-02-19.csv'
#     name = "Vikas"
#
#     #Testing
#     #create a model for the user
#     model = Model(data, marker)
#     #extract features thrice. # need to update the path in argument in the subsequent runs
#     model.extract_features()
#     model.extract_features()
#     model.extract_features()
#     #train once finished
#     model.train()
#     #Testing use the same data
#     test = Model(data, marker)
#
#     print(test)
#     #run model on saved classifier
#     for i in range(3):
#         model.run(test_data[i].reshape(1,-1))
#         time.sleep(1)

if __name__ == '__main__':
    main()
