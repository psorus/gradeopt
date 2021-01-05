from webstate import *

from webhelper import *

from flask import request

import json

import os

from betterhash import bhash as hash

from grademath import *


class kstate(webstate):

  def __init__(s):
    webstate.__init__(s)
    s.loggedin=False

  def getstates(s):return ["new","prelogin","preregister","loggedin","stdinf","needed","addneeded","optional","addoptional","calculating","results","missingstuff"]
  
  
  def vis(s,state):
    return f"The current state ({state}) is not visualizable"

  def setname(s):
    s['name']=request.form["name"]
    s._postname()
  def _postname(s):
    if s.exist():
      s.load()
    
    if s.hasvar("pass"):
      s.setstate("prelogin")
    else:
      s.setstate("preregister")
  
  def resetstate(s):
    s.setstate("new")

  def register(s):
    s["pass"]=hash(request.form["pass"])
    s.loggedin=True
    s.setstate("loggedin")
  
  def login(s):
    pw=request.form["pass"]
    # print("comparing passwords",hash(pw),s['pass'])
    if hash(pw)==s["pass"]:
      s.loggedin=True
      s.setstate("loggedin")
  def gotologgedin(s):
    s.setstate("loggedin")
  def gotoaddneeded(s):
    s.setstate("addneeded")
  def gotoaddoptional(s):
    s.setstate("addoptional")
  
  def addneeded(s):
    if not s.hasvar("needed"):
      s["needed"]=[]
    s["needed"].append([request.form["desc"].strip(),float(request.form["grade"].strip()),int(request.form["cp"].strip())])
    s.setstate("needed")
  def addoptional(s):
    if not s.hasvar("optional"):
      s["optional"]=[]
    s["optional"].append([request.form["desc"].strip(),float(request.form["grade"].strip()),int(request.form["cp"].strip())])
    s.setstate("optional")
  
  def gotocalculating(s):
    s.setstate("calculating")
  def gotoresults(s):
    if s.hasvar("results"):
      s.setstate("results")
    else:
      s.setstate("missingstuff")
  
  def startgeneral(s):
    s.setstate("stdinf")
  def startneeded(s):
    s.setstate("needed")
  def startoptional(s):
    s.setstate("optional")
  def enterstdinf(s):
    s["thesisgrade"]=float(request.form["thesisgrade"].strip())
    s["totalcp"]=int(request.form["totalcp"].strip())
    s["thesiscp"]=int(request.form["thesiscp"].strip())
    
    s.setstate("loggedin")
    
  def vis_new(s):
    return generateform("setname",[{"name":"name","desc":"How should I call you?"}],submit="Hello")
  
  # def vis_prelogin(s):
  def vis_preregister(s):
    return f"""Hello {s['name']} {generatelink('resetstate','Not you?')}<br>"""+generateform("register",[{"name":"pass","desc":"Please enter your password","typ":"password"}],submit="Register")
  def vis_prelogin(s):
    return f"""Welcome Back {s['name']} {generatelink('resetstate','Not you?')}<br>"""+generateform("login",[{"name":"pass","desc":"Please enter your password","typ":"password"}],submit="Login")
    
  def vis_loggedin(s):
    return "What do you want to do?<br>"+generatelink("startgeneral","Enter general Information")+"<br>"+generatelink("startneeded","Enter Courses that are needed for your degree")+"<br>"+generatelink("startoptional","Enter Courses that your are free to choose from")+"<br>"+generatelink("gotocalculating","Calculate Results")+"<br>"+generatelink("gotoresults","View Results")
  def vis_stdinf(s):
    return generateform("enterstdinf",[
    {"name":"totalcp","desc":"Please enter the total number of credits needed","value":s.avar("totalcp",120)},
    {"name":"thesiscp","desc":"Please enter the number of credits that your thesis provides","value":s.avar("thesiscp",60)},
    {"name":"thesisgrade","desc":"Please enter the grade of your master thesis (averaged with thesis defence)","value":s.avar("thesisgrade","")},
    ],submit="Save")
  def vis_needed(s):
    ret="You do not have any needed courses registered yet"
    if s.hasvar("needed"):
      ret="Your currently saved courses are:<br>"+"<br>".join([f"{ac[0]}:{ac[1]}*{ac[2]}" for ac in s["needed"]])
    ret+="<br>"
    
    ret+=generatelink("gotoaddneeded","Add new course")+"<br>"
    ret+=generatelink("gotologgedin","Go Back")+"<br>"
    return ret
  def vis_addneeded(s):
    return generateform("addneeded",[
    {"name":"desc","desc":"How would you name this course?"},
    {"name":"grade","desc":"How well did you do? Enter 0 for ungraded courses and use '.'","value":"0.0"},
    {"name":"cp","desc":"How many credit points does this course provide?","value":"10"},
    ],submit="Add")
  def vis_optional(s):
    ret="You do not have any optional courses registered yet"
    if s.hasvar("optional"):
      ret="Your currently saved courses are:<br>"+"<br>".join([f"{ac[0]}:{ac[1]}*{ac[2]}" for ac in s["optional"]])
    ret+="<br>"
    
    ret+=generatelink("gotoaddoptional","Add new course")+"<br>"
    ret+=generatelink("gotologgedin","Go Back")+"<br>"
    return ret
  def vis_addoptional(s):
    return generateform("addoptional",[
    {"name":"desc","desc":"How would you name this course?"},
    {"name":"grade","desc":"How well did you do? Enter 0 for ungraded courses and use '.'","value":"0.0"},
    {"name":"cp","desc":"How many credit points does this course provide?","value":"10"},
    ],submit="Add")

  def _vishelper(s,q):
    return str(q["grade"])+":"+str([ac[0] for ac in q["com"]])
  def vis_results(s):
    return "If you choose the following optional courses, this would average to those numbers<br>"+"<br>".join([s._vishelper(ac) for ac in s["results"]])+"<br>"+generatelink("gotologgedin","Back")

  def init_calculating(s,fro):
    if not s.hasvar("thesisgrade","thesiscp","totalcp","optional","needed"):
      s.setstate("missingstuff")
      return 
    s["results"]=doit(**s.q)
    s.setstate("results")
  def vis_missingstuff(s):
    return "Please enter more information<br>"+generatelink("gotologgedin","Back")
  
  def save(s):
    # return ""
    # print(os.system("pwd"))
    # exit()
    if s.hasvar("name"):
      with open(f"{os.getcwd()}/users/{s['name']}","w") as f:
        f.write(json.dumps(s.asdict(),indent=2))
  
  def exist(s,f=None):
    if f is None:f=s['name']
    return os.path.isfile(f"{os.getcwd()}/users/{f}")
  
  def load(s,f=None):
    if f is None:f=s['name']
    with open(f"{os.getcwd()}/users/{f}","r") as f:
      s.loaddict(json.loads(f.read()))
  
  def into(s,fro,too):
    s.save()
    return True
  
  def avar(s,q,alt=""):
    if s.hasvar(q):return str(s[q])
    return alt
  
  def init(s,fro,too):
    if not s.hasvar("name"):#If I dont know who you are, you have to tell me
      if not too=="new":
        s.setstate("new")
        return
    if not s.loggedin:#I need a password from you
      if not (too=="new" or too=="prelogin" or too=="preregister"):
        s._postname()
  







