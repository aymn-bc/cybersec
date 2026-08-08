from pwn import *

problem = "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"
decoded = bytes.fromhex(problem)
hint = "crypto{"
key = []
j = 0

while j < len(hint):
    for i in range(256):
        xored = xor(decoded, i)

        if xored[j] == ord(hint[j]):
            # print(f"{i}: {xored}")

            key.append(i)
            j += 1
            break
for i in range(256):
    xored = xor(decoded, i)
    if xored[-1] == ord("}"):
        key.append(i)
        break
print(key)

solution = ""
for i in range(len(decoded)):
    solution += chr(decoded[i] ^ key[i % len(key)])
print(solution)