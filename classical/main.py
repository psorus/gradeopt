import os
import json
import numpy as np

from lister import *


def load(q,q0=""):
  if len(str(q0))>0:q=q+" (="+str(q0)+")"
  x=input(q+":\n")
  if len(x)==0:x=str(q0)
  
  return x


def loadlist(q,p):
  print(q)
  ret=[]
  while True:
    ac=[]
    for zw in p:
      ac.append(load(zw))
    ret.append(ac)
    cont=load("Another grade? Enter anything to stop","")
    if len(cont)>0:break
  return ret

def modlist(q):
  return [[ac[0],float(ac[1]),int(ac[2])] for ac in q]


def getdata():
  ret={}
  ret["total_cp"]=int(load("Total Credit points needed",120))
  ret["thesis_cp"]=int(load("How many credit points are given for the master thesis",60))
  ret["thesis_grade"]=float(load("Average grade for your master thesis"))
  ret["neccesary"]=modlist(loadlist("First enter all neccesary grades (for example particle physics 1 for the particle physics track",["Enter an identifier","Enter your grade","How many credits for this course"]))
  ret["optional"]=modlist(loadlist("Now enter all optional grades (for example Deep Learning or Astroparticle physics for the particle physics track",["Enter an identifier","Enter your grade","How many credits for this course"]))
  return ret
  

if os.path.isfile("data.json"):
  with open("data.json","r") as f:
    q=json.loads(f.read())
else:
  q=getdata()
  with open("data.json","w") as f:
    f.write(json.dumps(q))

ncp=np.sum([zw[2] for zw in q["neccesary"]])
nsm=np.sum([zw[1]*zw[2] for zw in q["neccesary"]])
thesiscp=q["thesis_cp"]
coursecp=q["total_cp"]-q["thesis_cp"]
thesisgrade=q["thesis_grade"]


def isval(o):#optional ones
  acp=np.sum([zw[2] for zw in o])
  return acp+ncp>coursecp

def subeval(o):
  acp=np.sum([zw[2] for zw in o if not zw[1]==0.0])#allow ungraded courses
  acg=np.sum([zw[1]*zw[2] for zw in o])
  return acp+ncp,nsm+acg

def eval(o):
  if not isval(o):return 9.0
  acp,acg=subeval(o)
  acp+=thesiscp
  global thesisgrade
  acg+=thesiscp*thesisgrade
  return acg/acp
  
# print(eval(q["optional"]))
  
def fulleval(o):
  rel=[]
  i=0
  print("calculating...",thesisgrade)
  for com,dex in bothlist(o):
    ac=eval(com)
    rel.append({"grade":ac,"com":com})
    # print(i,dex)
    i+=1
  return sorted([zw for zw in rel if zw["grade"]<6],key=lambda q:q["grade"])

def bestgrade(o):
  return fulleval(o)[0]["grade"]
def gradebytgrade(tgrade,o):
  global thesisgrade
  thesisgrade=tgrade
  return bestgrade(o)

tgrade=np.arange(1.0,4.0001,0.01)
tgrade=[1.0,1.3,1.7,2.0,2.3,2.7,3.0,3.3,3.7,4.0]
grades=[gradebytgrade(zw,q["optional"]) for zw in tgrade]

print(tgrade)
print(grades)

# np.savez_compressed("output",x=tgrade,y=grades)



# acd=fulleval(q["optional"])

# print(acd)















