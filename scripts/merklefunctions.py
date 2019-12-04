import string
import hashlib
import merklelib
from merklelib import MerkleTree, beautify, utils
from string import ascii_lowercase
import sys

# Define custom hash function
# This needs to be be hashlib.sha1(str(value).encode()).hexdigest()
# if using in Keylime
def hashfunc(value):
	hash = hashlib.sha256(str(value).encode()).hexdigest()
	return hash

def proof_to_string(proof):
	hashlist, typelist = proof_to_lists(proof)
	hash_string = '%s' % ','.join(map(str, hashlist))
	type_string = '%s' % ','.join(map(str, typelist))
	proof_string = hash_string + ':' + type_string
	# Return value is string of node info delimited by :
	# Node info is delimited by ,
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

def string_to_proof(proof_string):
	hashstring, typestring = proof_string.split(":")
	hashlist = hashstring.split(",")
	typelist = typestring.split(",")
	proof = lists_to_proof(hashlist, typelist)
	return proof

def main():
	data = []
	tree = MerkleTree(data, hashfunc)
	for i in ascii_lowercase:
  		tree.append(i)

	beautify(tree)

	print("Original verify_leaf_inclusion")
	original_proof = tree.get_proof('a')
	print(tree.verify_leaf_inclusion('a', original_proof))

	print("Proof to lists/ Lists to proof verify_leaf_inclusion")
	root = tree._root
	proof_hashs, proof_types = proof_to_lists(original_proof)
	remade_proof = lists_to_proof(proof_hashs, proof_types)
	print(merklelib.verify_leaf_inclusion('a', remade_proof, hashfunc, utils.to_hex(root.hash)))

	print("Proof to string test")
	string_proof = proof_to_string(original_proof)
	print(type(string_proof) == type("hello"))

	print("Proof to string/ String to proof verify_leaf_inclusion")
	new_proof = string_to_proof(string_proof)
	print(merklelib.verify_leaf_inclusion('a', remade_proof, hashfunc, utils.to_hex(root.hash)))

if __name__ == '__main__':
  test = 'b'
  main()