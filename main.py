# -*- coding: utf-8 -*-
import numpy as np

def loadDataSet():
	postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
							['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
							['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
							['stop', 'posting', 'stupid', 'worthless', 'garbage','fuck'],
							['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
							['quit', 'buying', 'worthless', 'dog', 'food', 'stupid','fuck']]
	classVec = [0,1,0,1,0,1]
	return postingList, classVec

def createVocabList(dataset):
	vocabs = set( [ ] )
	for document in dataset:
		vocabs = vocabs|set( document )
	return list(vocabs)
	
def bagOfWords2Vec(vocabs, inputSet):
	returnVec = [0] * len(vocabs)
	
	for inp in inputSet:
		if inp not in vocabs:
			print "not fount %s", inp
		else:
			returnVec[vocabs.index(inp)] += 1
	
	return  returnVec
		
def trainNB0(trainMatrix, trainCategory):
	numTrainDocs = len(trainMatrix)
	numWords = len(trainMatrix[0])
	pAbusive = sum(trainCategory) / float( numTrainDocs )
	p0Num = np.ones( numWords )
	p1Num = np.ones( numWords )
	p0Denom = 2.0
	p1Denom = 2.0
	
	for i in range( numTrainDocs ):
		if trainCategory[i] == 1:
			p1Num += trainMatrix[i]
			p1Denom += sum( trainMatrix[i] )
		else:
			p0Num += trainMatrix[i]
			p0Denom += sum( trainMatrix[i] )
	
	p1Vect = np.log(p1Num / p1Denom)
	p0Vect = np.log(p0Num / p0Denom)
	return p0Vect,p1Vect,pAbusive
	
def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
	p1 = sum(vec2Classify * p1Vec) + np.log(pClass1)
	p0 = sum(vec2Classify * p0Vec) + np.log(1.0 - pClass1)

	if p1 > p0:
		return 1
	else:
		return 0
		
def testingNB(splitted):
	vlist,vec = loadDataSet()
	voc = createVocabList(vlist)
	trainMat = [ ]
	for post in vlist:
		trainMat.append(bagOfWords2Vec(voc, post))
	
	p0V,p1V,pAb = trainNB0(trainMat,vec)
	
	doc = bagOfWords2Vec(voc,splitted)
	print splitted,"classified as",classifyNB(doc,p0V,p1V,pAb)
	

if __name__ == '__main__':
	testingNB(['love','ate','fuck'])
	
	