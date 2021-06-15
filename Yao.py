from cryptography.fernet import Fernet


class GarbleGate:

    def __init__(self):
        self.keys = [],
        self.cyphertext = []
        self.outputs = [],
        self.wires = {}

    def getWires(self):
        return self.wires
    
    def run(self, garbledCircuit, gate):
        self.garble(gate, garbledCircuit)
        return {
            'id': gate['id'],
            'keys': self.keys,
            'cyphertext': self.cyphertext,
            'outputs': self.outputs,
            'inputs':gate['input']
        }

    def generateKey(self):
        return Fernet.generate_key()

    # Finds and returns the key pair of a wire that is the output of a gate
    def getKeyFromGateOutput(self, garbled_circuit, wire_id):
        keys = []
        for garbled_gate in garbled_circuit:
            if(garbled_gate['id'] == wire_id):
                keys.append(garbled_gate['outputs'][0])  
                keys.append(garbled_gate['outputs'][1])  
                return keys
        return None

    # Generates or finds the appropriates input keys for a gate
    def generateInputKeys(self, gate, garbled_circuit):
        keys = []
        wire1Found = False
        wire2Found = False
        #if the wire already has a set of keys generated, find them
        if(self.wires.get(gate['input'][0]) is not None):
            wireKeys = self.wires.get(gate['input'][0])
            keys = keys + wireKeys
            wire1Found = True
        if(not wire1Found):
            #if the wire is the output of another gate, find its keys
            res = self.getKeyFromGateOutput(garbled_circuit, gate['input'][0])
            if(res is not None):
                keys = keys + res
            #if they are not generate 2 keys
            else:
                keys.append(self.generateKey())
                keys.append(self.generateKey())
            #log the wire: [key1,key2] combination in a dictionary
            self.wires.update({gate['input'][0]:keys})
        #do the same for the second wire
        if(self.wires.get(gate['input'][1]) is not None):
            wireKeys = self.wires.get(gate['input'][1])
            keys = keys + wireKeys
            wire2Found = True
        if(gate['input'][0] != gate['input'][1]):
            if(not wire2Found):
                #if the wires is an output from another gate, find their corresponding keys
                res = self.getKeyFromGateOutput(garbled_circuit, gate['input'][1])
                #if they are not generate 2 keys
                if(res == None):
                    keys.append(self.generateKey())
                    keys.append(self.generateKey())
                else:
                    keys = keys + res
                self.wires.update({gate['input'][1]:[keys[2],keys[3]]})                    
        else:
            keys.append(keys[0])
            keys.append(keys[1])
        self.keys = keys

    #Generates two keys that mark the output of a gate
    def generateOutputKeys(self):
        outputs = []
        outputs.append(self.generateKey())  # keyW_0
        outputs.append(self.generateKey())  # keyW_1
        self.outputs = outputs

    #garble a gate
    def garble(self, gate, garbled_circuit):
        # Nand truth table
        truth_table = ['1', '1', '1', '0']

        #generate the 4 input keys
        self.generateInputKeys(gate, garbled_circuit)
        #generate the 2 output keys
        self.generateOutputKeys()
        # create the 4 cyphertexts
        cyphertext = []
        cyphertext.append(Fernet(self.keys[2]).encrypt(
            Fernet(self.keys[0]).encrypt(truth_table[0].encode())))
        cyphertext.append(Fernet(self.keys[2]).encrypt(
            Fernet(self.keys[1]).encrypt(truth_table[1].encode())))
        cyphertext.append(Fernet(self.keys[3]).encrypt(
            Fernet(self.keys[0]).encrypt(truth_table[2].encode())))
        cyphertext.append(Fernet(self.keys[3]).encrypt(
            Fernet(self.keys[1]).encrypt(truth_table[3].encode())))
        self.cyphertext = cyphertext