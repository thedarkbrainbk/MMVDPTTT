import hashlib
import time
import json
import os
import platform

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

def create_genesis_block():
    return Block(0, "0", time.time(), "Genesis Block", calculate_hash(0, "0", time.time(), "Genesis Block"))

def calculate_hash(index, previous_hash, timestamp, data):
    block_data = str(index) + previous_hash + str(timestamp) + data
    return hashlib.sha256(block_data.encode('utf-8')).hexdigest()

def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = time.time()
    hash = calculate_hash(index, previous_block.hash, timestamp, data)
    return Block(index, previous_block.hash, timestamp, data, hash)

def save_blockchain_to_file(blockchain, file_name):
    with open(file_name, 'w') as f:
        f.write(json.dumps([block.__dict__ for block in blockchain], indent=4))

def load_blockchain_from_file(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            loaded_blocks = json.loads(f.read())
            return [Block(block['index'], block['previous_hash'], block['timestamp'], block['data'], block['hash']) for block in loaded_blocks]
    else:
        return [create_genesis_block()]

def start_blockchain_loop(blockchain, block_creation_interval):
    previous_block = blockchain[-1]

    while True:
        time.sleep(block_creation_interval)
        block_to_add = create_new_block(previous_block, f"Block {previous_block.index + 1}")
        blockchain.append(block_to_add)
        previous_block = block_to_add
        print(f"Block {block_to_add.index} added to the blockchain!")
        print(f"Hash: {block_to_add.hash}\n")
        save_blockchain_to_file(blockchain, "blockchain.txt")

# Load or initialize the blockchain
blockchain = load_blockchain_from_file("blockchain.txt")

print("Press any key to start the node...")

if platform.system() == "Windows":
    os.system('pause >nul')
else:
    # Wait for the user to input any value and press enter
    input()

print("Node started. Creating blocks every 10 seconds...\n")
start_blockchain_loop(blockchain, 10)
