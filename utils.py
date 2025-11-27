
OP_ADD, OP_SUB, OP_AND, OP_ADDI, NOP = 1, 2, 3, 4, 0

def instr_r(op, rs, rt, rd):
    return {"type":"R", "op":op, "rs":rs, "rt":rt, "rd":rd, "imm":0}

def instr_i(op, rs, imm, rd):
    return {"type":"I", "op":op, "rs":rs, "rt":0, "rd":rd, "imm":imm}
