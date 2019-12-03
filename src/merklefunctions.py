import string
import hashlib
import merklelib
from merklelib import MerkleTree, beautify, utils
from string import ascii_lowercase
import sys

# Define custom hash function
# May just need "return value" in our implementation
def hashfunc(value):
	new_value = value
	return new_value

def proof_to_string(proof):
	proof_list = []
	nodes = proof.hex_nodes
	for node in nodes:
	    new_data = bytes.fromhex(node).decode('utf-8')
	    proof_list.append(new_data)
	proof_string = '%s' % ','.join(map(str, proof_list))
	# Return value is string of nodes delimited by commas
	return proof_string

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
	data = []
	tree = MerkleTree(data, hashfunc)
	for i in ascii_lowercase:
  		tree.append(i)
	beautify(tree)
	original_proof = tree.get_proof('a')
	print(tree.verify_leaf_inclusion('a', original_proof))

	root = tree._root
	proof_hashs, proof_types = proof_to_lists(original_proof)
	remade_proof = lists_to_proof(proof_hashs, proof_types)
	print(merklelib.verify_leaf_inclusion('a', remade_proof, hashfunc, utils.to_hex(root.hash)))

	string_proof = proof_to_string(original_proof)
	print("String Proof: " + string_proof)

if __name__ == '__main__':
  test = 'b'
  main()
