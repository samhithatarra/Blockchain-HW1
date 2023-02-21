from math import floor
from typing import Optional, List
from hashlib import sha256

def verify(obj: str, proof: str, commitment: str) -> bool:
		proof_splitted = proof.split(" ")
		order = proof_splitted[::2]
		proofs = proof_splitted[1::2]
		hashed_obj = sha256(obj.encode()).hexdigest()
		
		
		for i, p in enumerate(proofs):
			if order[i] == "first":
				concat = p + hashed_obj
			else:
				concat = hashed_obj + p
			hashed_obj = sha256(concat.encode()).hexdigest()
		
		return hashed_obj == commitment


# got from stack overflow
def power_of_two(target):
    if target > 1:
        for i in range(1, int(target)):
            if (2 ** i >= target):
                return 2 ** i
    else:
        return 1

class Prover:
	def __init__(self):
		self.tree = []
		self.objectlst = []

		
	
	# Build a merkle tree and return the commitment
	def build_merkle_tree(self, objects: List[str]) -> str:

		self.objectlst = objects.copy()
		
		for i in range(power_of_two(len(objects))-len(objects)):
			objects.append("None")

		leaf_row = []
		for val in objects:
			leaf_row.append(sha256(val.encode()).hexdigest())
		self.tree.append(leaf_row)

		bottom_row = leaf_row

		while len(bottom_row) != 1:
			row_above = []
			# getting the pairs
			for i in range(0,len(bottom_row)-1,2):
				concat = bottom_row[i] + bottom_row[i+1]
				hash_concat = sha256(concat.encode()).hexdigest()
				row_above.append(hash_concat)
			self.tree.append(row_above)
			bottom_row = row_above


		return self.tree[-1][0]
			


	def get_leaf(self, index: int) -> Optional[str]:
		if index > len(self.objectlst)-1:
			return None
		else:
			return self.tree[0][index]


	def generate_proof(self, index: int) -> Optional[str]:

		if index > len(self.objectlst)-1:
			return None
		proof = []
		curr_index = index
		
		for row in self.tree:
			if len(row) > 1:
				if curr_index % 2 == 0:
					proof.append("second")
					proof.append(row[curr_index+1])
					

					curr_index = floor((curr_index+1)/2)
					
				else:
					proof.append("first")
					proof.append(row[curr_index-1])
					curr_index = floor((curr_index-1)/2)

		return " ".join(proof)





p = Prover()
p.build_merkle_tree(["a","b","c","d","e"])
p.get_leaf(5)
p.generate_proof(1)
verify("c", p.generate_proof(2), p.build_merkle_tree(["a","b","c","d","e"]))
# p.build_merkle_tree(["jpm","debt","stupid","hi", "bye"])