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
        # print(self.keys)
        #if the gate's wires are both input wires search for the appropriate keys and decode them
        # if(gate['type'] == 'input'):
        #     keys = []
        #     for key in gate['keys']:
        #         print(key)
        #     print('+')
        #     print(gate['inputs'])
        #     print(self.keys.get(gate['inputs'][0]))
        #     print(self.keys.get(gate['inputs'][1]))
        #     keys.append(self.keys.get(gate['inputs'][0]))
        #     keys.append(self.keys.get(gate['inputs'][1]))
        #     print('---------------------------------------------------')
        #     return self.decodeCyphertext(gate,keys)
        # #if not check if one of the 2 wires is an input wire
        # keys = []
        # for entry in self.keys:
        #     found = entry.get(gate['inputs'][0])
        #     # print(found)
        #     if(gate['inputs'][0] == entry['id']):
        #         # print(entry['outputs'])
                 pass      
        
    def decodeCyphertext(self,gate,keys):
        for cyphertext in gate['cyphertext']:
            try:
                return Fernet(keys[0]).decrypt(Fernet(keys[1]).decrypt(cyphertext))
            except:
                pass