# -*- coding: utf-8 -*-
"""
Spyder Editor

build up a blockchain
1.build up a class.
Blockchain 类负责管理链式数据，它会存储交易并且还有添加新的区块到链式数据的Method。
2.about block and new_transaction
3.about PoW


"""

import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request

#这个blockchain类负责管理链式数据，
#它会存储交易，并且还有添加新的区块到链式数据的methods

class Blockchain(object): 
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        
        # 创建创世区块
        self.new_block(previous_hash=1, proof=100)


    def new_block(self, proof, previous_hash=None):
        # Creates a new Block and adds it to the chain
        """
        创建一个新的区块到区块链中
        :param proof: <int> 由工作证明算法生成的证明
        :param previous_hash: (Optional) <str> 前一个区块的 hash 值
        :return: <dict> 新区块
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # 重置当前交易记录
        self.current_transactions = []

        self.chain.append(block)
        return block

   
   
    def new_transaction(self, sender, recipient, amount):
        # Adds a new transaction to the list of transactions
            """
            Creates a new transaction to go into the next mined Block
            :param sender: <str> Address of the Sender
            :param recipient: <str> Address of the Recipient
            :param amount: <int> Amount
            :return: <int> The index of the Block that will hold this transaction
            """
    
            self.current_transactions.append({
                'sender': sender,
                'recipient': recipient,
                'amount': amount,
            })
    
            return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]
    
    @staticmethod
    def hash(block):
        """
        给一个区块生成 SHA-256 值
        :param block: <dict> Block
        :return: <str>
        """

        # 我们必须确保这个字典（区块）是经过排序的，否则我们将会得到不一致的散列
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


    def proof_of_work(self, last_proof):
            """
            Simple Proof of Work Algorithm:
             - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
             - p is the previous proof, and p' is the new proof
            :param last_proof: <int>
            :return: <int>
            """
    
            proof_factor = 0 #This is the random number
            while self.valid_proof(last_proof, proof_factor) is False:
                proof_factor += 1
    
            return proof_factor
    
    @staticmethod
    def valid_proof(last_proof, proof_factor):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """

        guess = f'{last_proof}{proof_factor}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


##########################################################################
#build up nodes

# Instantiate our Node(实例化节点)
app = Flask(__name__)

# Generate a globally unique address for this node(为节点创建一个随机名称)
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain(实例化blockchain类)
blockchain = Blockchain()

#创建/mine接口，GET方式请求
@app.route('/mine', methods=['GET'])
def mine():
     # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

#创建 /transactions/new 接口，POST 方式请求，可以给接口发送交易数据。
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

#创建 /chain 接口，返回整个区块链。
@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

#服务器运行端口 5000 。
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



