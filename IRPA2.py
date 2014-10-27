import re
import porter_algorithm
import math
import sys

p = porter_algorithm.PorterStemmer()
stop_words_file = open('stop_words.txt', 'r')
stop_words = stop_words_file.read().split()

fullList = []
arrayForEachDocument = []
arrayForEachDocumentWithCount = []

numberOfDocs = int(sys.argv[1])

for x in range(numberOfDocs):
	fileIndex = x + 1
	file_name = "IRTM/" + str(fileIndex) + ".txt"
	f = open (file_name, 'r')
	result = re.sub("[^A-Za-z]"," ",f.read().lower()).split()
	stop = filter(lambda x: not(x in stop_words), result)
	stemmed = map(lambda x: p.stem(x, 0, len(x)-1), stop)
	addIndex = map(lambda x: {1: x, 2: fileIndex}, stemmed)
	fullList += addIndex
	addIndex.sort( key = lambda x : x[1])
	sortedaddIndex = []
	addIndexSortCount = -1
	for z in range(len(addIndex)):
		if  z == 0:
			sortedaddIndex += [{1: addIndex[z][1], 2:1}]
			addIndexSortCount += 1
		else :
			if addIndex[z][1] == addIndex[z-1][1]:
				sortedaddIndex[addIndexSortCount][2] += 1
			else :
				sortedaddIndex += [{1: addIndex[z][1], 2:1}]
				addIndexSortCount += 1
	#print sortedaddIndex
	arrayForEachDocumentWithCount.append(sortedaddIndex)
	arrayForEachDocument.append(sorted(stemmed))
	#for q in sortedaddIndex:
		#print q[1] + '  ' + str(q[2])
	f.close()
#print arrayForEachDocument
#print len(arrayForEachDocument)

sortedList = sorted(fullList, key = lambda x : x[1])

dictionary = []
dictCount = -1

for x in range(len(sortedList)):
	if  x == 0:
		dictionary += [{1: sortedList[x][1], 2:1, 3:dictCount+2}]
		#print dictionary
		dictCount += 1
	else :
		if sortedList[x][1] == sortedList[x-1][1]:
			if sortedList[x][2] != sortedList[x-1][2]:
				dictionary[dictCount][2] += 1
		else :
			dictionary += [{1: sortedList[x][1], 2:1, 3:dictCount+2}]
			dictCount += 1

dictionaryTXT = open('dictionary.txt', 'w')
#print "{:<7} {:<20}{}".format("i_index", "term", "df")
dictionaryTXT.write("{:<7} {:<20}{}\n".format("i_index", "term", "df")) 
for x in range(len(dictionary)):
	#print "{:<5}   {:<20}{}".format(str(x+1), dictionary[x][1], str(dictionary[x][2])) 
	dictionaryTXT.write("{:<5}   {:<20}{}\n".format(str(x+1), dictionary[x][1], str(dictionary[x][2])))

allVectors = []
#print len(dictionary)
for y in range(len(arrayForEachDocument)):
	getTermIndex = filter(lambda x: (x[1] in arrayForEachDocument[y]), dictionary)
	# fileIndex = y + 1
	# file_name = "results/" + str(fileIndex) + ".txt"
	# writeResult = open (file_name, 'w')
	# print file_name + ' ' + str(len(arrayForEachDocumentWithCount[y]))
	# writeResult.write(str(len(arrayForEachDocumentWithCount[y])) + '\n')
	# print "t_index tf_idf"
	# writeResult.write("t_index tf_idf\n")
	vector = []
	for q in range(len(arrayForEachDocumentWithCount[y])):
		#print "{:<5}   {:.2f}".format(str(getTermIndex[q][3]), math.log(float(numberOfDocs) / float(getTermIndex[q][2]), 10) * arrayForEachDocumentWithCount[y][q][2])
		#writeResult.write("{:<5}   {:.2f}\n".format(str(getTermIndex[q][3]), math.log(float(numberOfDocs) / float(getTermIndex[q][2]), 10) * arrayForEachDocumentWithCount[y][q][2]))
		vector.append({1: getTermIndex[q][3], 2: (math.log(float(numberOfDocs) / float(getTermIndex[q][2]), 10) * arrayForEachDocumentWithCount[y][q][2])})
	#writeResult.close()
	allVectors.append(vector)

distanceForEveryDocument = []

for x in range(len(allVectors)):
	distance = 0.0
	for y in range(len(allVectors[x])):
		distance += allVectors[x][y][2]*allVectors[x][y][2]
	distance = math.sqrt(distance)
	distanceForEveryDocument.append(distance)
#print distanceForEveryDocument

for x in range(len(allVectors)):
	fileIndex = x + 1
	file_name = "results/" + str(fileIndex) + ".txt"
	writeResult = open (file_name, 'w')
	#print file_name + ' ' + str(len(allVectors[x]))
	writeResult.write(str(len(allVectors[x])) + '\n')
	#print "t_index tf_idf"
	writeResult.write("t_index tf_idf\n")
	for y in range(len(allVectors[x])):
		allVectors[x][y][2] = allVectors[x][y][2]/distanceForEveryDocument[x]
		#print "{:<5}   {:.2f}".format(str(allVectors[x][y][1]), allVectors[x][y][2])
		writeResult.write("{:<5}   {:.2f}\n".format(str(allVectors[x][y][1]), allVectors[x][y][2]))
	writeResult.close()

def cos_similarity(x, y):
	common = []
	pointerX = 0
	pointerY = 0;
	while pointerX < len(allVectors[x]) and pointerY < len(allVectors[y]):
		if allVectors[x][pointerX][1] == allVectors[y][pointerY][1]:
			common.append({1: allVectors[x][pointerX][1], 2:allVectors[x][pointerX][2], 3:allVectors[y][pointerY][1], 4:allVectors[y][pointerY][2], 5: allVectors[x][pointerX][2] * allVectors[y][pointerY][2] })
			pointerY += 1
			pointerX += 1
		elif allVectors[x][pointerX][1] < allVectors[y][pointerY][1]:
			pointerX += 1
		elif allVectors[x][pointerX][1] > allVectors[y][pointerY][1]:
			pointerY += 1
	#print common
	# distanceX = 0.0
	# distanceY = 0.0
	# for a in allVectors[x]:
	# 	distanceX += a[2]*a[2]
	# distanceX = math.sqrt(distanceX)
	# for b in allVectors[y]:
	# 	distanceY += b[2]*b[2]
	# distanceY = math.sqrt(distanceY)
	inner = 0.0
	for c in common:
		inner += c[5]
	#return inner/(distanceY*distanceX)
	return inner

#str(getTermIndex[q][3]) + ' ' + arrayForEachDocumentWithCount[y][q][1] + "  " + str(math.log(float(numberOfDocs) / float(getTermIndex[q][2]), 10) * arrayForEachDocumentWithCount[y][q][2])
dictionaryTXT.close()
stop_words_file.close()

print "cosine similarity of " + sys.argv[2] + ' and ' + sys.argv[3]
print cos_similarity(int(sys.argv[2]),int(sys.argv[3]))

