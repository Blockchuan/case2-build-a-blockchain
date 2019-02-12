# case2-build-a-blockchain
How to build a bitcoin blockchain from nothing .

step 0:preparing the software  
step 1:build up a blockchain


step 0:preparing the software
---------------------------------
1.python 3.6+ (we install ancaconda3 for python 3.6),and then add the \Ancaconda\Scripts into the path, which is in the My-computer.  
2.install Flask and Request  
3.install serves which supporting HTTP

step 1:build up a blockchain
---------------------------------
1.build up a class  
2.about block and new_transaction  
3.about PoW  

step 2: Blockchain as an API
---------------------------------
We use the python Flask framework, which is a light web application framework. It can reflect the web request into python function. 

And the blockchain can run in the flask web.  

we will build up three applications:  
/transactions/new   create a transaction into block  
/mine               tell the sever to mine new block  
/chain              return the whole blockchain  

1.build up nodes  
2.send transactions  
3.mine  


step3: run blockchian
---------------------------------
use postman to send the mine/transaction/chain-request


step4: consensus
---------------------------------
before doing the consensus algorithm, we need to make a node know the other nodes. So every node should keep a record including the other nodes in the network.

so we add several APIs.
/nodes/register receive the new node list in URL
/nodes/resolve run consistent algorithm, solve the conflict, ensure node own the right chain.

consensus algorithm.




