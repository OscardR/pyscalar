#!/usr/bin/env python
# coding:utf8

"""
Created on 08/03/2014
@author: Óscar Gómez Alcañiz <oscar.gomez@uji.es>
"""

from app.log import Log
from datastructures import asm
from datastructures.instruction import Trap

l = Log( "pipeline" )

class Stage( object ):
    """
    Base class for the pipelining implementation
    """
    def __init__( self, name, cpu ):
        self.name = name
        l.v( "Stage %s initialized!" % name, "Stage" )
        self.cpu = cpu

    def execute( self ):
        raise NotImplementedError( 
            "Stage {0} has not implemented 'execute' method!".format( self.name ) )


class IF( Stage ):
    """
    Instruction Fetch
    =================
    Instructions are captured from the instructions memory and inserted onto
    the instructions buffer, at a rate of 'S' instructions per cycle
    """
    def __init__( self, cpu ):
        super( IF, self ).__init__( "IF", cpu )
        self.S = self.cpu.S
        self.imem = self.cpu.imem  # Instructions Memory
        self.ib = self.cpu.ib  # Instructions Buffer

    def execute( self ):
        # S-Scalar fetches S instructions per cycle
        for _ in range( self.S ):
            # Extract instruction from Instructions Memory...
            inst = self.imem.fetch_instruction( self.cpu.PC )

            # ...and push it into the Instructions Buffer
            self.ib.push_instruction( inst )

            l.d( "[ PC {:>2} ] {}".format( self.cpu.PC, inst ), "IF/{}".format( _ ) )

            # Increment PC
            self.cpu.increment_PC()

class ID( Stage ):
    """
    Instruction Decode
    ==================
    Instructions are inserted onto the instruction window, 
    after fetching the operands from the register bank
    """
    def __init__( self, cpu ):
        super( ID, self ).__init__( "ID", cpu )
        self.ib = self.cpu.ib  # Instructions Buffer
        self.iw = self.cpu.iw  # Instructions Window
        self.regs = self.cpu.regs  # Registers Bank
        self.rob = self.cpu.rob  # Reorder Buffer
        self.S = self.cpu.S  # S-Scalar factor

    def execute( self ):
        for _ in range( self.S ):
            # If the Instruction Window has free slots
            if not self.iw.is_full():
                n_inst, inst = self.ib.pop_instruction()

                l.d( inst, "ID/{}".format( _ ) )
                # If no instruction is available, iterate
                if inst == None: break

                # Extract OP code and destination register
                ( codop, dest ) = inst.codop, inst.dest

                # Check the instruction is not a TRAP or NOP
                if codop not in [asm.TRAP, asm.NOP]:

                    # Add dest register to the ReorderBuffer
                    self.rob.insert_line( \
                        n_inst=n_inst, \
                        dest=dest, \
                        value=self.regs[dest], \
                        ok=self.regs.check_ok( dest ) )

                    # Invalidate dest reg on the registers bank
                    self.regs.invalidate( dest )

                    # Get ROB line where operand 1 can be retrieved from
                    # Or else retrieve it from the registers bank
                    if self.regs[inst.op1] == None:
                        i = self.rob.get_last_index( inst.op1 )
                        op1 = self.rob[ i ].value
                        ok1 = self.rob[ i ].ok
                    else:
                        op1 = self.regs[inst.op1]
                        ok1 = True

                    # If OP code is not an inmediate type, get ROB line for
                    # operand 2 as well
                    if codop not in [asm.MULTI, asm.ADDI, asm.DIVI, asm.SUBI, asm.LW, asm.SW]:
                        if self.regs[inst.op2] == None:
                            i = self.rob.get_last_index( inst.op2 )
                            op2 = self.rob[ i ].value
                            ok2 = self.rob[ i ].ok
                        else:
                            op2 = self.regs[inst.op2]
                            ok2 = True
                    else:
                        op2, ok2 = inst.op2, True

                    # Insert instruction into the Instructions Window
                    self.iw.insert_instruction( codop, dest, op1, ok1, op2, ok2 )
                else:
                    if codop == asm.TRAP:
                        raise Trap( "TRAP on Stage ID" )

class ISS( Stage ):
    """
    Issue Stage
    ===========
    Instructions which have their operands are issued from the instructions window,
    to their functional units, if they are available for their operation.
    """
    def __init__( self, cpu ):
        super( ISS, self ).__init__( "ISS", cpu )
        self.S = self.cpu.S
        self.iw = self.cpu.iw
        self.fu = self.cpu.fu

    def execute( self ):
        # S-scalar processors issue S instructions per cycle
        issued = 0
        possible = self.S
        while issued < self.S and possible > 0:
            pos, inst = self.iw.next_ready_instruction()
            l.d( "{}".format( inst ), "ISS/{}".format( issued ) )

            # If no instructions are ready, abort stage
            if inst == None:
                break

            # Do nothing if it's a TRAP instruction
            elif inst.codop == asm.TRAP:
                raise Trap( "TRAP on Stage ISS" )

            # If it's a MULTtiplication or division,
            # push it to the MULTtiplication functional units
            elif inst.codop in [asm.MULT, asm.MULTI, asm.DIV, asm.DIVI]:
                if self.fu[asm.MULT].is_empty():
                    self.fu[asm.MULT].feed( inst.op1, inst.op2, inst.dest )
                    self.iw.flush_instruction( pos )
                    issued += 1

            # Same for addition and substraction
            elif inst.codop in [asm.ADD, asm.ADDI, asm.SUB, asm.SUBI]:
                if self.fu[asm.ADD].is_empty():
                    self.fu[asm.ADD].feed( inst.op1, inst.op2, inst.dest )
                    self.iw.flush_instruction( pos )
                    issued += 1

            possible -= 1

class ALU( Stage ):
    """
    ALU Stage
    =========
    In this stage all functional units compute a cycle.
    """
    def __init__( self, cpu ):
        super( ALU, self ).__init__( "ALU", cpu )
        self.fu = self.cpu.fu

    def execute( self ):
        # Every Functional Unit moves forward one step
        for t in self.fu:
            fu = self.fu[t]
            if fu.is_empty():
                l.d( "[ {}/- ] <empty>".format( fu ), "ALU" )
                continue
            step = fu.step()
            l.d( "[ {}/{} ] ROB:{}".format( fu, step, fu.dest ), "ALU" )

class MEM( Stage ):
    """
    MEM Stage
    =========
    In this stage results from completed functional 
    units are written to memory. 
    """
    def __init__( self, cpu ):
        super( MEM, self ).__init__( "MEM", cpu )
        self.mem = self.cpu.dmem
        self.fu = self.cpu.fu

    def execute( self ):
        # Every Functional Unit which has completed execution writes results to Mem
        for t in self.fu:
            fu = self.fu[t]
            if fu.is_completed():
                if fu.op == asm.SW:
                    self.mem[fu.get_result()] = self.rob[ fu.dest ].value
                l.d( "[ {} ] <completed>".format( fu ), "MEM" )

class WB( Stage ):
    """
    WB Stage
    ========
    In this stage all results from finished functional units 
    are written to the reorder buffer.
    """
    def __init__( self, cpu ):
        super( WB, self ).__init__( "WB", cpu )
        self.rob = self.cpu.rob
        self.fu = self.cpu.fu

    def execute( self ):
        # Every Functional Unit's result is harvested (from the FU or Mem) and
        # written to its corresponding line of the ROB
        for t in self.fu:
            fu = self.fu[t]
            if fu.is_completed():
                rob_line = self.rob[ fu.dest ]
                if fu.op == asm.LW:
                    rob_line.set_value( self.mem[fu.get_result()] )
                else:
                    rob_line.set_value( fu.get_result() )
                rob_line.set_ok()
                l.d( "[ {} ] <completed>".format( fu ), "WB" )

class COM( Stage ):
    """
    COM Stage
    =========
    In this stage all correct values from the reorder buffer get written 
    to their correspondent registers in the register bank.
    """
    def __init__( self, cpu ):
        super( COM, self ).__init__( "COM", cpu )
        self.regs = self.cpu.regs
        self.rob = self.cpu.rob

    def execute( self ):
        for line in self.rob.flush_finished():
            self.regs[line.dest] = line.value
            l.d( "[ ROB{:>2} ] reg: {} = {} / OK!".format( line.index, reg.name( line.dest ), line.value ), "COM" )
