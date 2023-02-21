""" Script to verify that a coin is properly formatted, according to the specification of homework 1's writeup.

To run, supply your coin.txt file and your watermark (as a bit string) as the first and second command line parameters, respectively.

Example: python3 hw1_p1_verify_coin.py coin.txt 100001100111
"""


import sys
import hashlib
import random
import string
from random import randbytes




k = 4
n = 28
watermark_length = 4

def verify_coin(coin_txt, watermark_hex):
    if len(watermark_hex) != watermark_length:
        return False
    d = None
    with open(coin_txt) as f:
        for i, c_i in enumerate(f):
            c_i_hash = bin(int(hashlib.sha256(bytes.fromhex(c_i)).hexdigest(), base=16)).lstrip('0b').zfill(256)[:n]
            print( c_i_hash) 
            if i == 0:
                d = c_i_hash
            if c_i[:watermark_length] != watermark_hex or c_i_hash != d:
                return False
    
    return False if i+1 != k else True

def find_watermark_and_coins():
    # ***** CODE to find watermark for given NID, find the coin preimages etc  ****
    nid = "st786"
    watermark = bin(int(hashlib.sha256(nid.encode()).hexdigest(), base=16)).lstrip('0b').zfill(256)[:16]
    print("watermark:", watermark)


    leading_bits = hex(int(watermark, 2)).lstrip('0x')
    print("leading bits:", leading_bits)

    coin_i = bytearray(bytes.fromhex(leading_bits))
    keep_going = True
    coin_dict = dict()

    while keep_going:
        coin_i.extend(randbytes(6))
    
        c_i_hash = bin(int(hashlib.sha256(bytes.fromhex(coin_i.hex())).hexdigest(), base=16)).lstrip('0b').zfill(256)[:n]
    
        if c_i_hash in coin_dict.keys():
            coin_dict[c_i_hash].append(coin_i.hex()[:16])
            if len(coin_dict[c_i_hash]) == 4:
                print("hash:", c_i_hash)
                print("coin vals:", coin_dict[c_i_hash])
                keep_going = False
        else:
            coin_dict[c_i_hash] = [coin_i.hex()[:16]]
        coin_i = bytearray(bytes.fromhex(leading_bits))
    
    # ***** CODE to find watermark for given NID, find the coin preimages etc  ****

def forging_watermark():
    og_nid = "st786"
    og_watermark = bin(int(hashlib.sha256(og_nid.encode()).hexdigest(), base=16)).lstrip('0b').zfill(256)[:16]
    keep_going = True

    forged_nid = ""
    while keep_going:
        for i in range(2):
            forged_nid+=random.choice(string.ascii_lowercase)

        for i in range(4):
            forged_nid+=str(random.randint(0,9))

        forged_watermark = bin(int(hashlib.sha256(forged_nid.encode()).hexdigest(), base=16)).lstrip('0b').zfill(256)[:16]



        if forged_watermark == og_watermark:
            print("forged_nid:", forged_nid)
            print("forged_nid's watermark:", forged_watermark)
            f = open("forged-watermark.txt", "w")
            f.write(forged_nid)
            f.close()
            keep_going = False
        else:
            forged_nid = ""
        

    
    

if __name__ == "__main__":

    forging_watermark()

    coin_txt, watermark = sys.argv[1:]
    watermark_hex = hex(int(watermark, 2)).lstrip('0x')
    if verify_coin(coin_txt, watermark_hex):
        print("Your coin is valid!")
    else:
        print("Your coin is not valid!")
