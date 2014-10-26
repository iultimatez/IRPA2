import re
import porter_algorithm
p = porter_algorithm.PorterStemmer()
stop_words_file = open('stop_words.txt', 'r')
stop_words = stop_words_file.read().split()
fullList = []
for x in range(1095):
	fileIndex = x + 1
	file_name = "IRTM/" + str(fileIndex) + ".txt"
	f = open (file_name, 'r')
	result = re.sub("[^A-Za-z]"," ",f.read().lower()).split()
	stop = filter(lambda x: not(x in stop_words), result) 
	stemmed = map(lambda x: p.stem(x, 0, len(x)-1), stop)

	addIndex = map(lambda x: {1: x, 2: fileIndex}, stemmed)


	fullList += addIndex

	f.close()

sortedList = sorted(fullList, key = lambda x : x[1])

dictionary = []
dictCount = -1

for x in range(len(sortedList)):
	#print sortedList[x][1] + ' ' + str(sortedList[x][2])
	if  x == 0:
		dictionary += [{1: sortedList[x][1], 2:1}]
		#print dictionary
		dictCount += 1
	else :
		if sortedList[x][1] == sortedList[x-1][1]:
			if sortedList[x][2] != sortedList[x-1][2]:
				dictionary[dictCount][2] += 1
		else :
			dictionary += [{1: sortedList[x][1], 2:1}]
			dictCount += 1
for x in dictionary:
	print x
#print dictionary
stop_words_file.close()

