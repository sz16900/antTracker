# This needs to be dynamic, count how many ants, allocate the arrays, and loop the ants to show the
# histograms

import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
import scipy.stats as stats
import pylab as pl
import itertools




def ang(P1X,P1Y,P2X,P2Y,P3X,P3Y):
   numerator = P2Y*(P1X-P3X) + P1Y*(P3X-P2X) + P3Y*(P2X-P1X)
   denominator = (P2X-P1X)*(P1X-P3X) + (P2Y-P1Y)*(P1Y-P3Y)
   # print numerator
   # print denominator
   if denominator != 0:
     ratio = numerator/denominator
     angleRad = math.atan(ratio);
     angleDeg = (angleRad*180)/3.1416;
     return angleDeg
   # print angleDeg
   # if angleDeg<0:
   #     angleDeg = 180+angleDeg
   #     return angleDeg

# print leaderAnt
# print followerAnt
# print thirdAnt
# exit()

#########################Produce Angles#########################################
def buildArray(followerAnt, leaderAnt):
  arrayOfFifteensFollower = list()
  arrayOfFifteensLeader = list()
  arrayDict = {}
  # arrayOfFifteensThird = list()
  i = 0

  # I dont know why I choose two, but it seems to work fine
  # Does it make sense to do it on every single frame
  for i in range(0,len(followerAnt)):
      # print "Iteration", i # Python is an interesting language (no concat?)
      # print followerAnt[i]
      arrayOfFifteensFollower.append(followerAnt[i])
      arrayOfFifteensLeader.append(leaderAnt[i])
      # arrayOfFifteensThird.append(thirdAnt[i])

  arrayDict[0] = arrayOfFifteensFollower
  arrayDict[1] = arrayOfFifteensLeader
  return arrayDict


# Try to put these in a container so it could be iterated later 
# tracksContainer = list()
# tracksContainer.append(followerAnt)
# tracksContainer.append(leaderAnt)
# tracksContainer.append(thirdAnt)

def tandemrun(antInQuestion, pointingTo):
  
  arrayOfAngles = list()
  standardDev = 0

  for i in range(0, len(antInQuestion)-15):

      # Follower points to leader X
      x = ang(antInQuestion[i][0], antInQuestion[i][1],
      antInQuestion[i+15][0], antInQuestion[i+15][1],
      pointingTo[i+15][0], pointingTo[i+15][1])

      if x is None:
          xxxx = 0
      else:
          arrayOfAngles.append(x)

  # print "Mean of Follower: ", np.mean(arrayOfAngles)
  # print "Max of Follower: ", max(arrayOfAngles)
  # print "Mean - Max of Follower: ", np.mean(arrayOfAngles) - max(arrayOfAngles)
  print "Standard Deviation of Follower: ", np.std(arrayOfAngles)
  standardDev = np.std(arrayOfAngles)
  return standardDev


  # h = sorted(arrayOfAngles)
  # fit = stats.norm.pdf(h, np.mean(h), np.std(h))  #this is a fitting indeed
  # pl.plot(h,fit,'-o')
  # pl.hist(h,normed=True)      #use this to draw histogram of your data
  # pl.show()

#####################################Read File##################################
filename = "tracks21.txt"
f = open(filename, 'r')
f.next() # lets skip the header
my_list = list()
mycounter = 0
for line in f:
    mycounter = mycounter + 1
f.close


numAnts = 2
# This is to get the frames (3 ants)
mycounter = mycounter / numAnts

followerAnt = np.zeros(shape=(mycounter,2))
leaderAnt = np.zeros(shape=(mycounter,2))
# thirdAnt = np.zeros(shape=(counter,2))
counter = 0
i = 0
j = 0
k = 0
lead = 0
follow = 1

f = open(filename, 'r')
f.next() # lets skip the header

arrayOfSTD = list()
for line in f:

  if "RESET" in line:

    # I wrote this piece of code here to analyze the STD of every Tracklet
    # arrayDict = buildArray(followerAnt, leaderAnt)
    # myCoolArray = [tandemrun(arrayDict[0], arrayDict[1]), tandemrun(arrayDict[1], arrayDict[0])]
    # # tandemrun(arrayDict[0], arrayDict[1])
    # # tandemrun(arrayDict[1], arrayDict[0])
    # arrayOfSTD.append(myCoolArray)
    # counter = 0
    # del my_list[:]
    # followerAnt = np.zeros(shape=(mycounter,2))
    # leaderAnt = np.zeros(shape=(mycounter,2))
    lead = 0
    follow = 1

    # This piece of code here tries to switch everytome theres a ReSET to follow the EUCLIDEANs 

  else:
    counter = counter + 1
    intList = map(float, line.strip().split())
    my_list.append(intList[2])
    my_list.append(intList[3])
    if intList[1] == lead:
      leaderAnt[i] = my_list
      i = i + 1
    elif intList[1] == follow:
      followerAnt[j] = my_list
      j += 1
    # elif intList[1] == 2:
    #   thirdAnt[k] = my_list
    #   k += 1
    del my_list[:]

f.close() 

# print "STD's: ", arrayOfSTD
# d = 0
# # for value in arrayOfSTD:
# #   b = list()
# #   a = value
# #   print a
# #   exit()
# b = list(itertools.product(*arrayOfSTD))
# print b
# yy = len(b)
# print "Length: ", yy
# # print "Over Here: ", key, value
# # repeat by the number of RESTARTS????
# zz = list(itertools.product([0, 1], repeat=3))
# for c in range(0, len(b)):
#   print zz[c], sum(b[c])


arrayDict = buildArray(followerAnt, leaderAnt)
tandemrun(arrayDict[0], arrayDict[1])
# # tandemrun(arrayOfFifteensFollower, arrayOfFifteensThird)
tandemrun(arrayDict[1], arrayDict[0])

# tandemrun(arrayOfFifteensLeader, arrayOfFifteensThird)
# tandemrun(arrayOfFifteensThird, arrayOfFifteensFollower)
# tandemrun(arrayOfFifteensThird, arrayOfFifteensLeader)
