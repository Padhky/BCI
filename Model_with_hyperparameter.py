import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.model_selection import train_test_split
from sklearn.model_selection import LeaveOneOut
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.pipeline import make_pipeline
from get_trial_data import make_feature_vec, update_feature_vec

import extract_Features as Feature
import os

CURR_DIR = os.getcwd()
print(CURR_DIR)

class Model():
    '''
    We define a model class that takes care of:
    extracting features,
    computing statistical features
    reducing the dimenstions
    tuning the hyperparameters

    Helpful as we need a subject specific model
    '''


    def __init__(self, name):
        '''
        default values of the parameters
        '''

        self.name = name
        self.NO_Training = 0           # Parameter to disable from running live mode before training
        self.training = 0              # No. of trials - to display on GUI
        self.sc = StandardScaler()
        self.lda = LDA(n_components=3)
        self.Test_data = None
        self.window_size = 10
        self.train_threshold = 20      #No. of trainings to carry on before live mode is activated - currently disabled
        self.mask = np.array([0,0,0,0,0])  #helps you choose what statisticl features to extract
                                           # [mean, std, entropy, skewness, kurtosis]
                                           # to remove, replace 0 with 1, e.g. if only mean is needed: mask = [0,1,1,1,1]


    def train(self, hyperpara):
        """
        Hyperparameter tuning for both the classifiers

        """
        self.knn_hp, self.svm_hp = hyperpara

        if self.NO_Training == 0:
            print("Error - you must train first")

        else:
            train_data = self.df.iloc[:,:-1]
            train_label = self.df.iloc[:,-1]
            print(np.shape(train_data))
            print(train_label)

        self.clf = SVC(kernel=self.svm_hp[0], C= self.svm_hp[1], gamma = self.svm_hp[2])
        train_data = self.sc.fit_transform(train_data)
        train_data = self.lda.fit_transform(train_data)
        print(train_data)

        self.clf.fit(train_data, train_label)
        print(self.clf.score(train_data, train_label)) #fit on the same data just to ensure
        print("Training Success")

    def extract_TestFeatures(self, Test_data):
        Testfeatures = Feature.test_feature(Test_data, self.mask)
        return Testfeatures

    def run(self, Test_data):
        if self.NO_Training == 0:
            print("Error you must train first!")
            """elif self.NO_Training < self.train_threshold:
            print("Insufficient training!")"""

        else:
            #self.clf = make_pipeline(StandardScaler(), LDA(n_components=2), SVC(kernel='linear'))
            Test_features_raw = self.extract_TestFeatures(Test_data)

            Test_features = self.sc.transform(Test_features_raw)
            Test_features = self.lda.transform(Test_features)
            prediction = self.clf.predict(Test_features)
            #print(prediction)
            return prediction

    def extract_features(self, EEG_path, marker_path):
        '''
        compute dwt features, extract statistical features from EEG data
        and stores it in self.df = [features, label]

        '''
        train_data, train_label = Feature.main(EEG_path, marker_path, self.mask, self.window_size)
        df_new = make_feature_vec(train_data, train_label)

        if self.NO_Training == 0:
            self.df = df_new
        else:
            self.df = update_feature_vec(self.df, df_new)

        self.NO_Training += 1

        print("Extract_feature flag")
        return train_data

    
    
    def hyperparameter(self, EEG_path, marker_path):
        '''
        returns the hyperparameters of svm and knn

        '''

        #features, labels = Feature.main(EEG_path, marker_path, self.mask, self.window_size)
        features, labels = self.df.iloc[:,:-1], self.df['label']
        #print(features)
        #print(labels)
        X_train, Y_train = features, labels
        """Hyperparameter for KNN:"""
        n_neig = [1,3,5,7,9 ]
        p = [1, 2]
        hyperparameter_knn = dict(kneighborsclassifier__n_neighbors=n_neig, kneighborsclassifier__p=p)

        """Pipeline"""
        clf_knn = make_pipeline(StandardScaler(), LDA(n_components = 3), KNN())
        cv = LeaveOneOut()
        knn_parameter = GridSearchCV(clf_knn, hyperparameter_knn, cv=cv)

        best_knn_model = knn_parameter.fit(X_train, Y_train)
        self.best_p = best_knn_model.best_estimator_.get_params()['kneighborsclassifier__p']
        self.best_nn = best_knn_model.best_estimator_.get_params()['kneighborsclassifier__n_neighbors']
        print("Best p:", self.best_p)
        print("Best Nearest neighbors:", self.best_nn )

        hp_knn = (self.best_p, self.best_nn)

        """Hyperparameter for SVM"""
        svc = SVC()
        clf_svc = make_pipeline(StandardScaler(), LDA(n_components = 3), SVC())
        parameter = {
        '''Change parameter space here'''
        
            "svc__kernel": ['linear', 'rbf'],
            "svc__C": [0.001,0.01,0.1,1,10,100],
            "svc__gamma":[0.001,0.01,0.1,1,10,100],
        }
        svc_parameter = GridSearchCV(clf_svc, parameter, cv=cv, return_train_score = True)
        best_svc_model = svc_parameter.fit(X_train,Y_train)
        self.best_C =  best_svc_model.best_estimator_.get_params()['svc__C']
        self.best_kernel = best_svc_model.best_estimator_.get_params()['svc__kernel']
        self.best_gamma = best_svc_model.best_estimator_.get_params()['svc__gamma']
        print("Best_kernel:", self.best_kernel)
        print("Best_C:", self.best_C )
        print("Best_gamma:", self.best_gamma)
        hp_svm = (self.best_kernel, self.best_C, self.best_gamma)

        return (hp_knn, hp_svm)
