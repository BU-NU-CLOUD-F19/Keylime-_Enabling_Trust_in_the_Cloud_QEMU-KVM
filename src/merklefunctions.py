import string
import hashlib
import merklelib
from merklelib import MerkleTree, beautify, utils
from string import ascii_lowercase
import sys

# Define custom hash function
# May just need "return value" in our implementation
def hashfunc(value):
	# Convert to string because it doesn't like bytes
	new_value = str(value)
	hash = hashlib.sha256(new_value).hexdigest()
	return hash

def proof_to_lists(proof):
	hashlist = []
	typelist = []
	for node in proof._nodes:
		hashlist.append(utils.to_hex(node.hash))
		typelist.append(node.type)
	return hashlist, typelist

def lists_to_proof(hashlist, typelist):
	nodepath = []
	for nodehash, nodetype in zip(hashlist, typelist):
		nodepath.append(merklelib.AuditNode(utils.from_hex(nodehash), nodetype))
	proof = merklelib.AuditProof(nodepath)
	return proof

def main():
	reload(sys)  
	sys.setdefaultencoding('utf-8')

	print(sys.getdefaultencoding())

	data = []
	tree = MerkleTree(data, hashfunc)
	for i in ascii_lowercase:
  		tree.append(i)
  	original_proof = tree.get_proof('a')
  	print(tree.verify_leaf_inclusion('a', original_proof))

  	root = tree._root

  	proof_hashs, proof_types = proof_to_lists(original_proof)
  	remade_proof = lists_to_proof(proof_hashs, proof_types)
  	print(merklelib.verify_leaf_inclusion('a', remade_proof, hashfunc, utils.to_hex(root.hash)))

if __name__ == '__main__':
	test = 'b'
	main()

