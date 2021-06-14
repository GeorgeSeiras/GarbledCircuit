import pandas as pd
from itertools import product
from Alice import Alice
import json
from Bob import Bob
f = open('circuit.json')
circuit = json.load(f)


alice = Alice()
bob = Bob()

#generate the garbled circuit
garbled_circuit = alice.garbleCirtcuit(circuit)
if(garbled_circuit == None):
    print('An error has occured, check if the circuit.json has the correct values')

print(garbled_circuit[0])
#send bob the garbled circuit
bob.getGarbledCircuit(garbled_circuit)

#Generate inputs for the circuit
inputs = alice.generateInputs()

#send Bob the inputs
bob.getInputs(inputs)