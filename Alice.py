from Yao import GarbleGate
import random
class Alice:

    #given a circuit, creates and returnes its garbled version
    def garbleCirtcuit(self,circuit):
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
                        if(inputs[index] == 0):
                          inputWireKeys.update({wire:gate['keys'][0]})
                        elif(inputs[index] == 1):
                         inputWireKeys.update({wire:gate['keys'][1]})
                    elif(index == 1):
                        if(inputs[index] == 0):
                          inputWireKeys.update({wire:gate['keys'][2]})
                        elif(inputs[index] == 1):
                         inputWireKeys.update({wire:gate['keys'][3]})
        return inputWireKeys
