
def sublister(q,modulo=1):
  i=0
  j=0
  while True:
    yield j % q
    i+=1
    if i % modulo==0:j+=1


# def lister(q):
  
  # lea=q
  # border=lea
  # gen=[sublister(q)]
  
  # i=0
  # while True:
    # ac=[zw.__next__() for zw in gen]
    # yield ac
    # i+=1
    # if i==border:
      # q-=1
      # if q<=0:break
      # gen.insert(0,sublister(q,modulo=border))
      # border*=lea
      # i=0

def lister3(q,modulo=1):
  """all numbers from 0 to q with modulo"""
  i=0
  j=0
  while True:
    yield i
    j+=1
    if not j%modulo:
      i+=1
      if i==q:i=0
    
    
  for i in range(q):yield i#yes kind of stupid

def valid(q):
  if len(q)<2:return True
  for i in range(len(q)-1):
    if q[i]>=q[i+1]:return False
  return True

def lister2(l,q):
  """all possible combinations with len l up to q where each number is always bigger than the last"""
  k=[lister3(q,q**i) for i in range(l)]
  for i in range(q**l):
    ac=[zw.__next__() for zw in k]
    if valid(ac):yield ac


def lister(q):
  """all possible combinations up to q"""
  for i in range(q):
    for zw in lister2(i+1,q):
      yield zw 

def allelem(q):
  """all element combinations in q, assuming pertubility"""
  for dex in multibool(len(q)):
    yield [q[i] for i in dex]

def bothlist(q):
  """allelem+lister"""
  for dex in multibool(len(q)):
    yield [q[i] for i in dex],dex


def booloop(modulo=1):
  """boolean iterator with a modulo"""
  i=0
  j=0
  while True:
    yield bool(i%2)
    
    j+=1
    if not j%modulo:i+=1

def multibool(q):
  """multiple (q) boolean iterators"""
  ret=[booloop(modulo=2**i) for i in range(q)]
  for i in range(2**q):
    ac= [i for i,q in enumerate(ret) if q.__next__()]
    if not len(ac)==0:yield(ac)




# def test(q):
  # for i in range(q):
    # yield(i)




if __name__=="__main__":
  for q in allelem(["a","b","c"]):
  # for q in multibool(5):
    print(q)