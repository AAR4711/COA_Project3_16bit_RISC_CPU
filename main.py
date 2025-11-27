from cpu_pipeline import CPU
from utils import *

# Program with RAW hazards (tests forwarding)
program = [
    instr_i(OP_ADDI, rs=0, imm=5, rd=1),   # R1 = 5
    instr_r(OP_ADD, rs=1, rt=1, rd=2),     # R2 = R1 + R1 
    instr_r(OP_SUB, rs=2, rt=1, rd=3),     # R3 = R2 - R1 
]

cpu = CPU(program)

for _ in range(3):
    cpu.step()

cpu.dump_registers()
