import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse 

import mysql.connector

#Connecting to MySqL server for data(voters, candidattes and nodes)
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="MySQL@18",
  database="votingdata"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM users")

voters_list = mycursor.fetchall()

  
mycursor.execute("SELECT * FROM candidates")

candidates_list = mycursor.fetchall()

candidates =[]      #Candidates list
voters =[]           #Voters list
passwords ={}
for x in range(0,len(voters_list)):
    voters.append(voters_list[x][0])
    passwords[voters_list[x][0]]= voters_list[x][1]
    
for y in range(0,len(candidates_list)):
    candidates.append(candidates_list[y][0])


# Part 1 - Creating a Blockchain

class Blockchain:

    def __init__(self, voters, candidates):
        self.chain = []
        self.__id = tuple(voters)
        self.__idDone = []
        self.candidate = tuple(candidates)
        self.__countVote = {}
        self.VotingTrans = []
        self.create_block(proof=1, previous_hash='0')
        self.nodes = set()
        for i in range(len(self.candidate)):
            self.__countVote.update({self.candidate[i]: 0})
    
    #Create Block
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'VotingTrans': self.VotingTrans}
        self.VotingTrans = []
        self.chain.append(block)
        return block
    
    #Get Previous Block
    def get_previous_block(self):
        return self.chain[-1]

    #Get Proof of Work
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    #Calculate Hash Value
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    #Check If Chain is Valid
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
    
    
    #Add Transaction
    def add_transaction(self, voter, candidate):
        if voter in self.__id and candidate in self.candidate:
            if voter not in self.__idDone:
                self.VotingTrans.append(
                    {'voter': voter,
                     'candidate': candidate,
                     })
                self.__idDone.append(voter)
                self.__countVote[candidate]+=1
                # self.__countVote[candidate] = count

                previous_block = self.get_previous_block()
                return previous_block['index'] + 1
            else:
                return None
        else:
            return None

    #Add node
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
    
    #Replace chain (Consensus rule  )
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
    
    #Count individual votes and return result
    def getResult(self):
        return self.__countVote
    
    
# Part 2 - Mining the Blockchain

# Creating a Web App
app = Flask(__name__)

# Creating an address for the node on Port 5000
node_address = str(uuid4()).replace('-', '')

# Creating a Blockchain

blockchain = Blockchain(voters, candidates)


# Mining a new block

def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(voter=-1, candidate=-1)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'VotingTrans': block['VotingTrans']}
    return jsonify(response), 200


# Getting the full Blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200


# Checking if the Blockchain is valid
@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200


# Adding a new transaction to the Blockchain
@app.route('/caste_vote', methods=['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['voter', 'candidate']
    if not all(key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing', 400
    index = blockchain.add_transaction(json['voter'], json['candidate'])
    if index==None:
        return 'This is Vote has already been marked or is Invalid'
    # elif index==False:
    #     return 'This is a Fake Vote'
    else:
        if len(blockchain.VotingTrans)==5:
            mine_block()
        response = 'This was a successful vote'
        return response,200

         
# Part 3 - Decentralizing our Blockchain

# Connecting new nodes
@app.route('/connect_node', methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No node", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'All the nodes are now connected. The Hadcoin Blockchain now contains the following nodes:',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201


# Replacing the chain by the longest chain if needed
@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'The nodes had different chains so the chain was replaced by the longest one.',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'All good. The chain is the largest one.',
                    'actual_chain': blockchain.chain}
    return jsonify(response), 200


@app.route('/getResult', methods=['GET'])
def getResult():
    response =  blockchain.getResult()
    return jsonify(response)


# Running the app
app.run(host='0.0.0.0', port=5000)

