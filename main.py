from Alice import Alice
import json
from Bob import Bob
from cryptography.fernet import Fernet
import copy

#this key will be used to encrypt and decrypt the circuit output
publicKey = Fernet.generate_key()

f = open('circuit.json')
circuit = json.load(f)


alice = Alice(publicKey)
bob = Bob(publicKey)

#generate the garbled circuit
garbled_circuit = alice.garbleCircuit(circuit)
if(garbled_circuit == None):
    print('An error has occured, check if the circuit.json has the correct values')

garbled_circuit_without_keys = copy.deepcopy(garbled_circuit)
for gate in garbled_circuit_without_keys:
    gate.pop('keys',None)

#send bob the garbled circuit
bob.getGarbledCircuit(garbled_circuit_without_keys)

#Generate inputs for the circuit
inputs = alice.generateInputs()
print('Inputs: ',inputs)
#send Bob the keys for the gates with input wires as both of their wires
keys = alice.getInputGateKeys(garbled_circuit,circuit['inputs'],inputs)
bob.getInputs(keys)

#decode circuit
decoded_circuit = bob.decodeCircuit(circuit['outputs'])

#send circuit outputs to alice
result = alice.decodeOutput(decoded_circuit)
print('Outputs: ',result)