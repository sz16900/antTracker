import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
import scipy.stats as stats
import pylab as pl

#####################################Read File##################################
filename = "tracks.txt"
f = open(filename, 'r')
f.next() # lets skip the header
my_list = list()
counter = 0
for line in f:
    counter = counter + 1
f.close

# This is to get the frames
counter = counter / 2

followerAnt = np.zeros(shape=(counter,2))
leaderAnt = np.zeros(shape=(counter,2))
counter = 0
i = 0
j = 0

f = open(filename, 'r')
f.next() # lets skip the header
for line in f:

  if "RESET" in line:
    break

  counter = counter + 1
  intList = map(float, line.strip().split())
  my_list.append(intList[2])
  my_list.append(intList[3])
  if intList[1] == 0:
    leaderAnt[i] = my_list
    i = i + 1
  elif intList[1] == 1:
    followerAnt[j] = my_list
    j += 1
  del my_list[:]

f.close()

#########################Get Single Angle From Lines###########################

# def dot(vA, vB):
#     return vA[0]*vB[0]+vA[1]*vB[1]
# def ang(lineA, lineB):
#     # Get nicer vector form
#     vA = [(lineA[0][0]-lineA[1][0]), (lineA[0][1]-lineA[1][1])]
#     vB = [(lineB[0][0]-lineB[1][0]), (lineB[0][1]-lineB[1][1])]
#     # Get dot prod
#     dot_prod = dot(vA, vB)
#     # Get magnitudes
#     magA = dot(vA, vA)**0.5
#     magB = dot(vB, vB)**0.5
#     # Get cosine value
#     cos_ = dot_prod/magA/magB
#     # Get angle in radians and then convert to degrees
#     angle = math.acos(dot_prod/magB/magA)
#     # Basically doing angle <- angle mod 360
#     ang_deg = math.degrees(angle)%360
#
#     if ang_deg-180>=0:
#         # As in if statement
#         return 360 - ang_deg
#     else:
#
#         return ang_deg

def ang(P1X,P1Y,P2X,P2Y,P3X,P3Y):
   numerator = P2Y*(P1X-P3X) + P1Y*(P3X-P2X) + P3Y*(P2X-P1X)
   denominator = (P2X-P1X)*(P1X-P3X) + (P2Y-P1Y)*(P1Y-P3Y)
   print numerator
   print denominator
   if denominator != 0:
     ratio = numerator/denominator
     angleRad = math.atan(ratio);
     angleDeg = (angleRad*180)/3.1416;
     return angleDeg
   # print angleDeg
   # if angleDeg<0:
   #     angleDeg = 180+angleDeg
   #     return angleDeg

print leaderAnt
print followerAnt
# exit()

#########################Produce Angles#########################################

arrayOfFifteensFollower = list()
arrayOfFifteensLeader = list()
i = 0

# I dont know why I choose two, but it seems to work fine
# Does it make sense to do it on every single frame
for i in range(0,len(followerAnt)):
    # print "Iteration", i # Python is an interesting language (no concat?)
    # print followerAnt[i]
    arrayOfFifteensFollower.append(followerAnt[i])
    arrayOfFifteensLeader.append(leaderAnt[i])

i = 0

arrayOfAngles = list()
arrayOfAngles2 = list()
for i in range(0, len(arrayOfFifteensLeader)-15):

    # Follower points to leader X
    x = ang(arrayOfFifteensFollower[i][0], arrayOfFifteensFollower[i][1],
    arrayOfFifteensFollower[i+15][0], arrayOfFifteensFollower[i+15][1],
    arrayOfFifteensLeader[i+15][0], arrayOfFifteensLeader[i+15][1])


    # Leader points to follower Y
    y = ang(arrayOfFifteensLeader[i][0], arrayOfFifteensLeader[i][1],
    arrayOfFifteensLeader[i+15][0], arrayOfFifteensLeader[i+15][1],
    arrayOfFifteensFollower[i+15][0], arrayOfFifteensFollower[i+15][1])

    # clean up the none values
    if x is None:
        print "None"

    else:
        arrayOfAngles.append(x)

    if y is None:
        print "None"

    else:
        arrayOfAngles2.append(y)

# print arrayOfAngles
# print arrayOfAngles2

print "Mean of Follower: ", np.mean(arrayOfAngles)
print "Mean of Leader: ", np.mean(arrayOfAngles2)
print "Max of Follower: ", max(arrayOfAngles)
print "Max of Leader: ", max(arrayOfAngles2)
print "Mean - Max of Follower: ", np.mean(arrayOfAngles) - max(arrayOfAngles)
print "Mean - Max of Leader : ", np.mean(arrayOfAngles2) - max(arrayOfAngles2)
print "Standard Deviation of Follower: ", np.std(arrayOfAngles)
print "Standard Deviation of Leader: ", np.std(arrayOfAngles2)


mu, sigma = 0, 0.1 
count, bins, ignored = plt.hist(arrayOfAngles, 10, normed=True)
plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) ), linewidth=2, color='r')
print "This", 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2))
plt.show()

count, bins, ignored = plt.hist(arrayOfAngles2, 10, normed=True)
plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) ), linewidth=2, color='r')
print "This", 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2))
plt.show()


# plt.hist(arrayOfAngles)
# plt.show("Follower")

# plt.hist(arrayOfAngles2)
# plt.show("Leader")

h = sorted(arrayOfAngles)
fit = stats.norm.pdf(h, np.mean(h), np.std(h))  #this is a fitting indeed
pl.plot(h,fit,'-o')
pl.hist(h,normed=True)      #use this to draw histogram of your data
pl.show()                   #use may also need add this 

h = sorted(arrayOfAngles2)
fit = stats.norm.pdf(h, np.mean(h), np.std(h))  #this is a fitting indeed
pl.plot(h,fit,'-o')
pl.hist(h,normed=True)      #use this to draw histogram of your data
pl.show() 