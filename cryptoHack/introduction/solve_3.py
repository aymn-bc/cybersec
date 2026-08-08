from pwn import *

problem = "73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d"
decoded = bytes.fromhex(problem)

for i in range(0, 126):
    if "crypto" in xor(decoded, i).decode("utf-8"): 
        print(f"{i}: ", xor(decoded, i).decode("utf-8"))
        break

