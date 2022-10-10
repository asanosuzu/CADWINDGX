nn=6
a = [[0]*8]*nn
for k in range(nn):
    b=[0]*8
    for j in range(8):
        b[j] = k
    a[k] = b

print(a)

