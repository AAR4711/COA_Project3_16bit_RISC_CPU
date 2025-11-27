from register_file import RegisterFile
from memory import Memory
from utils import *

class ALU:
    def exec(self, op, a, b):
        if op == OP_ADD:  return a + b
        if op == OP_SUB:  return a - b
        if op == OP_AND:  return a & b
        if op == OP_ADDI: return a + b
        return 0

class CPU:
    def __init__(self, program):
        self.reg = RegisterFile()
        self.mem = Memory()
        self.program = program
        self.pc = 0
        self.alu = ALU()

        self.IF  = {"instr": None, "pc": 0}
        self.ID  = {"instr": None}
        self.EX  = {"alu_out": 0, "rd": None}
        self.MEM = {"val": 0, "rd": None}
        self.WB  = {"val": 0, "rd": None}

   
    #   PIPELINE STAGES
  

    def fetch_decode(self):
        if self.pc < len(self.program):
            self.IF = {"instr": self.program[self.pc], "pc": self.pc}
            self.ID = {"instr": self.program[self.pc]}
        else:
            self.IF = {"instr": {"type":"R","op":NOP,"rs":0,"rt":0,"rd":0,"imm":0}, "pc": self.pc}
            self.ID = {"instr": self.IF["instr"]}
        self.pc += 1

    def execute(self):
        ins = self.ID["instr"]
        if ins is None:
            self.EX = {"alu_out": 0, "rd": None}
            return

        op, rs, rt, rd, imm = ins["op"], ins["rs"], ins["rt"], ins["rd"], ins["imm"]

        a = self.reg.read(rs)
        b = self.reg.read(rt) if ins["type"] == "R" else imm

        

        # Forward for rs
        if self.MEM["rd"] == rs:
            a = self.MEM["val"]
        if self.WB["rd"] == rs:
            a = self.WB["val"]

        # Forward for rt (only R-type)
        if ins["type"] == "R":
            if self.MEM["rd"] == rt:
                b = self.MEM["val"]
            if self.WB["rd"] == rt:
                b = self.WB["val"]

        out = self.alu.exec(op, a, b)
        self.EX = {"alu_out": out, "rd": rd}

    def memory(self):
        self.MEM = {"val": self.EX["alu_out"], "rd": self.EX["rd"]}

    def write_back(self):
        if self.MEM["rd"] is not None:
            self.reg.write(self.MEM["rd"], self.MEM["val"])
            self.WB = {"val": self.MEM["val"], "rd": self.MEM["rd"]}

   

    def step(self):
        self.fetch_decode()
        self.execute()
        self.memory()
        self.write_back()

    def dump_registers(self):
        print("Registers:", self.reg.r)
