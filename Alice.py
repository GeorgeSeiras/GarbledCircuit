from Yao import GarbleGate
import random
class Alice:

    def garbleCirtcuit(self,circuit):
        garbled_circuit = []
        yao = GarbleGate()
        for gate in circuit['gates']:
            garbled_gate = yao.run(garbled_circuit, circuit['inputs'], gate)
            if(garbled_gate == None):
                return None
            garbled_circuit.append(garbled_gate)
        return garbled_circuit

    def generateInputs(self):
        return [random.randint(0,1), random.randint(0,1)]

    def getInputGateKeys(self,circuit,inputs):
        inputGateKeys = []
        for gate in circuit:
            keys = []
            if(gate['type'] == 'input'):
                if(inputs[0] == 0):
                    keys.append(gate['keys'][0])
                else:
                    keys.append(gate['keys'][1])
                if(inputs[1] == 0):
                    keys.append(gate['keys'][2])
                else:
                    keys.append(gate['keys'][3])
            inputGateKeys.append({'id':gate['id'],'keys':keys})
        return inputGateKeys
