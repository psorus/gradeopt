from webstate import *

from webhelper import *

from flask import request


import os

class kstate(webstate):

  def __init__(s):
    webstate.__init__(s)

  def getstates(s):return ["new","prelogin","preregister","loggedin","stdinf","needed","optional","calculating","results"]
  
  
  def vis(s,state):
    return f"The current state ({state}) is not visualizable"

  def setname(s):
    s.name=request.form["name"]
    if os.path.exists(s.name+".txt"):
      s.setstate("prelogin")
      ##load everything
    else:
      s.setstate("preregister")
  
  def resetstate(s):
    s.setstate("new")

  def register(s):
    s.passw=request.form["pass"]
    s.setstate("loggedin")
  
  def login(s):
    pw=request.form["pass"]
    if pw=s.passw:
      s.setstate("loggedin")
      
  
  def vis_new(s):
    return generateform("setname",[{"name":"name","desc":"How should I call you?"}],submit="Hello")
  
  # def vis_prelogin(s):
  def vis_preregister(s):
    return f"""Hello {s.name} {generatelink('resetstate','Not you?')}<br>"""+generateform("register",[{"name":"pass","desc":"Please enter your password","typ":"password"}],submit="Register")
  # def vis_loggedin(s):
  # def vis_stdinf(s):
  # def vis_needed(s):
  # def vis_optional(s):
  # def vis_calculating(s):
  # def vis_results(s):
  







