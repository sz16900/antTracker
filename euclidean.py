# TO DO:
	# I need to figure out way to swap the ids in the file accroding to their euclidean distance


from scipy.spatial import distance
import tempfile
import sys
import re

fileName = "tracks.txt"

# Euclidean function
def myEuclidean(before, after):
	finalIdDict = {}

	for key, value in before.iteritems():
		afterDist = {}
		# I think that there should be some check here, but for now it seems to be working as it is
		for keyAft, valueAft in after.iteritems():
			afterDist[keyAft] = distance.euclidean(before[key], after[keyAft])
		# get the corresponding id
		after[min(afterDist, key=afterDist.get)] = key

	return after

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
				# print "BEFORE: ", before
				# print "After: ", after
				finalIdDict = myEuclidean(before, after)
				transcribe(finalIdDict)
				break

			# This means we are in the frame and checking
			elif frame == intList[0] and reset ==  False:
				# print 1
				theIds.append(intList[1])
				ids = (intList[2], intList[3])
				before[intList[1]] = ids
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

			elif frame == intList[0] and reset ==  True:
				# print 3
				ids = (intList[2], intList[3])
				after[intList[1]] = ids

def transcribe(finalIdDict):
	oldFile = open(fileName, "r")

	t = tempfile.NamedTemporaryFile(mode="r+")
	# oldFile = open("tracks.txt", "r")
	# oldFile.next()
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


			# # for now, I know its two, but it needs to be dynaimc
			# if finalIdArray[0][0] == 0 and finalIdArray[0][1] == 0:
			# 	if switch == 0:
			# 		intList[1] = theIds[0]
			# 		t.write("%d %d %d %d\r\n" % (intList[0], intList[1], intList[2], intList[3]))
			# 		switch += 1
			# 	elif switch == 1:
			# 		intList[1] = theIds[1]
			# 		t.write("%d %d %d %d\r\n" % (intList[0], intList[1], intList[2], intList[3]))
			# 		switch -= 1

			# # This is not very dynamic. This needs to change. 
			# else:
			# 	if switch == 0:
			# 		intList[1] = finalIdArray[0][0]
			# 		t.write("%d %d %d %d\r\n" % (intList[0], intList[1], intList[2], intList[3]))
			# 		switch += 1
			# 	elif switch == 1:
			# 		intList[1] = finalIdArray[0][1]
			# 		t.write("%d %d %d %d\r\n" % (intList[0], intList[1], intList[2], intList[3]))
			# 		switch -= 1
		else:
			t.write(line)

	# oldFile.close()
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