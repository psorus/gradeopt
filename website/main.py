# from grademath import *


# print(optimize(loadorgen()))
# print(gradebytgrade(4.0,loadorgen()["optional"]))


from kstate import *
from khandler import *


if __name__=="__main__":
  k=khandler(lambda:kstate())
  k.run()





