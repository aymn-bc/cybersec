from pwn import *

solution = ""
for i in 'label':
    # solution += chr(ord(i) ^ 13)   => solution 1 
    solution += xor(ord(i), 13).decode("utf-8") # => solution 2

print("crypto{" + solution + "}")

# BOTH SOLUTION WORKS