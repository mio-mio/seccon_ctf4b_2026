from Crypto.Cipher import ARC4, AES
from Crypto.Util.Padding import unpad

# key = b"THISISNOTAESKEY!ImashyKey!Dontlookme!!!"
data = open("flag.txt.hacked", "rb").read()
#cipher = ARC4.new(key)
#plain = cipher.decrypt(data)

aes_key = b"THISISNOTAESKEY!"

rc4_keys = [
    b"ImashyKey!Dontlookme!!!",
    b"ImashyKey!Dontlookme!!!\x00",
    b"ImashyKey!",
    b"ImashyKey!\x00"
]

for rc4_key in rc4_keys:
    print("RC4 key: ", rc4_key)
    print("keylen : ", len(rc4_key))
    
    print("case1")
    try:
        mid = AES.new(aes_key, AES.MODE_ECB).decrypt(data)
        for candidate in [mid, unpad(mid, 16)]:
            plain = ARC4.new(rc4.key).decrypt(candidate)
            print("AES->RC4 : ", plain[:200])
    except Exception as e:
          pass
    
    print("case2")

    # Case 2: encrypt = AES then RC4, so decrypt = RC4 then AES
    try:
        mid = ARC4.new(rc4_key).decrypt(data)
        plain = AES.new(aes_key, AES.MODE_ECB).decrypt(mid)

        print("RC4 -> AES raw:", plain)
        print("RC4 -> AES decoded:", plain.decode(errors="replace"))

        # paddingを外せるなら外す
        try:
            plain_unpadded = unpad(plain, 16)
            print("RC4 -> AES unpadded:", plain_unpadded)
            print("RC4 -> AES unpadded decoded:", plain_unpadded.decode(errors="replace"))

            # 中身がHEX文字列ならさらに復号
            try:
                flag = bytes.fromhex(plain_unpadded.decode().strip())
                print("HEX decoded flag:", flag)
                print("HEX decoded flag decoded:", flag.decode(errors="replace"))
            except Exception:
                print("Not valid hex after unpad")

        except Exception:
            # unpadできない場合、plainそのものがHEX文字列か試す
            try:
                flag = bytes.fromhex(plain.decode().strip())
                print("HEX decoded flag:", flag)
                print("HEX decoded flag decoded:", flag.decode(errors="replace"))
            except Exception:
                print("Not valid hex without unpad")

    except Exception as e:
        print("Case 2 failed:", e)