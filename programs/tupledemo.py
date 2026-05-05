

alist = [10,20,30]
alist[0] = 100
print("Updated list :",alist) # [100,20,30]


atup = (10,20,30)
#atup[0] = 1000
print("updated tuple :", atup)

# typecasting - converting from one object to another object
atup = (10,20,30)
alist = list(atup) # converting to list
alist[0] = 1000    # making changes
atup = tuple(alist)# reconverting back to tuple
print("updated tuple:",atup)