/*REXX*/                                                                00001000
ADDRESS 'TSO'                                                           00010000
INFILE='USER.ADDDATA'                                                 00020000
"ALLOC FI(INDD) DA("INFILE") SHR REU"                                   00090000
"EXECIO * DISKR INDD (STEM A. FINIS"                                    00100000
PNAME=STRIP(A.1)                                                        00110000
DOB=STRIP(A.2)                                                          00120000
TM=STRIP(A.3)                                                           00130000
CALL SYSCALLS('ON')                                                     00140000
ADDRESS SYSCALL                                                         00150000
SAY 'SLEEP STARTED'                                                     00151000
"SLEEP" TM                                                              00160000
SAY 'SLEEP ENDED'                                                       00161000
CALL SYSCALLS('OFF')                                                    00170000
ADDRESS 'ISPEXEC'                                                       00171000
INJCL='USER.JCLLIB(CBLDB2RN)'                                         00172000
"VPUT (PNAME,DOB)"                                                      00180000
"EDIT DATASET("INJCL") MACRO(CBLDBMAC)"                                 00190000
