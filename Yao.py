from cryptography.fernet import Fernet


class GarbleGate:

    def __init__(self):
        self.keys = [],
        self.cyphertext = []
        self.outputs = []

    def run(self, garbledCircuit, circuitInputs, gate):
        self.garble(gate, circuitInputs, garbledCircuit)
        return {
            'id': gate['id'],
            'keys': self.keys,
            'cyphertext': self.cyphertext,
            'outputs': self.outputs
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
    def generateInputKeys(self, gate, circuit_inputs, garbled_circuit):
        keys = []
        # if the gate input wires are input wires, generate 4 keys
        if(gate['type'] == "input"):
            keys.append(self.generateKey())  # keyX_0
            keys.append(self.generateKey())  # keyX_1
            keys.append(self.generateKey())  # keyY_0
            keys.append(self.generateKey())  # keyY_1
        elif(gate['type'] == "outer"):
            if(gate['input'][0] in circuit_inputs):
                keys.append(self.generateKey())  # keyX_0
                keys.append(self.generateKey())  # keyX_1
            else:
                res = self.getKeyFromGateOutput(garbled_circuit, gate['input'][0])
                if(res == None):
                    return None
                keys = keys + res
            if(gate['input'][1] in circuit_inputs):
                keys.append(self.generateKey())  # keyY_0
                keys.append(self.generateKey())  # keyY_1
            else:
                res = self.getKeyFromGateOutput(garbled_circuit, gate['input'][1])
                if(res == None):
                    return None
                keys = keys + res
        self.keys = keys

    def generateOutputKeys(self):
        outputs = []
        outputs.append(self.generateKey())  # keyW_0
        outputs.append(self.generateKey())  # keyW_1
        self.outputs = outputs

    def garble(self, gate, circuit_inputs, garbled_circuit):
        # Nand truth table
        truth_table = ['1', '1', '1', '0']

        self.generateInputKeys(gate, circuit_inputs, garbled_circuit)
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