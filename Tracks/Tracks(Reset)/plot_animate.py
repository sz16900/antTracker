# To Do:
    # Label the arrays, ant follower, leader, etc
    # This is not ver DRY, things repeat too much, but it makes some sense


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider

#####################################Read File##################################
filename = "tracks7.txt"
f = open(filename, 'r')
f.next() # lets skip the header
my_list = list()
counter = 0
for line in f:
  if "RESET" in line:
    print "Skipping"
  else:
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
      print "Skipping"
  else:
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

# This is to find the minimun and maximun value to use for graph
xy = np.min(leaderAnt, axis=0)
minx = xy[0]
miny = xy[1]
xy = np.max(leaderAnt, axis=0)
maxx = xy[0]
maxy = xy[1]

################################################################################

# plt.figure()
# ax = plt.gca()

# ax.set_xlim([minx, maxx])
# ax.set_ylim([miny, maxy])

# def update(val):

#     # This is to have a track or just points
#     # ax.clear()
#     i = int(round(sfreq.val))

#     # This needs to be a bit more DRY

#     if i > len(leaderAnt)-2:
#         print "Reached Boundry"
#     else:
#         X, Y = leaderAnt[i]
#         U, V = leaderAnt[i+1]
#         ax.annotate("", xy=(U, V), xytext=(X, Y),
#                 arrowprops=dict(arrowstyle="->", color='red'))
#     if i > len(followerAnt)-2:
#         print "Reached Boundry"
#     else:
#         A, B = followerAnt[i]
#         C, D = followerAnt[i+1]
#         ax.annotate("", xy=(C, D), xytext=(A, B),
#             arrowprops=dict(arrowstyle="->"))

# axfreq = plt.axes([0.25, 0.03, 0.65, 0.03])

# # Find how big the slider should be
# if len(leaderAnt) > len(followerAnt):
#     sliderLength = len(leaderAnt)
# else:
#     sliderLength = len(followerAnt)

# sfreq = Slider(axfreq, 'Next', 0, sliderLength, valinit=0)
# sfreq.on_changed(update)

# plt.show()

fig, ax = plt.subplots()

for i in range(len(leaderAnt) - 1):
    print "frame: ", i
    X, Y = leaderAnt[i]
    A, B = followerAnt[i]
    if i == 0:
        points, = ax.plot(X, Y,  marker='o', linestyle='None')
        points2, = ax.plot(A, B, marker='o', linestyle='None')
        ax.set_xlim([minx, maxx])
        ax.set_ylim([miny, maxy]) 
    else:
        points.set_data(X, Y)
        points2 .set_data(A, B)
    plt.pause(0.0001)
