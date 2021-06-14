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
