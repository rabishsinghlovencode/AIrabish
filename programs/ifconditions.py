###############
# if condition
if 1 < 2:
        
    print("true")
    print("inside if")
    print("still inside if")




name = "python programming"
if "python" in name:
    print("you are learning python")

if len(name) == 18:
    print("its python programming")
####################
# if-else condition 
if "python" in name:
    print("you are learning python")
else:
    print("you are learning java")

######################################
# if-elif-elif-elif-elif-else conditions
lang = input("Enter any language:")
if lang == "python":
    print("you are learning python")
elif lang == "unix":
    print("you are lerning unix")
elif lang == "oracle":
    print("you are learning oracle")
else:
    print("you are learning data science")