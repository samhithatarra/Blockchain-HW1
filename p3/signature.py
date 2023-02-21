import string
import random
import hashlib
from math import floor


# return the hash of a string
def SHA(s: string) -> string:
    return hashlib.sha256(s.encode()).hexdigest()

# transfer a hex string to integer
def toDigit(s: string) -> int:
    return int(s, 16)

# generate 2^d (si^{-1}, si) pairs based on seed r
def KeyPairGen(d: int, r: int) -> dict:
    pairs = {}
    random.seed(r)
    for i in range(1 << d):
        cur = random.randbytes(32).hex()
        while cur in pairs:
            cur = random.randbytes(32).hex()
        pairs[cur] = SHA(cur)
    return pairs


class MTSignature:
    def __init__(self, d, k):
        self.d = d
        self.k = k
        self.treenodes = [None] * (d+1)
        for i in range(d+1):
            self.treenodes[i] = [None] * (1 << i)
        self.sk = [None] * (1 << d)
        self.pk = None # same as self.treenodes[0][0]


    # Populate the fields self.treenodes, self.sk and self.pk. Returns self.pk.
    def KeyGen(self, seed: int) -> string:
        pairs = KeyPairGen(self.d,seed)
        i = 0
        self.sk = list(pairs.keys())


        for k, v in pairs.items():
            self.treenodes[-1][i] = v
            i+=1


        tree_i = -1
        bottom_row = self.treenodes[tree_i]

    
        while len(bottom_row) != 1:
            tree_i-=1
            row_above = []
			# getting the pairs
            index = 0
            for i in range(0,len(bottom_row)-1,2):
                hash_concat = SHA(format(index, "b").zfill(256) + bottom_row[i] + bottom_row[i+1])
                row_above.append(hash_concat)
                index+=1
            self.treenodes[tree_i] = row_above
            bottom_row = row_above

        self.pk = self.treenodes[0][0]
        return self.pk
        

    # Returns the path SPj for the index j
    # The order in SPj follows from the leaf to the root.
    def Path(self, j: int) -> string:
        proof = []
        curr_index = j
        self.treenodes.reverse()
        for row in self.treenodes:
            if len(row) > 1:
                if curr_index % 2 == 0:
                    proof.append(row[curr_index+1])
                    curr_index = floor((curr_index+1)/2)
                else:
                    proof.append(row[curr_index-1])
                    curr_index = floor((curr_index-1)/2)

        
        self.treenodes.reverse()            
        return "".join(proof)

    # Returns the signature. The format of the signature is as follows: ([sigma], [SP]).
    # The first is a sequence of sigma values and the second is a list of sibling paths.
    # Each sibling path is in turn a d-length list of tree node values. 
    # All values are 64 bytes. Final signature is a single string obtained by concatentating all values.
    def Sign(self, msg: string) -> string:
        zj = []
        for j in range(1,self.k+1):
            zj.append(toDigit(SHA(format(j, "b").zfill(256)+msg))%(2**self.d))

        sigmas = []
        paths = []
        for z in zj:
            sigmas.append(self.sk[z])
            paths.append(self.Path(z))

        return "".join(sigmas+paths)

        

# Problem 3.2 Signature forgery below
# Completed extra credit as well as both messages are grammatically correct english sentences

m = MTSignature(10,2)
m.KeyGen(2023)
original_sig = m.Sign("My name is Samhitha Tarra and I am having a good day.")

not_found = True
chicken_count = 0
while not_found:
    chicken_count+=1
    forged_sig = m.Sign("Samhitha Tarra has " + str(chicken_count)+ " pet chickens.")
    if original_sig == forged_sig:
        not_found = False
        f = open("forgery.txt", "w")
        f.write("My name is Samhitha Tarra and I am having a good day.\n")
        f.write("Samhitha Tarra has " + str(chicken_count)+ " pet chickens.")
        f.close()
        
        

