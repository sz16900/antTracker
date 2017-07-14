# TO DO:
	# I need to figure out way to swap the ids in the file accroding to their euclidean distance


from scipy.spatial import distance

before = list()
after = list()

file = open("tracks.txt","r")

# lets skip the header
file.next() 

# For now, I am only going to put two because I know it
frame = 1
reset = False

# Euclidean function
def myEuclidean(before, after):
	idBef = 1
	idAft = 1
	for pointBef in before:
		beforeList = list()
		for pointAft in after:
			beforeList.append(distance.euclidean(pointBef, pointAft))
		print beforeList




for line in file:
	if "RESET" in line:
		line = file.next()
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
		myEuclidean(before, after)
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
file.close()