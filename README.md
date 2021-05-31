# Usage Guidelines
GUI is the main interface that combines all the parts. 
Please take a look at the manual on how GUI is implemented.

The GUI binds these packages:
1. Cortex API: please refer to pdf version of the Manual
2. TestPage
3. Model_with_hyperparameters


### TestPage

Important steps that makes life easier in managing huge chunks of data, extracted
features, and the preserving model from each session. 

    class TestPage(QWidget):

    def start_Training(self):
        """Create a session and record the raw EEG data"""

    def start_sequence_test(self):
        Updates the progress bar and trains from offline data
        
    def end_recording(self):
        """Once Finish button pressed in TestPage:
        1. Export EEG file and updated marker file
        2. Read those files and process feature extraction, Dimensionality Reduction and classification using model_with_hyperparameter.py

         """
    def create_EEG_file(self):
        """Export the EEG file to the user folder"""

    def live_prediction(self):
        """get prediction using trained model from online 
            data stream"""

    def start_Live(self, bool):
        Cube changes its position according to the prediction in live mode

    class manage_file:
        '''
        Creates file directory of each user in the current folder
        this is where EEG file, marker file, joblib are stored
    
        '''





###Model with hyperparameters
Class model is defined as follows

class Model():

    def __init__(self, name):
        ...
    def train(self, hyperpara):
        ...
    def extract_TestFeatures(self, Test_data):
        ...
    def run(self, Test_data):
        ...
    def extract_features(self, EEG_path, marker_path):
        ...
    def hyperparameter(self, EEG_path, marker_path):
        ...
Model is created for each user that logs in. extract_features
extracts EEG data specific to trial using marker files. DWT is
applied on these data and statistical features are computed.
This is used for extracting features from offline csv data that 
are collected from training. It returns a dataframe of 
features with labels in the last column.

'hyperparameter' tunes knn and svm with the given parameter space. Parameter 
space can be adjusted as required. This returns the best parameters for both
the classifiers.

'train' fits the classifier with the given hyperparameter. 

extract_TestFeatures: extracts features from online stream of data with the 
given window size. This function calls extract_Features.py. The extracted 
features are stored in self.df using get_trial_data.py. If the same user has
trained again the old df will be appended with the new one. 

run: using the trianed model, it predicts from features extracted from
extract_TestFeatures. 



