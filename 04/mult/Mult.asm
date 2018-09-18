// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

	@1 
	D=M
	@counter
	M=D

	@ZEROARG
	D;JEQ

	@0
	D=M
	@ZEROARG
	D;JEQ

	@result
	M=D
	@TESTEND
	0;JMP

(MULTLOOP)
	@0
	D=M
	@result
	D=M+D
	M=D

(TESTEND)
	@counter
	D=M
	D=D-1
	M=D
	@MULTLOOP
	D;JNE

(SAVERES)
	@result
	D=M
	@2
	M=D

(ENDLOOP)
	@ENDLOOP
	0;JMP

(ZEROARG)
	@result
	M=0
	@SAVERES
	0;JMP