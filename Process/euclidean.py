# TO DO:
	# I need to figure out way to swap the ids in the file accroding to their euclidean distance


from scipy.spatial import distance
import tempfile
import sys
import re

fileName = "tracks.txt"
dataToBeWritten = {}

# Euclidean function
def myEuclidean(afterFrame):

	# Negative 6 because we want to look at the last 5 frames
	pastInfo = dataToBeWritten[afterFrame - 6]
	predicted = {}
	velocity = {}
	for key, value in dataToBeWritten[afterFrame - 1].iteritems():
		velocity[key] =  ((value[0] - pastInfo[key][0]), (value[1] - pastInfo[key][1]))
		predicted[key] = ((value[0] + velocity[key][0]), (value[1] + velocity[key][1]))
	print velocity
	print predicted



	finalIdDict = {}
	bigDict = {}
	afterDist = {}

	for key, value in dataToBeWritten[afterFrame].iteritems():
		smallDict = list()
		total = 0
		# I think that there should be some check here, but for now it seems to be working as it is
		for keyAft, valueAft in predicted.iteritems():

			i = distance.euclidean(valueAft, value)
			# print i
			# total += i
			smallDict.append(i)
			afterDist[keyAft] = i

		# get the corresponding id
		finalIdDict[key] = smallDict.index(min(smallDict))
		# smallDict.append(total)
		bigDict[key] = smallDict
		# print smallDict

		print "The min:", min(afterDist, key=afterDist.get)

	print finalIdDict
	# This one checks if two or more points share the same id (obviously, this needs to be dynamic)
	
	print "big Dict: ", bigDict
	# exit()

	# Before I return, I should check if there are any equals. This is just for the two, so its not dynamic
	if finalIdDict[0] == finalIdDict[1]:
		print "here"
	# exit()

	return finalIdDict

# For now, I am only going to put two because I know it

def readRestart():
	frame = 1
	reset = False
	theCode = list()
	before = {}
	after = {}
	theIds = list()

	with open(fileName) as myFile:
		# lets skip the header
		myFile.next() 
		for line in myFile:

			if "RESET" in line:
				line = myFile.next()
				frame += 1
				reset = True


			ids = (0,0)
			intList = map(int, line.strip().split())

			if frame != intList[0] and reset ==  True:
				# print 4

				frame += 1
				# Perhaps here I run the euclidean distance in a function
				reset = False

				# Minus 1 because we want the frame just after the RESET 
				finalIdDict = myEuclidean(intList[0] - 1)
				print "FinalIdDict: ", finalIdDict
				# exit()
				# transcribe(finalIdDict)
				# break

			# This means we are in the frame and checking
			if frame == intList[0] and reset ==  False:
				# print 1
				theIds.append(intList[1])
				ids = (intList[2], intList[3])
				before[intList[1]] = ids
				dataToBeWritten[intList[0]] = before
			# This means we are not on the same frame, move on	
			elif frame != intList[0] and reset ==  False:
				# print 2
				frame += 1
				before = {}
				after = {}
				theIds = list()
				theIds.append(intList[1])
				ids = (intList[2], intList[3])
				before[intList[1]] = ids
				dataToBeWritten[intList[0]] = before

			elif frame == intList[0] and reset ==  True:
				# print 3
				ids = (intList[2], intList[3])
				after[intList[1]] = ids
				dataToBeWritten[intList[0]] = after

def transcribe(finalIdDict):
	oldFile = open(fileName, "r")

	t = tempfile.NamedTemporaryFile(mode="r+")
	oldFile = open("tracks.txt", "r")
	oldFile.next()
	change = False
	resetButton = 0
	for line in oldFile:
		if "RESET" in line:
			resetButton += 1
			if resetButton > 1:
				break
			#re write everythin over and over, try to fix this later
			line = oldFile.next()
			change = True
		if change == True:
			intList = map(int, line.strip().split())
			intList[1] = finalIdDict[intList[1]]
			t.write("%d %d %d %d\r\n" % (intList[0], intList[1], intList[2], intList[3]))
		else:
			t.write(line)

	oldFile.close()
	oldFile.close()

	t.seek(0) #Rewind temporary file to beginning

	o = open('tracks.txt', "r+")  #Reopen input file writable

	#Overwriting original file with temporary file contents
	
	for line in t:
		o.write(line)


	t.close() #Close temporary file, will cause it to be deleted 
	o.close()


readRestart()
# print theCode