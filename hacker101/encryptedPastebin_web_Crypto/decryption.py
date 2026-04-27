decrypted = ""
encrypted = input("encrypted string: ")
for i in encrypted:
    if (i == '~'):
        current = '='
    elif (i == '!'): 
        i = '/'
    elif (i == '-'):
        current = '+'
    else : current = i
    
    decrypted += current
print(decrypted)
