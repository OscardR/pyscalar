#!/usr/bin/env python
# coding:utf8

"""
Created on 08/03/2014
@author: Óscar Gómez Alcañiz <oscar.gomez@uji.es>
"""

from app.log import Log
from datastructures import asm
from datastructures.instruction import Trap
from arch import rob, reg

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

            if inst != None:
                l.d( "[ {} ] >> IB".format( inst ), "IF/{}".format( _ ) )
            else:
                l.d( "[ ---idle--- ]", "IF/{}".format( _ ) )

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

                # If no instruction is available, iterate
                if inst == None:
                    l.d( "[ ---idle--- ]", "ID/{}".format( _ ) )
                    break

                # Log
                l.d( "[ I{} ] << {}".format( n_inst, inst ), "ID/{}".format( _ ) )

                # Extract OP code and destination register
                ( codop, dest ) = inst.codop, inst.dest

                # Check the instruction is not a TRAP or NOP
                if codop not in [asm.TRAP, asm.NOP]:

                    # Add dest register to the ReorderBuffer
                    self.rob.insert_line( \
                        n_inst=n_inst, \
                        dest=dest, \
                        value=None, \
                        ok=False )

                    # Invalidate dest reg on the registers bank
                    self.regs.invalidate( dest )

                    # Get ROB line where operand 1 can be retrieved from
                    # Or else retrieve it from the registers bank
                    if self.regs[inst.op1] == None:
                        i = self.rob.get_last_index( inst.op1 )
                        if self.rob[i].ok:
                            op1 = self.rob[ i ].value
                        else:
                            op1 = i
                        ok1 = self.rob[ i ].ok
                    else:
                        op1 = self.regs[inst.op1]
                        ok1 = True

                    # If OP code is not an inmediate type, get ROB line for
                    # operand 2 as well
                    if codop not in [asm.MULTI, asm.ADDI, asm.DIVI, asm.SUBI, asm.LW, asm.SW]:
                        if self.regs[inst.op2] == None:
                            i = self.rob.get_last_index( inst.op2 )
                            if self.rob[i].ok:
                                op2 = self.rob[ i ].value
                            else:
                                op2 = i
                            ok2 = self.rob[ i ].ok
                        else:
                            op2 = self.regs[inst.op2]
                            ok2 = True
                    else:
                        op2, ok2 = inst.op2, True

                    # Insert instruction into the Instructions Window
                    l.d( "[ I{n_inst} ] >> IW".format( **locals() ) , "ID/{}".format( _ ) )
                    self.iw.insert_instruction( n_inst, codop, dest, op1, ok1, op2, ok2 )
                else:
                    # First trap check
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
        self.rob = self.cpu.rob

    def execute( self ):

        # S-scalar processors issue S instructions per cycle
        issued = 0
        possible = self.S
        while issued < self.S and possible > 0:
            pos, n_inst, inst = self.iw.next_ready_instruction()

            # If no instructions are ready, abort stage
            if inst == None:
                l.d( "[ ---idle--- ]", "ISS/{}".format( issued ) )
                break

            # If it's a MULTtiplication or division,
            # push it to the MULTtiplication functional units
            elif inst.codop in [asm.MULT, asm.MULTI, asm.DIV, asm.DIVI]:
                if self.fu[asm.MULT].is_empty():
                    self.fu[asm.MULT].feed( inst.op1, inst.op2, inst.dest, n_inst )
                    self.rob.get_instruction( n_inst ).set_flag( rob.ISSUED )
                    self.iw.flush_instruction( pos )
                    # Log
                    l.d( "[ I{} ] >> {}".format( n_inst, self.fu[asm.MULT] ), "ISS/{}".format( issued ) )
                    issued += 1

            # Same for addition and substraction
            elif inst.codop in [asm.ADD, asm.ADDI, asm.SUB, asm.SUBI, asm.LW, asm.SW]:
                if self.fu[asm.ADD].is_empty():
                    self.fu[asm.ADD].feed( inst.op1, inst.op2, inst.dest, n_inst )
                    self.rob.get_instruction( n_inst ).set_flag( rob.ISSUED )
                    self.iw.flush_instruction( pos )
                    # Log
                    l.d( "[ I{} ] >> {}".format( n_inst, self.fu[asm.ADD] ), "ISS/{}".format( issued ) )
                    issued += 1

            possible -= 1

        # Always check trapping
        if self.cpu.has_trapped():
            raise Trap( "TRAP on Stage ISS" )

class ALU( Stage ):
    """
    ALU Stage
    =========
    In this stage all functional units compute a cycle.
    """
    def __init__( self, cpu ):
        super( ALU, self ).__init__( "ALU", cpu )
        self.fu = self.cpu.fu
        self.rob = self.cpu.rob

    def execute( self ):

        # Every Functional Unit moves forward one step
        for t in self.fu:
            fu = self.fu[t]
            if fu.is_empty():
                l.d( fu, "ALU" )
                continue
            else:
                self.rob.get_instruction( fu.n_inst ).set_flag( rob.EXECUTING )
                fu.step()
                l.d( "{} [ ROB {} ]".format( fu, fu.dest ), "ALU" )

        # Always check trapping
        if self.cpu.has_trapped():
            raise Trap( "TRAP on Stage ALU" )

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
        self.rob = self.cpu.rob

    def execute( self ):
        # Every Functional Unit which has completed execution writes results to Mem
        for t in self.fu:
            fu = self.fu[t]
            # TODO: Comprobar que llegada esta etapa aún quedan datos que recolectar de las FU's
            if fu.is_completed():
                if fu.codop == asm.SW:
                    self.mem[fu.get_result()] = self.rob[ fu.dest ].value
                    self.rob.get_instruction( fu.n_inst ).set_flag( rob.FINISHED )
                l.d( "[ {} ] [completed]".format( fu ), "MEM/ROB" )

        # Always check trapping
        if self.cpu.has_trapped():
            raise Trap( "TRAP on Stage MEM" )

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
        self.iw = self.cpu.iw

    def execute( self ):
        # Every Functional Unit's result is harvested (from the FU or Mem) and
        # written to its corresponding line of the ROB
        for t in self.fu:
            fu = self.fu[t]
            if fu.is_completed():
                rob_line = self.rob.get_instruction( fu.n_inst )
                if fu.codop == asm.LW:
                    rob_line.set_value( self.mem[fu.get_result()] )
                # TODO: Revisar la escritura en memoria
                elif fu.codop != asm.SW:
                    rob_line.set_value( fu.get_result() )
                rob_line.set_ok()
                rob_line.set_flag( rob.FINISHED )

                # Buscamos lineas en la IW que necesiten el dato
                iw_lines = self.iw.get_blocked_instructions( rob_line.index )
                # if iw_lines != None:
                for iw_line in iw_lines:
                    l.d( "Found: {}".format( iw_line.n_inst ), "WB/IW" )
                    if  iw_line.op1 == rob_line.index:
                        iw_line.op1 = rob_line.value
                        iw_line.ok1 = True
                        l.d( "OP1 <- OK!".format( iw_line ), "WB/IW" )
                    if iw_line.op2 == rob_line.index:
                        iw_line.op2 = rob_line.value
                        iw_line.ok2 = True
                        l.d( "OP2 <- OK!".format( iw_line ), "WB/IW" )

                l.d( "Written: {}".format( rob_line ), "WB/ROB" )
                l.d( "{} [completed]".format( fu ), "WB/ROB" )

        # Always check trapping
        if self.cpu.has_trapped():
            raise Trap( "TRAP on Stage WB" )

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
            l.d( "[ ROB{:>2} ] reg: {} <= {} / OK!".format( line.index, reg.name( line.dest ), line.value ), "COM/REG" )

        # Always check trapping
        if self.cpu.has_trapped():
            raise Trap( "TRAP on Stage COM" )
