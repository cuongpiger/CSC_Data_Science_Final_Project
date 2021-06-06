import pickle
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import label_binarize

def readData(pPath: str):
    datas = []
    filenames = ('X_train.pickle', 'X_test.pickle', 'y_train.pickle', 'y_test.pickle')
    
    for filename in filenames:
        with (open(f"{pPath}{filename}", "rb")) as data:
            while True:
                try:
                    datas.append(pickle.load(data))
                except EOFError:
                    break
                
    return datas


def saveGridsearchCV(pModelParams: dict, pPath: str):
    with open(pPath, 'w') as writer:
        json.dump(pModelParams, writer)
        
def saveModel(pModel, pPath: str):
    pickle.dump(pModel, open(pPath, 'wb'))
        

def jupyterCompleted(pSignalPath: str):
    os.system(f"vlc {pSignalPath}")