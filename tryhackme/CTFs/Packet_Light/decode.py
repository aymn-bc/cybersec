import base64

key="H0t3lSt@ff0NlyK3epS3cr3t!"
encoded_characters=[ 
    "HA==", "AA==", "BQ==", "Mw==", "Hg==", "ew==", "Og==", "fA==", "Fw==", "eQ==", "Ow==", "Fw==", "Pw==", "fA==", "PA==", "Kw==", "IA==", "eQ==", "Jg==", "Lw==", "Fw==", "eA==", "Pg==", "LQ==", "Gg==", "Fw==", "MQ==", "eA==", "PQ==", "NQ=="
]

def xor(data: bytes, key: bytes) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

for char in encoded_characters:
    decoded_char = base64.b64decode(char)
    print(xor(decoded_char, key.encode()).decode("utf-8"), end="")
print("\n")