#usage
#python <script>.py  xlen ylen Ants particles iteration
#python ClusterACO.py  xlen ylen Ants particles iteration
#runfile('ClusterACO.py',args='20 20 10 10 30')
#runfile('D:/GDrive/20191202_PSOvsACO_Python/clusterACO/ClusterACO.py',args='20 20 10 75 30')


import math
import sys
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from random import randint
from itertools import cycle
cycol = cycle('bgycmk')
import time
import os
timestr = time.strftime("%Y%m%d-%H%M%S")
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
#headN=5
#particles=50
#iteration=20
counter=0



def printarray(printarray):
	for i in printarray:
		print(i)

def findCount(list,cluster):
  j=0
  for i in list:
    if i[4]==cluster:
      j=j+1
  return j

def phermoneCount(headlist,list,phermone):
	for i in range(len(headlist)):
		dim1=headlist[i]-1
		phermone[dim1][i]=phermone[dim1][i]+1
		#print(dim1)
	printarray(phermone)
	return phermone  
  
#in ACO the ant would try to visit all the nodes. and leave behind a pheromone signature on visited nodes. 
#same is acheived via a array list of total no of elements/particles

def mutate(headlist,list,headN,phermone,iteration):
  iteration=iteration+2
  #print("\n")
  #printarray(list)
  #print("\n")
  #printarray(phermone)
  print("\n")
  for i in range(headN): # for each ant i
    #counter=0
    #count=findCount(list,i)
    #stop=randint(0, count+1)
    #ph=phermone[i]
    occupied=[]
    for j in range(len(list)): # for each particle
      #occupied=[]
      
      
      if phermone[j][i]==0 and not(iteration in phermone[j]):# and not(j in occupied):
        headlist[i]=list[j][6]
        occupied.append(j)
        phermone[j][i]=iteration
        #print("occ1="+str(occupied))
        break
      else:
			  #node has already been occupied by the ant 
			  #move to next node
        #k=j
        while 1==1:
          p=randint(0,len(list)-1)
				  #finding next available space to park the ant
          #and make sure the position is not occupied by another ant
          if phermone[p][i]==0 and not(iteration in phermone[p]):#and not(p in occupied):
            headlist[i]=list[p][6]
            occupied.append(p)
            phermone[p][i]=iteration
            #print("occ2="+str(occupied))
            break
        break


  return headlist

def plotGraph(list,headN,counter,headlist,D,text):
  savestring=text+str(counter)+'.png'
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
        #nearestKey=j-1
        i[4]=cluster
        i[5]=D
        i[2]=k[0]
        i[3]=k[1]

      cluster=cluster+1
  return list

def initialize(xl,yl,particles,headN):
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

def initializePheromone(particles,headN):
	return  [[0 for col in range(headN)] for row in range(particles)]
  

DD=sys.maxsize
list=initialize(xlen,ylen,particles,headN)
phermone=initializePheromone(particles,headN)
#print(phermone)
Dlist=list
#for i in list:
 #  print(i)
   #print("\n")


fig = plt.figure(figsize=(xlen, ylen))
ax = fig.add_subplot(111)

# #points = []
# #last = 0
# #bound = 100
# #for i in range(0, 100):
# #  last += randint(-bound, bound)
# #  points.append(last)

for j in list:
  ax.plot([j[0],j[2]],[j[1],j[3]],marker='D',c=next(cycol))
# fig.savefig('graphStart.png')

 #initialize random centre nodes
headlist=[]
fig1 = plt.figure(figsize=(xlen, ylen))
ax1 = fig1.add_subplot(111)
for k in range(headN):
	k=randint(0, particles)
	while k in headlist:
		k=(randint(0, particles-1))
	headlist.append(int(math.sqrt(k*k)))
	j=list[k-1]
	ax1.plot([j[0],j[2]],[j[1],j[3]],marker='o',c=next(cycol))
# fig1.savefig('graphNode.png')

print("\n")
print("heads are : ")
print(headlist)
list=makeClusters(list,headlist)
print("\n")
# #print(lsit)
for i in list:
   print(i)
   
print("length of list is :")
print(len(list))

for i in range(particles):
 print(phermone[i])
 print(list[i][1],list[i][2])
 
phermone=phermoneCount(headlist,list,phermone)
stats=[]
for m in range(iteration):

 
	D=findEntrieDistance(list)
	#phermone marking
	#phermone=phermoneCount(headlist,list,phermone)
	#print("\n")
	#printarray(phermone)
	#printarray(headlist)
	#print("\n")


	print("Iteration "+str(m)+" D "+str(D)+" DD "+str(DD))
	stats.append([D,DD,m])
	if D<DD:
	  sstr=path1+'\\'+timestr+'GraphBest '
	  plotGraph(list,headN,counter,headlist,D,sstr)
	  Dlist=list

	  DD=D
	headlist=mutate(headlist,list,headN,phermone,m)
	list=makeClusters(list,headlist)
	sstr=path1+'\\'+timestr+'Iteration '
	plotGraph(list,headN,counter,headlist,D,sstr)
	#print("\n")
	
	#printarray(list)
	#print(headlist)
	#print("\n")
	counter=counter+1
#print("Iteration "+str(m)+" D "+str(D)+" DD "+str(DD))

printarray(stats)

#for i in stats:
#    printString="The Err % at run "+str(i[2])+" is "+str(float(((float(i[0]-DD))/float(DD))*100))
#    print(printString)
#

count2=0
sum2=0.0
for i in stats:
    printString="The Err % at run "+str(i[2])+" is "+str(float(((float(i[0]-DD))/float(DD))*100))
    count2=count2+1
    sum2=sum2+float(((float(i[0]-DD))/float(DD))*100)
    print(printString)

print("\n")
print("The Mean Error rate is "+str(sum2/count2))

# #ax.plot(points)
# #ax.plot([1, 2, 3, 4], [1, 4, 9, 3],marker='o',c=next(cycol))
# #ax.plot([1, 2, 3, 4], [1, 4, 9, 3],'r')
# #ax.plot([7, 5, 4, 2], [6, 8, 1, 3],marker='o',c=next(cycol))
# #ax.plot([7, 5, 4, 2], [6, 8, 1, 3],'g')
# #ax.plot([6, 3, 2, 1], [3, 5, 7, 0],marker='o',c=next(cycol))
# #ax.plot([6, 3, 2, 1], [3, 5, 7, 0],'b')
# #fig.savefig('graph.png')



