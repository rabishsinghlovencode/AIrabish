

alist = [34,67,23,65,26,37]
alist.append(90)        # adding single value
print("After appending:",alist)
alist.extend([84,19,84]) # adding multiple values
print("After extending:",alist)
alist.insert(1,16)
print("after inserting:",alist)
alist.pop(4) # 4 is the index - remove value at that index
print("After pop operation:",alist)
alist.remove(90)  # removing value directly
print("After removing:",alist)
alist.reverse()
print("After reversing:",alist)
alist.sort()
print("After sorting:",alist)
