"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0
        self.hlt = False
        self.ldi = 0b10000010
        self.prn = 0b01000111
        self.halt = 0b00000001
        self.mul = 0b10100010
        self.cmp = 0b10100111

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    # def LDI(self):
    #     self.register[self.ram_read(self.pc + 1)] = self.ram_read(self.pc + 2)
    #     self.pc += 3

    # def PRN(self):
    #     print(f'value: {self.register[self.ram_read(self.pc + 1)]}')
    #     self.pc += 2

    # def HLT(self):
    #     self.hlt = True
    #     self.pc += 1

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        try:
            address = 0
            with open(filename) as f:
                for line in f:
                    comment_split = line.split("#")[0].strip()
                    # n = comment_split[0].strip()

                    if comment_split == '':
                        continue

                    val = int(comment_split, 2)
                    # store val in memory
                    self.ram[address] = val

                    address += 1

                # print(f"{x:08b}: {x:d}")

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
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

    def run(self):
        while self.hlt == False:
            ir = self.ram[self.pc]  # IR = instruction register
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == self.ldi:  # store a value in register
                self.register[self.ram_read(
                    self.pc + 1)] = self.ram_read(self.pc + 2)
                self.pc += 3
            elif ir == self.prn:  # print a value in the register
                print(f'{self.register[self.ram_read(self.pc + 1)]}')
                self.pc += 2
            elif ir == self.mul:  # multiply
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            elif ir == self.halt:  # halt
                self.hlt = True
                self.pc += 1
            else:
                raise Exception("Unsupported ALU operation")
