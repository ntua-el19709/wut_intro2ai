import numpy as np
import random
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn import tree
import time
# from sklearn.metrics import confusion_matrix
from sklearn import preprocessing
import matplotlib.pyplot as plt


def encode_feature(array):
    """ Encode a categorical array into a number array
    :param array: array to be encoded
    :return: numerical array
    """
    encoder = preprocessing.LabelEncoder()
    encoder.fit(array)
    tolist = encoder.transform(array)

    return tolist.tolist()


method = int(input("Enter method : 1 for SVM and 2 for Decision Tree:\n"))

#read the file and put the packets in list
with open('kddcup.data.corrected', 'rb') as f:
    inputs = f.readlines()

class_names = ['DDoS packet','normal']

packets = []

for item in inputs:
    packets.append(str(item)[2:(len(item)+1)])

hX = []
hy = []
hXc1 = []
hXc2 = []
hXc3 = []


#sample the input, because its very big for training
for packet in packets:
    strlistpac = packet.split(",")
    take = np.random.binomial(1, 0.01)
    if take == 0:
        continue
    if "normal" in packet:
        hy.append(0)
    else:
        hy.append(1)
    hX.append([float(x)for x in strlistpac[4:41]])
    if method == 2:
        hXc1.append(strlistpac[1])
        hXc2.append(strlistpac[2])
        hXc3.append(strlistpac[3])


hX = list(map(list, zip(*hX)))
if method == 2:
    hX.append(encode_feature(hXc1))
    hX.append(encode_feature(hXc2))
    hX.append(encode_feature(hXc3))

# hyperparameter optimization

bestparam = []
bestcla = 0

start = time.time()
#try randomly a lot of times different combinations of parameters
#and remember the best one
for i in range(100):
    param = random.sample(range(0, 37), 10)
    htX = []
    for z in param:
        htX.append(hX[z])
    htX = list(map(list, zip(*htX)))
    xtrain, xtest, ytrain, ytest = train_test_split(htX, hy, test_size=0.3, random_state=32)
    if method == 1:
        model = SVC()
    elif method == 2:
        model = tree.DecisionTreeClassifier()
    model.fit(xtrain, ytrain)
    cla = model.score(xtest, ytest)
    if bestcla < cla:
        bestcla = cla
        bestparam = param.copy()

#train the model according to the best parameters
htX = []
for z in bestparam:
    htX.append(hX[z])
htX = list(map(list, zip(*htX)))
if method == 1:
    model = SVC()
elif method == 2:
    model = tree.DecisionTreeClassifier()
model.fit(htX, hy)

#open corrected file to test it
with open('corrected', 'rb') as f:
    inputs = f.readlines()

packets = []
for item in inputs:
    packets.append(str(item)[2:(len(item)+1)])

X = []
Xc1 = []
Xc2 = []
Xc3 = []
y = []
for packet in packets:
    strlistpac = packet.split(",")

    if "normal" in packet:
        y.append(0)
    else:
        y.append(1)
    X.append([float(x)for x in strlistpac[4:41]])
    if method == 2:
        Xc1.append(strlistpac[1])
        Xc2.append(strlistpac[2])
        Xc3.append(strlistpac[3])

X = list(map(list, zip(*X)))
if method == 2:
    X.append(encode_feature(Xc1))
    X.append(encode_feature(Xc2))
    X.append(encode_feature(Xc3))

htX = []
for z in bestparam:
    htX.append(X[z])
X = list(map(list, zip(*htX)))

print("The packets are correctly classified with probability:\n", model.score(X,y))
end = time.time()
print("Computational time : \n", end-start)

if method == 2:
    decision_tree = tree.DecisionTreeClassifier(random_state=456)
    decision_tree = decision_tree.fit(xtrain, ytrain)
    # Visualizing the decision tree

    # 1. Saving the image of the decision as a png
    plt.subplots(figsize=(17, 12))
    tree.plot_tree(decision_tree, filled=True, rounded=True,class_names=class_names)
    plt.savefig("decision_tree.png")

    train_error = np.round(decision_tree.score(xtrain, ytrain), 2)
    test_error = np.round(decision_tree.score(xtest, ytest), 2)

    print("Training Set Mean Accuracy = " + str(train_error))
    print("Test Set Mean Accuracy = " + str(test_error))

