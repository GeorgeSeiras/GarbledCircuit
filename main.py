from itertools import product
from Alice import Alice
import json
from Bob import Bob
from cryptography.fernet import Fernet

f = open('circuit.json')
circuit = json.load(f)


alice = Alice()
bob = Bob()

#generate the garbled circuit
garbled_circuit = alice.garbleCirtcuit(circuit)
if(garbled_circuit == None):
    print('An error has occured, check if the circuit.json has the correct values')

#send bob the garbled circuit
bob.getGarbledCircuit(garbled_circuit)

#Generate inputs for the circuit
inputs = alice.generateInputs()
#send Bob the keys for the gates with input wires as both of their wires
keys = alice.getInputGateKeys(garbled_circuit,circuit['inputs'],inputs)
bob.getInputs(keys)

decoded_circuit = bob.decodeCircuit()
print(decoded_circuit)