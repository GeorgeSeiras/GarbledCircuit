from cryptography.fernet import Fernet
class Bob:
    def getInputs(self, keys):
        self.keys = keys
        
    def getGarbledCircuit(self, circuit):
        self.circuit = circuit

    def decodeCircuit(self):
        self.decoded_circuit = []
        for gate in self.circuit:
            found = self.decodeGate(gate)
            if(found == b'0'):
                self.decoded_circuit.append({'id':gate['id'],'output':gate['outputs'][0]})
            elif(found == b'1'):
                self.decoded_circuit.append({'id':gate['id'],'output':gate['outputs'][1]})
        return self.decoded_circuit

    def decodeGate(self, gate):
        #if the gate's wires are both input wires search for the appropriate keys and decode them
        if(gate['type'] == 'input'):
            for entry in self.keys:
                if(gate['id'] == entry['id']):
                    return self.decodeCyphertext(gate,entry['keys'])
        #if not check if one of the 2 wires is an input wire
        # keys = []
        # for entry in self.keys:
        #     if(gate['input'][0] == entry['id']):
        #         keys[0] = entry[]
            
                    
    def decodeCyphertext(self,gate,keys):
        for cyphertext in gate['cyphertext']:
            try:
                return Fernet(keys[0]).decrypt(Fernet(keys[1]).decrypt(cyphertext))
            except:
                pass