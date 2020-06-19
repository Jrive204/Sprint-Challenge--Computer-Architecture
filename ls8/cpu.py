"""CPU functionality."""

import sys
import re

# instance = {
#     "LDI": 0b10000010,  # Sets the Value of a reg to an int
#     "HLT": 0b00000001,  # halts the program, "ends it"/"stops it"
#     "PRN": 0b01000111,  # Prints the value at the next reg
#     "MUL": 0b10100010,  # multiply reg at +1 with reg at +2
# }


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.is_run = False
        self.fl = 0b00000000
        self.sp = 0xF4

    def ram_read(self, mar):
        print("MAR: ", mar)
        return self.reg[mar]

    def ram_write(self, mdr, value):
        self.reg[mdr] = value

    def load(self, program_file):
        """Load a program into memory."""

        address = 0

        file = open(program_file, "r")
        for line in file.readlines():
            # load a line into memory (not including comments)
            try:
                x = line[:line.index("#")]
            except ValueError:
                x = line

            try:
                # convert binary to decimal
                y = int(x, 2)
                self.ram[address] = y
            except ValueError:
                continue
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def LDI(self):
        reg_index = self.ram[self.pc + 1]
        value = self.ram[self.pc + 2]
        self.reg[reg_index] = value
        self.pc += 3

    def HLT(self):
        self.is_run = False
        self.pc += 1

    def PRN(self):
        index = self.ram[self.pc + 1]
        value = self.reg[index]
        # print(f"Value: {value}, Register Index : {index}")
        print(f"Value: {value}")
        self.pc += 2

    def MUL(self):
        num1 = self.ram_read(self.ram[self.pc + 1])
        num2 = self.ram_read(self.ram[self.pc + 2])
        self.reg[self.ram[self.pc + 1]] = num1 * num2
        self.pc += 3

    def POP(self):

        # take from the stack and add it to the reg location
        # weird cause they both are  in reg
        # top parts of reg is stack
        value = self.ram[self.sp]
        self.reg[self.ram[self.pc + 1]] = value
        self.sp += 1
        self.pc += 2

    def PSH(self):
        # Decrement the SP
        self.sp -= 1
        # write the value in ram at pc to the stack (top parts of RAM)
        # save ram value to stack
        reg_num = self.ram[self.pc + 1]
        value = self.reg[reg_num]
        top_of_stack_addr = self.sp
        self.ram[top_of_stack_addr] = value
        self.pc += 2

    def ADD(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]
        self.alu("ADD", reg_a, reg_b)
        self.pc += 3

    def AND(self):
        pass

    def CALL(self):
        """
        push current pc to stack, so we can return later
            we do not want to inc the pc while pushing
        set pc to the address in the given register...
        register will hold a location that points to
        somewhere in ram, we will go there and do the things
        .....value is stored in a reg
        """
        self.sp -= 1
        self.ram[self.sp] = self.pc
        self.pc = self.reg[self.ram[self.pc + 1]]

    def CMP(self):
        """
        comepare 2 given regs
        set flags according to the out put
        reg_a === reg_b = flag  E to 1 or 0
        reg_a < reg_b = flag L to 1 or 0
        reg_a > reg_b = flag G to 1 or 0
        """
        reg_a = self.reg[self.ram[self.pc + 1]]
        reg_b = self.reg[self.ram[self.pc + 2]]

        if reg_a == reg_b:
            self.fl = 1
        else:
            self.fl = 0
        self.pc += 3

    def DEC(self):
        pass

    def DIV(self):
        pass

    def INC(self):
        pass

    def INT(self):
        pass

    def IRET(self):
        pass

    def JEQ(self):
        """
        if the Equal flag is true (0b00000001)
        then jump to the register
        """
        a = self.fl

        if a == 1:
            self.pc = self.reg[self.ram[self.pc + 1]]
        else:
            self.pc += 2

    def JGE(self):
        pass

    def JGT(self):
        pass

    def JLE(self):
        pass

    def JLT(self):
        pass

    def JMP(self):
        self.pc = self.reg[self.ram[self.pc + 1]]
        return True

    def JNE(self):
        """
        jump to given register if E flag is false
        
        """
        a = self.fl

        if a == 0:
            self.pc = self.reg[self.ram[self.pc + 1]]
        else:
            self.pc += 2

        pass

    def LD(self):
        pass

    def MOD(self):
        pass

    def NOP(self):
        pass

    def NOT(self):
        pass

    def OR(self):
        pass

    def PRA(self):
        pass

    def RET(self):
        """
        retrive are saved location, should be in stack
        and set the to pc
        inc pc 2 so we dont run call again.
        dec sp because we are poppin lockin
        """
        self.pc = self.ram[self.sp]
        self.pc += 2
        self.sp -= 1

        pass

    def SHL(self):
        pass

    def SHR(self):
        pass

    def ST(self):
        pass

    def SUB(self):
        pass

    def XLA(self):
        pass

    def call_func(self, n):
        func_stack = {
            0b10000010: self.LDI,
            0b00000001: self.HLT,
            0b01000111: self.PRN,
            0b10100010: self.MUL,
            0b01000110: self.POP,
            0b01000101: self.PSH,
            0b10100000: self.ADD,
            0b10101000: self.AND,
            0b01010000: self.CALL,
            0b10100111: self.CMP,
            0b01100110: self.DEC,
            0b10100011: self.DIV,
            0b01100101: self.INC,
            0b01010010: self.INT,
            0b00010011: self.IRET,
            0b01010101: self.JEQ,
            0b01011010: self.JGE,
            0b01010111: self.JGT,
            0b01011001: self.JLE,
            0b01011000: self.JLT,
            0b01010100: self.JMP,
            0b01010110: self.JNE,
            0b10000011: self.LD,
            0b10100100: self.MOD,
            0b00000000: self.NOP,
            0b01101001: self.NOT,
            0b10101010: self.OR,
            0b01001000: self.PRA,
            0b00010001: self.RET,
            0b10101100: self.SHL,
            0b10101101: self.SHR,
            0b10000100: self.ST,
            0b10100001: self.SUB,
            0b10101011: self.XLA

        }
        if n in func_stack:
            func_stack[n]()
        else:
            print(f"No instruction found! IR: {n}")
            sys.exit(1)

    def run(self):
        """Run the CPU."""
        self.is_run = True

        while self.is_run:
            ir = self.ram[self.pc]  # the instruction or code to run
            self.call_func(ir)

            # if ir == instance["LDI"]:
            #     self.ram_write(self.ram[self.pc + 1], self.ram[self.pc + 2])
            #     self.pc += 3

            # elif ir == instance["PRN"]:
            #     reg_num = self.ram[self.pc + 1]
            #     print(self.reg[reg_num])
            #     self.pc += 2

            # elif ir == instance["HLT"]:
            #     self.is_run = False
            #     self.pc += 1

            # elif ir == instance["MUL"]:
            #     num1 = self.ram_read(self.ram[self.pc + 1])
            #     num2 = self.ram_read(self.ram[self.pc + 2])
            #     print("MUL answere: ", num1 * num2)
            #     self.pc += 3

            # else:
            #     print(f'Unknown instruction {ir} at address {self.pc}')
            #     sys.exit(1)
