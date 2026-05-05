#obj = { key: value, key:value , key:value}
book = {"chap1":10 , "chap2":20 ,"chap3":30}

# add new key-values
book["chap4"] = 40
book["chap5"] = 50
book["chap6"] = 60

print(book)

# diplay individual values
print(book["chap1"]) # 10
print(book["chap2"]) # 20

# display keys
print(book.keys())

for k in book.keys():
    print(k)

# dislay values
print(book.values())

for v in book.values():
    print(v)

# display item(key,value)
print(book.items())

for k,v in book.items():
    print(k,v)

# remove key-value
book.pop("chap1") # chap1-10 will be removed
print("After removing:",book)