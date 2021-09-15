
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
