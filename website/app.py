# from grademath import *


# print(optimize(loadorgen()))
# print(gradebytgrade(4.0,loadorgen()["optional"]))


from kstate import *
from khandler import *


k=khandler(lambda:kstate())
app=k.app
if __name__=="__main__":
  k.run()





