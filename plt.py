import matplotlib.pyplot as plt
import numpy as np


f=np.load("output.npz",allow_pickle=True)
x=f["x"]
y=f["y"]


plt.plot(x,y)
plt.xlabel("thesis grade")
plt.ylabel("final grade")

plt.savefig("grades.png",format="png")
plt.savefig("grades.pdf",format="pdf")


plt.show()



