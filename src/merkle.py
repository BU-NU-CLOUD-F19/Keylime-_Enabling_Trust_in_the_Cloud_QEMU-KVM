import string
import hashlib

from merklelib import MerkleTree, beautify
from string import ascii_lowercase

# Define custom hash function
# May just need "return value" in our implementation
def hashfunc(value):
  # Convert to string because it doesn't like bytes
  new_value = str(value)
  hash = hashlib.sha256(new_value.encode('utf-8')).hexdigest()
  return hash

# Instantiate empty list
data = []

# Instantiate empty Merkle tree
tree = MerkleTree(data, hashfunc)

# Add all ASCII characters to Merkle tree
for i in ascii_lowercase:
  tree.append(i.encode('utf-8'))

# Print MerkleTree
print("\n")
beautify(tree)

# Generate an audit proof the letter a
print("\n")
print("Generating audit proof for a")
print("Hash of a is : " + hashlib.sha256("a".encode('utf-8')).hexdigest())
proof = tree.get_proof('a')
print("Proof: ")
print(proof)
print()

# Verify that a is in the tree
if tree.verify_leaf_inclusion('a', proof):
  print('a is in the tree')
  print()
else:
  exit('a is not in the tree')

# Add in string hash to test
new_hash = "rgie3948guhiev"
tree.append(new_hash)

# Generate an audit proof for the string
print("Generating audit proof for rgie3948guhiev")
proof = tree.get_proof('rgie3948guhiev')
print("Proof: ")
print(proof)
print()

# Verify that rgie3948guhiev is in the tree
if tree.verify_leaf_inclusion('rgie3948guhiev', proof):
  print('rgie3948guhiev is in the tree')
  print()
else:
  exit('rgie3948guhiev is not in the tree')

# Generate an audit proof for random string
print("Generating audit proof for DONTFINDME")
proof = tree.get_proof('DONTFINDME')
print("Proof: ")
print(proof)
print()

# Verify that DONTFINDME is not in the tree
if tree.verify_leaf_inclusion('DONTFINDME', proof):
  print('DONTFINDME is in the tree')
  print()
else:
  exit('DONTFINDME is not in the tree')
