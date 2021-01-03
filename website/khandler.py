from handler import *



class khandler(handler):
  def __init__(s,gen_new,nam=None,SECRET_KEY=b'12'):
    handler.__init__(s,gen_new,nam=None,SECRET_KEY=b'12')
  
  
  # def addroute(s):#needed to allow for parametric functions
    # s.app.add_url_rule("/<function>/<parameter>","main",s.main)
    # s.app.add_url_rule("/<function>","main",s.main)
    # s.app.add_url_rule("/","main",s.mainf)
    
  def outerlayer(s,q):
    return '''<html><head><title>This has no title yet</title></head><body>
    ###
    </body></html>'''.replace("###",str(q))
  
  def main(s,function="",**kw):
    return s.outerlayer(handler.main(s,function,**kw))
    