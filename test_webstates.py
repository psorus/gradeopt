from handler import *
from webstate import *



class shop(webstate):

  def __init__(s):
    webstate.__init__(s)
    s["max_stock"]=10
    s["stock"]=10
    s.setstate("full")
  
  
####


  def getstates(s):return ["full","available","selling","sold","soldout","restocking"]
  
  def leave_soldout(s,into):return s["stock"]>0 or into=="restocking"
  
  def into_selling(s,leave):return s["stock"]>0
  
  def init_selling(s,leave):
    print("selling one object")
    s["stock"]-=1
    s.setstate("sold")
  
  def init_sold(s,leave):
    print("gratulations")
    if s["stock"]==0:
      s.setstate("soldout")
    else:
      s.setstate("available")
  
  
  def init_soldout(s,leave):
    print("out of order")
 
  
  def buy(s):
    print("trying to buy")
    s.map({"available":"selling","full":"selling","soldout":lambda:print("sadly no longer available")})
  
  def restock(s):
    print("restocking...")
    s.map({"available":"restocking","soldout":"restocking","full":lambda:print("cannot restock, already full")})
    # s.setstate("restocking")
  
  def init_restocking(s,leave):
    s["stock"]+=1
    print("restocked")
    s.setstate("available")
    s.setstate("full")
  
  def into_full(s,leave):return s["stock"]==10
  
  def into_restocking(s,leave):return leave != "full"
  
  def init_full(s,leave):print("completely full again")
  
  
  def available(s):
    return s.iseitherstate(["available","full"])



  
####

  def buttonbuy(s):
    return f'<br><a href="/buy">Buy item</a>'
  def buttonrestock(s):
    return f'<br><a href="/restock">Restock an item</a>'



  def vis_full(s):
    return f'Currently a full stock of {s["stock"]}'+s.buttonbuy()
  def vis_available(s):
    return f'Currently able to sell {s["stock"]} items'+s.buttonbuy()+s.buttonrestock()

  def vis_soldout(s):
    return 'Sadly, there are currently no more things to buy'+s.buttonrestock()
  def vis(s,state):
    return f"visualising for state {state} not yet implemented. This should go away by reloading the page (obviously ignoring that this should not be possible at all)"
    

k=handler(lambda:shop())
k.run()

#notice that this shop is kind of useless, since everybody has his own shop


