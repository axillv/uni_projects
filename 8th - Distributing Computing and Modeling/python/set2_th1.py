import math
b=1000000
r=1000000

round=0
while r>1.01:
    r=r-(r*(r-1)/(2*b-2))
    round+=1
print(round)