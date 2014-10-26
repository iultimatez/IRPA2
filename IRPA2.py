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
dictionaryTXT = open('dictionary.txt', 'w')
print "{:<7} {:<20}{}".format("i_index", "term", "df")
dictionaryTXT.write("{:<7} {:<20}{}\n".format("i_index", "term", "df")) 
for x in range(len(dictionary)):
	print "{:<5}   {:<20}{}".format(str(x+1), dictionary[x][1], str(dictionary[x][2])) 
	dictionaryTXT.write("{:<5}   {:<20}{}\n".format(str(x+1), dictionary[x][1], str(dictionary[x][2])) )
#print len(dictionary)
dictionaryTXT.close()
stop_words_file.close()

