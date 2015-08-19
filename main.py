# -*- coding: utf-8 -*-

import numpy as np
import codecs

def loadDataSet():
	filedir = "dataset/0.txt"
	result = readFile(filedir)
	vector = [1,1,0,0,1,0,0,0,1,0,0,1,0,1,1,1,0,1,1,1,0,0,0,1,1,0,0,0,0,1,1,1,0,1,0,0,1,0,0,0,1,1,0,1,0,0,1,0,0,0,0,1,1,1]
	return result,vector

def createVocabList(dataset):
	vocabs = set( [ ] )
	for document in dataset:
		vocabs = vocabs|set( document )
	return list(vocabs)
	
def readFile(fl):
	f = codecs.open(fl, 'r', encoding='iso8859_9')
	splitted = []
	
	for line in f.readlines():
		#line = line.encode('utf8')
		splitted.append(splitData(line))
		
	return splitted
		 
def splitData(sentence):
	arr = sentence.split(" ")
	for index,word in enumerate(arr):
		arr[index] = word.encode('iso8859_9')
	return arr

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
	#dt,vec = loadDataSet();
	testingNB(['orospu','poker,','zaman'])
	
	