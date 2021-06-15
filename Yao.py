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
            'type':gate['type'],
            'inputs':gate['input']
        }

    def generateKey(self):
        return Fernet.generate_key()

    # Used in the case where at least one input wire is the output wire
    # of another gate. Finds and returns the keys for the found output wire
    def getKeyFromGateOutput(self, garbled_circuit, wire_id):
        keys = []
        for garbled_gate in garbled_circuit:
            if(garbled_gate['id'] == wire_id):
                keys.append(garbled_gate['outputs'][0])  # keyY_0
                keys.append(garbled_gate['outputs'][1])  # keyY_1
                return keys
        return None

    # Generates or finds the appropriates keys for the gate input
    def generateInputKeys(self, gate, garbled_circuit):
        keys = []
        wire1Found = False
        wire2Found = False
        #if the either wire already has a set of keys generated, find them
        if(self.wires.get(gate['input'][0]) is not None):
            wireKeys = self.wires.get(gate['input'][0])
            keys = keys + wireKeys
            wire1Found = True
        if(not wire1Found):
            #if the wires is an output from another gate, find their corresponding keys
            res = self.getKeyFromGateOutput(garbled_circuit, gate['input'][0])
            #if they are not generate 2 keys
            if(res == None):
                keys.append(self.generateKey())
                keys.append(self.generateKey())
            else:
                keys = keys + res
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

    def generateOutputKeys(self):
        outputs = []
        outputs.append(self.generateKey())  # keyW_0
        outputs.append(self.generateKey())  # keyW_1
        self.outputs = outputs

    def garble(self, gate, garbled_circuit):
        # Nand truth table
        truth_table = ['1', '1', '1', '0']

        self.generateInputKeys(gate, garbled_circuit)
        self.generateOutputKeys()
        # create the cyphertexts from the truth table
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