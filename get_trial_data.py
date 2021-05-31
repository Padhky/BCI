import pandas as pd
'''
These functions help store the features in the joblib file
You do not have to calculate all the features again

'''

def make_feature_vec(data, label):
    '''
    concatenate features and label in one data frame
    df = [features[N columns], label]
    '''
    df = pd.DataFrame(data)
    df['label'] = label
    return df


def update_feature_vec(df_old, df_new):
    '''
    update the feature vector data frame
    '''
    df = pd.concat([df_old, df_new])
    return df


def makeCSV(df, feature_vec_file):
    '''
    make CSV out of feature files
    '''
    df.to_csv(feature_vec_file, index=False)


def appendCSV(df, feature_vec_file):
    with open(feature_vec_file, 'a') as f:
        df.to_csv(f, header=False, index=False)


def readCSV(feature_vec_file):
    df = pd.read_csv(feature_vec_file)
    return df
    
    


    

