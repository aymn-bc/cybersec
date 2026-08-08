t_hash = ":Ulunfkuwmg_hzl{owiuwks_ohzhieo_k3bp}"
alphabet = [chr(x) for x in range(ord("A"), ord("Z")+1)]

for i in range(len(alphabet)):
    decrypted = ""
    for j in range(len(t_hash)):
        if (t_hash[j] in alphabet):
            decrypted += alphabet[(alphabet.index(t_hash[j]) + i) % len(alphabet)]
        else:
            decrypted += t_hash[j]
    print(f"Shift {i}: " + decrypted)
