from pwn import xor
import string

encrypted_flag = bytes.fromhex("1d037d3c32782a5c29360c334406363d7f532c2108254274232507492f173b3f4977373b337f353f")
key_start = xor(b"THM{", encrypted_flag[:4])
for i in string.ascii_letters + string.digits:
	key = key_start + i.encode()
	print(f"{key} : {xor(encrypted_flag, key)}")
