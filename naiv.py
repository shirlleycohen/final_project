from __future__ import print_function
import math
import scipy.io as sio
import sys
import numpy
from math import hypot

max = 0;
k = 3;
temp = [];
final = []
newV = [];
trucks = [];
path = [['0' for x in range(1)] for y in range(k)];
inks = [];
flag=0;

v = [['0', 0, 0], ['1', 2, 4], ['2', -3, 2], ['3', 5, -8], ['4', 6, 1], ['5', 6, 5], ['6', 10, 2], ['7', -4, 6],
     ['8', -5, -5], ['9', -1, -3], ['10', 10, -5]]
goTo = ['1','2', '3','5','7','8','10'];
newV.append(v[0]);


if (k == 0):  # in case there is 0 channels
    exit();

for x in goTo:# create subArray from V-to create final.
    for y in v:
        if y[0] == x:
            newV.append(y);
print("newV", newV);


for x in newV:# create final table.
    temp = [];
    for y in newV:
        dis = math.hypot(x[1] - y[1], x[2] - y[2]);
        temp.append(dis);
        if dis > max:
            max = dis+10;
    final.append(temp);

trucks = numpy.zeros(k);

for x in goTo:# create copy from goTo
    inks.append(x);
k = len(goTo);

while k != 0:
    i = 0;
    for x in trucks:
        print(i);
        min = max;
        for y in goTo:
            place = inks.index(y) + 1;# index of the next v
            dis = final[int(x)][int(place)];#distnation fron place to next v.
            if dis < min:
                min = dis;
                nextV = y;
                nextIndex = place;
        print("The next V is:",nextV," And the index it's:",nextIndex);
        path[i].append(nextV);
        if len(goTo) != 1:
            goTo.remove(nextV);
            trucks[i] = nextIndex
            i = i + 1;
            k = len(goTo);
        else:
            trucks[i] = nextIndex;
            flag=1;
            break;
    if(flag==1):
            break;

print (path);
print (trucks);
