# Isolated testing script for Merkle Tree functions
# Functionality is tested here before being integrated with
# the Keylime Provider Verifier
import string
import hashlib
import json
import io

from merklelib import MerkleTree, beautify, export
from string import ascii_lowercase

# Define custom hash function
def hashfunc(value):
  new_value = value
  return new_value

# --------------- LEAF APPEND / TREE GENERATE TEST -------------------- #
print("\n--------------- LEAF APPEND / TREE GENERATE TEST --------------------")
# This test simulates accumulating nonces one at a time
# Instantiate empty list
data = []

# Instantiate empty Merkle tree for appending
asciiTree = MerkleTree(data, hashfunc)

# Add all ASCII characters to Merkle tree
for i in ascii_lowercase:
  asciiTree.append(i.encode('utf-8'))

# Print MerkleTree
print("\nPrinting Merkle Tree")
beautify(asciiTree)
print("\nPrinting root")
print(asciiTree.merkle_root)
print("\nPrinting leaves")
print(asciiTree.leaves)

# Generate an audit proof the letter a
print("\nGenerating audit proof for a")
proof = asciiTree.get_proof('a')
print("\nProof: ")
print(proof)

# Verify that a is in the tree
if asciiTree.verify_leaf_inclusion('a', proof):
  print('\na is in the tree')
else:
  exit('a is not in the tree')

# Add in longer string hash to test
new_hash = "rgie3948guhiev"
asciiTree.append(new_hash)

# Generate an audit proof for the string
print("\nGenerating audit proof for rgie3948guhiev")
proof = asciiTree.get_proof('rgie3948guhiev')
print("\nProof: ")
print(proof)

# Verify that rgie3948guhiev is in the tree
if asciiTree.verify_leaf_inclusion('rgie3948guhiev', proof):
  print('\nrgie3948guhiev is in the tree')
else:
  exit('rgie3948guhiev is not in the tree')

# Generate an audit proof for random string NOT in the tree
print("\nGenerating audit proof for DONTFINDME")
proof = asciiTree.get_proof('DONTFINDME')
print("\nProof: ")
print(proof)

# Verify that DONTFINDME is not in the tree
if asciiTree.verify_leaf_inclusion('DONTFINDME', proof):
  exit('\nDONTFINDME is in the tree')
else:
  print('\nDONTFINDME is not in the tree')

print("\n--------------- LEAF APPEND / TREE GENERATE TEST END --------------------")
# --------------- LEAF APPEND / TREE GENERATE TEST END -------------------- #


# --------------- GENERATE FROM LIST TEST -------------------- #
print("\n--------------- GENERATE FROM LIST TEST --------------------")
# This test simulates accumulating nonces in a single list
# Instantiate empty list
data = []

# Initialize testing list
newData = ["aoibune", "24pot309grtjb", "poegijshbn", "oqfh8vyu", "0298f7gvublnk", "pq09483f7guvbl"]

# Instantiate empty Merkle tree for appending
listTree = MerkleTree(data, hashfunc)

# Add list data to merkle tree
listTree.extend(newData);

# Print MerkleTree
print("\nPrinting Merkle Tree")
beautify(listTree)
print("\nPrinting root")
print(listTree.merkle_root)
print("\nPrinting leaves")
print(listTree.leaves)

# Generate an audit proof for the string
print("\nGenerating audit proof for poegijshbn")
proof = listTree.get_proof('poegijshbn')
print("\nProof: ")
print(proof)

# Verify that rgie3948guhiev is in the tree
if listTree.verify_leaf_inclusion('poegijshbn', proof):
  print('\npoegijshbn is in the tree')
else:
  exit('poegijshbn is not in the tree')

# Generate an audit proof for random string NOT in the tree
print("\nGenerating audit proof for DONTFINDME")
proof = listTree.get_proof('DONTFINDME')
print("\nProof: ")
print(proof)

# Verify that DONTFINDME is not in the tree
if listTree.verify_leaf_inclusion('DONTFINDME', proof):
  exit('\nDONTFINDME is in the tree')
else:
  print('\nDONTFINDME is not in the tree')

print("\n--------------- GENERATE FROM LIST TEST END --------------------")
# --------------- GENERATE FROM LIST TEST END -------------------- #

# --------------- EXPORT TREE TEST -------------------- #
# Jsonify and json.dumps fail because the object MerkleTree is not serializable

# This doesn't work currently
# NameError: name 'io' is not defined
export(asciiTree, filename='ascii', ext='json')

# --------------- EXPORT TREE TEST END -------------------- #
