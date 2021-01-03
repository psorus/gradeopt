from flask import Flask,make_response,session

import json



class controller():
  def __init__(s,gen_new,nam=None,SECRET_KEY=b'12'):
    s.q={}
    s.gen_new=gen_new
    s.max_id=0
    if nam is None:nam=__name__
    s.app=Flask(nam)
    s.app.config["SECRET_KEY"]=SECRET_KEY
    s.addroute()

  def addroute(s):
    s.app.add_url_rule("/","main",s.main)
  def run(s):
    s.app.run()
  
  def _create_new(s,index):
    # print("creating new index",index)
    s.q[index]=s.gen_new()
  
  def _findid(s):
    if "id" in session.keys():
      if session["id"] in s.q.keys():
        return int(session["id"])
    s._create_new(s.max_id)
    session["id"]=s.max_id
    s.max_id+=1
    return s.max_id-1
  
  def _getobj(s):
    return s.q[s._findid()]

  def callfunc(s,func,*p,**kw):
    obj=s._getobj()
    return getattr(obj,func)(*p,**kw)


  def main(s):
    return s.callfunc("main")
    ret="Hello World "+str(s.id)
    if not "key" in session.keys():
        session["key"]=str(np.random.randint(1000,10000))
    ret+=" "+str(session["key"])
    #ret=str(session)
    # return ret
    resp=make_response(ret)
    resp.set_cookie("test1","I am the cookie")
    return resp
    # return str(session["uid"])+"\n"+s.findwho().main()



class handler(controller):
  """a controller made to work with webstates"""
  def __init__(s,gen_new,nam=None,SECRET_KEY=b'12'):
    controller.__init__(s,gen_new,nam=nam,SECRET_KEY=SECRET_KEY)
  
  
  def addroute(s):
    s.app.add_url_rule("/<function>","main",s.main,methods=['GET','POST'])
    s.app.add_url_rule("/","main",s.main)
  
  
  def main(s,function="",**kw):
    ret=None
    if not (function=="" or function[0]=="_"):ret=s.callfunc(function,**kw)#can only call functions that are not of type _something
    if  type(ret) in [str,bool,float,int]:
      return str(ret)
    elif type(ret) in [list,dict]:
      return json.dumps(ret,indent=2)
    else:
      return s.callfunc("statefunc","vis",**kw)

    

  
