# TO DO:
	# I need to figure out way to swap the ids in the file accroding to their euclidean distance


from scipy.spatial import distance

before = list()
after = list()

fileName = "tracks.txt"

# For now, I am only going to put two because I know it
frame = 1
reset = False

# Euclidean function
def myEuclidean(before, after, resetNum):
	idBef = 1
	idAft = 1
	finalIdArray = list()
	change = False
	resetButton = 0
	for pointBef in before:
		beforeList = list()
		for pointAft in after:
			beforeList.append(distance.euclidean(pointBef, pointAft))
		print beforeList
		finalIdArray.append(beforeList.index(min(beforeList)))
	print finalIdArray
	print "Here: ", resetNum

	newFile = open("polishedTracks.txt", "a")
	oldFile = open("tracks.txt", "r")
	for line in oldFile:
		if "RESET" in line:
			resetButton += 1
			if resetButton > 1:
				break
			#re write everythin over and over, try to fix this later
			line = myFile.next()
			change = True
		if change == True:
			intList = map(int, line.strip().split())
			# for now, I know its two, but it needs to be dynaimc
			if intList[1] == 0:
				intList[1] = finalIdArray[0]
				newFile.write("%d %d %d %d\r\n" % (intList[0], intList[1], intList[2], intList[3]))
			elif intList[1] == 1:
				intList[1] = finalIdArray[1]
				newFile.write("%d %d %d %d\r\n" % (intList[0], intList[1], intList[2], intList[3]))
		else:
			newFile.write(line)
	newFile.close()
	oldFile.close()

with open(fileName) as myFile:
	# lets skip the header
	myFile.next() 
	for num, line in enumerate(myFile, 2):
		if "RESET" in line:
			print "This is the number: ", num
			resetNum = num
			line = myFile.next()
			frame += 1
			reset = True
			
		ids = list()
		intList = map(int, line.strip().split())

		print intList[0]

		if frame != intList[0] and reset ==  True:
			print 4

			frame += 1
			# Perhaps here I run the euclidean distance in a function
			reset = False
			myEuclidean(before, after, resetNum)
			print resetNum
			break

		if frame == intList[0] and reset ==  False:
			print 1
			ids.append(intList[2])
			ids.append(intList[3])
			before.append(ids)
		elif frame != intList[0] and reset ==  False:
			print 2

			frame += 1
			before = list()
			ids.append(intList[2])
			ids.append(intList[3])
			before.append(ids)
		elif frame == intList[0] and reset ==  True:

			print 3

			ids.append(intList[2])
			ids.append(intList[3])
			after.append(ids)




		# break

print before
print after