from cryptography.fernet import Fernet
class Bob:

    def __init__(self):
        self.output = {}

    def getInputs(self, keys):
        self.keys = keys
        
    def getGarbledCircuit(self, circuit):
        self.circuit = circuit

    #decodes the circuit gate by gate, logging the output of every gate it decodes
    #returns only the outputs of the gates that are marked as outputs of the circuit
    def decodeCircuit(self,outputs):
        self.decoded_circuit = []
        for gate in self.circuit:
            found = self.decodeGate(gate)
            if(found == b'0'):
                self.decoded_circuit.append({'id':gate['id'],'output':gate['outputs'][0]})
            elif(found == b'1'):
                self.decoded_circuit.append({'id':gate['id'],'output':gate['outputs'][1]})
        decodedOutputs = {}
        for gate in self.decoded_circuit:
            if(gate['id'] in outputs):
                decodedOutputs.update({gate['id']:gate['output']})
        return decodedOutputs

    def decodeGate(self, gate):
        keys = []
        #if the wire is an input wire find its corresponding key
        foundKey1 = self.keys.get(gate['inputs'][0])
        if(foundKey1 is not None):
            keys.append(foundKey1)
        #else find the output key of the corresponding gate
        else:
            keys.append(self.output.get(gate['inputs'][0]))
        foundKey2 = self.keys.get(gate['inputs'][1])
        if(foundKey2 is not None):
            keys.append(foundKey2)
        else:
            keys.append(self.output.get(gate['inputs'][1]))
        return self.decodeCyphertext(gate,keys)

    #decodes the appropriate cyphertext of the gate and logs the output of the gate in self.output
    def decodeCyphertext(self,gate,keys):
        for cyphertext in gate['cyphertext']:
            try:
                res = Fernet(keys[0]).decrypt(Fernet(keys[1]).decrypt(cyphertext))
                if(res == b'0'):
                    self.output.update({gate['id']:gate['outputs'][0]})
                    return res
                elif(res == b'1'):
                    self.output.update({gate['id']:gate['outputs'][1]})
                    return res
            except:
                pass