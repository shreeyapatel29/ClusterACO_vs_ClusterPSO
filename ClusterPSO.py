#usage
#python <script_name> xlen ylen headN particles iteration
#python <ClusterPSO.py> 20 20 10 10 10
#runfile('ClusterPSO.py',args='20 20 10 10 30')
#runfile('D:/GDrive/20191202_PSOvsACO_Python/ClusterPSO/ClusterPSO.py',args='20 20 10 75 30')
#runfile('D:/GDrive/20191202_PSOvsACO_Python/clusterPSO/ClusterPSO.py',args='20 20 10 75 30')


#xlen=20
##xlen=10
#ylen=20
##ylen=10
#headN=10
#particles=200
#iteration=10


import time
import math
import sys
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from random import randint
from itertools import cycle
cycol = cycle('bgycmk')
timestr = time.strftime("%Y%m%d-%H%M%S")
import os
print(os.path.dirname(os.path.realpath(__file__)))

path1=os.path.dirname(os.path.realpath(__file__))

print(' ')
xlen=int(sys.argv[1])
printString="xlen is :\t"+str(xlen)
print(printString)

ylen=int(sys.argv[2])
printString="ylen is :\t"+str(ylen)
print(printString)

headN=int(sys.argv[3])
printString="headN is :\t"+str(headN)
print(printString)

particles=int(sys.argv[4])
printString="particles is :\t"+str(particles)
print(printString)

iteration=int(sys.argv[5])
printString="iteration is :\t"+str(iteration)
print(printString)

print(' ')


#xlen=20
##xlen=10
#ylen=20
##ylen=10
#headN=10
#particles=200
#iteration=10




def printarray(printarray):
	for i in printarray:
		print(i)


def findCount(list,cluster):
  j=0
  for i in list:
    if i[4]==cluster:
      j=j+1
  return j

def mutate(headlist,list,headN):
  for i in range(headN):
    counter=0
    count=findCount(list,i)
    stop=randint(0, count+1)
    for j in list:
      if j[4]==i:
        counter=counter+1
        if counter==stop:
          headlist[i]=j[6]
  return headlist

def plotGraph(list,headN,counter,headlist,D,text):
  savestring=path1+'\\'+text+str(counter)+'.png'
  #print(savestring)
  fig = plt.figure(figsize=(xlen, ylen))
  ax = fig.add_subplot(111)
  for i in range(headN):
    col=next(cycol)
    for j in list:
      if j[4]==i:
        ax.plot([j[0],j[2]],[j[1],j[3]],marker='D',c=col)
  for k in headlist:
    l=list[k]
    ax.plot([l[0],0],[l[1],0],'r--')
  savestring2='Cluster at solution: '+str(D)+' @iteration: '+str(counter)
  fig.suptitle(savestring2,fontsize=20)
  #saveStr=timestr+'graphNode.png'
  #fig1.savefig(saveStr)
  fig.savefig(savestring)

def findEntrieDistance(list):
  total=0.0
  for i in list:
    total=total+findDistance([i[0],i[1]],[i[2],i[3]])

  return total

def findDistance(i,j):
  #if i==j:
    #return  math.sqrt((i[0] - 0)**2 + (i[1] - 0)**2)
  return math.sqrt((i[0] - j[0])**2 + (i[1] - j[1])**2)

def makeClusters(list,headlist):
  for i in list:
    nearestDist=sys.maxsize
    nearestKey=0
    cluster=0
    for j in headlist:
      #dist=sys.maxint
      D=findDistance(i,list[j])
      if D<nearestDist:
        k=list[j]
        nearestDist=D
        nearestKey=j
        i[4]=cluster
        i[5]=D
        i[2]=k[0]
        i[3]=k[1]

      cluster=cluster+1
  return list





def initialize(xl,yl,particles):
  print("inside initialize")
  print(xl,yl,particles)
  list=[]
  count=0
  for i in range(particles):
    x=randint(0, xl)
    y=randint(0, yl)
    list.append([x,y,0,0,0, math.sqrt((x - 0)**2 + (y - 0)**2),count])
    count=count+1
  return list


counter=0

DD=sys.maxsize
list=initialize(xlen,ylen,particles)
Dlist=list
print(list)
fig = plt.figure(figsize=(xlen, ylen))
ax = fig.add_subplot(111)

#points = []
#last = 0
#bound = 100
#for i in range(0, 100):
#  last += randint(-bound, bound)
#  points.append(last)

for j in list:
 ax.plot([j[0],j[2]],[j[1],j[3]],marker='D',c=next(cycol))
saveStr=timestr+'graphStart.png'
fig.savefig(saveStr)

#initialize random centre nodes
headlist=[]
fig1 = plt.figure(figsize=(xlen, ylen))
ax1 = fig1.add_subplot(111)
for k in range(headN):
  headlist.append(randint(0, particles))
  j=list[k]
  ax1.plot([j[0],j[2]],[j[1],j[3]],marker='o',c=next(cycol))
saveStr=timestr+'graphNode.png'
fig1.savefig(saveStr)
#fig1.savefig('graphNode.png')
print("\n")
print("heads are : ")
print(headlist)
list=makeClusters(list,headlist)
print("\n")
#print(lsit)
for i in list:
  print(i)
stats=[]
for m in range(iteration):
 
  D=findEntrieDistance(list)
  print("Iteration "+str(m)+" D "+str(D)+" DD "+str(DD))
  sstr=timestr+'Iteration'
  print(sstr)
  plotGraph(list,headN,counter,headlist,D,sstr)
  stats.append([D,DD,m])
  if D<DD:
    sstr=timestr+'GraphBest'
    plotGraph(list,headN,counter,headlist,D,sstr)
    Dlist=list
    
    DD=D
  headlist=mutate(headlist,list,headN)
  list=makeClusters(list,headlist)
  counter=counter+1


printarray(stats)

count2=0
sum2=0.0
for i in stats:
    printString="The Err % at run "+str(i[2])+" is "+str(float(((float(i[0]-DD))/float(DD))*100))
    count2=count2+1
    sum2=sum2+float(((float(i[0]-DD))/float(DD))*100)
    print(printString)

print("\n")
print("The Mean Error rate is "+str(sum2/count2))

#ax.plot(points)
#ax.plot([1, 2, 3, 4], [1, 4, 9, 3],marker='o',c=next(cycol))
#ax.plot([1, 2, 3, 4], [1, 4, 9, 3],'r')
#ax.plot([7, 5, 4, 2], [6, 8, 1, 3],marker='o',c=next(cycol))
#ax.plot([7, 5, 4, 2], [6, 8, 1, 3],'g')
#ax.plot([6, 3, 2, 1], [3, 5, 7, 0],marker='o',c=next(cycol))
#ax.plot([6, 3, 2, 1], [3, 5, 7, 0],'b')
#fig.savefig('graph.png')



#runfile('D:/GDrive/20191202_PSOvsACO_Python/ClusterPSO/ClusterPSO.py',args='20 20 10 75 30')