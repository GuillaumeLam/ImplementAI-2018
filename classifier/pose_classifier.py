from sklearn import datasets
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
import numpy as np
import math
import os
import pickle
import random
import re

def main():
	iris = datasets.load_iris()

	X = []
	Y = []

	X, Y = load_data(X, Y)
	#X = iris.data
	#Y = iris.target

	print("x[0]: " + str(X[10:]) + ", y[0]: " + str(Y[10:]))

	Z = list(zip(X,Y))
	random.shuffle(Z)

	X, Y = zip(*Z)

	print("x[0]: " + str(X[10:]) + ", y[0]: " + str(Y[10:]))

	# X =  np.array([[-1, -1], [-2, -1], [1, 1], [2, 1], [-3,7], [-8,4], [5,-6]])
	# Y = np.array([1, 1, 2, 2, 3, 3, 3])

	if not(len(X)==len(Y)):
		print("length of feature and class dont match!")
		exit() 

	size = len(X)

	X_train, X_test = X[:math.floor(size*0.7)], X[math.floor(size*0.7):]
	Y_train, Y_test = Y[:math.floor(size*0.7)], Y[math.floor(size*0.7):]

	clf = SVC(gamma='auto')

	clf.fit(X_train,Y_train)

	Y_pred = clf.predict(X_test)

	accuracy = accuracy_score(Y_test, Y_pred)
	error_rate = 1 - accuracy

	print("accuracy:" + str(accuracy) + " error rate:" + str(error_rate))

	with open(r"pose_classifier.p", "wb") as output_file:
		pickle.dump(clf, output_file)


def load_data(X, Y):
	files = os.listdir("./data")
	# filecount = count(files)
	for file in files:
		norm, _ = pickle.load(open("./data/" + str(file), 'rb'))
		X.append(norm.flatten())
		if re.match("squat*", file):
			Y.append(0)
		elif re.match("idle*", file):
			Y.append(1)

	return X, Y



if __name__ == "__main__":
	main()
