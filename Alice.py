from Yao import GarbleGate
import random
from cryptography.fernet import Fernet
class Alice:

    def __init__(self,publicKey):
        self.fernet = Fernet(publicKey)

    def decodeOutput(self,decodedCircuit):
        decodedOutput = {}
        for key,value in decodedCircuit.items():
            # print(self.fernet.decrypt(value))
            decodedOutput.update({key:self.fernet.decrypt(value)})
        return decodedOutput

    #given a circuit, creates and returnes its garbled version
    def garbleCircuit(self,circuit):
        garbled_circuit = []
        yao = GarbleGate()
        for gate in circuit['gates']:
            garbled_gate = yao.run(garbled_circuit, gate)
            if(garbled_gate == None):
                return None
            garbled_circuit.append(garbled_gate)
        return garbled_circuit

    def generateInputs(self):
        return [random.randint(0,1), random.randint(0,1)]

    #create a dictionary with the key that corresponds to each input wire of the circuit
    def getInputGateKeys(self,circuit,inputWires,inputs):
        inputWireKeys = {}
        for wire in inputWires:
            for gate in circuit:
                if wire in gate['inputs']:
                    index = gate['inputs'].index(wire)
                    if(index == 0):
                        if(inputs[wire] == 0):
                            inputWireKeys.update({wire:gate['keys'][0]})
                        elif(inputs[wire] == 1):
                            inputWireKeys.update({wire:gate['keys'][1]})
                    elif(index == 1):
                        if(inputs[wire] == 0):
                            inputWireKeys.update({wire:gate['keys'][2]})
                        elif(inputs[wire] == 1):
                            inputWireKeys.update({wire:gate['keys'][3]})
                    break
        return inputWireKeys

