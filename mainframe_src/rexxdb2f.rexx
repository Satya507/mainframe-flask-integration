/*REXX*/                                                                00010000
PULL PNAME                                                              00011000
SAY 'PNAME:'PNAME                                                       00012000
ADDRESS TSO                                                             00012100
/*"TSOLIB ACTIVATE DATASET('DB2SYS.SDSNLOAD')"*/                        00013000
"SUBCOM DSNREXX"                                                        00020000
SAY RC                                                                  00030000
S_RC = RXSUBCOM('ADD','DSNREXX','DSNREXX')                              00040000
ADDRESS DSNREXX "CONNECT "'DB2SYS'                                      00050000
SAY RC                                                                  00060000
SAY 'CONN:'SQLCODE                                                      00070000
                                                                        00080000
SQLSTMT ="SELECT                                                        00090000
DOB                                                                     00100000
FROM PERSNLDTL                                                          00110000
WHERE PNAME = ?"                                                        00120000
                                                                        00130000
ADDRESS DSNREXX "EXECSQL DECLARE C1 CURSOR FOR S1"                      00160000
SAY 'DECL:'SQLCODE                                                      00170000
ADDRESS DSNREXX "EXECSQL PREPARE S1 INTO :OUTSQLDA FROM :SQLSTMT"       00180000
SAY 'PREP:'SQLCODE                                                      00190000
ADDRESS DSNREXX "EXECSQL OPEN C1 USING ",                               00200000
":PNAME"                                                                00210000
SAY 'OPEN:'SQLCODE                                                      00220000
                                                                        00230000
/*ADDRESS DSNREXX "EXECSQL FETCH C1 USING DESCRIPTOR :OUTSQLDA"*/       00240000
ADDRESS DSNREXX "EXECSQL FETCH C1 INTO :DOB"                            00250000
SAY 'FETC:'SQLCODE                                                      00260000
/*SAY 'IN-AGE:'OUTSQLDA.1.SQLDATA*/                                     00270000
SAY 'DOB:'DOB                                                           00280000
ADDRESS DSNREXX "EXECSQL CLOSE C1"                                      00320000
SAY 'CLOS:'SQLCODE                                                      00330000
ADDRESS DSNREXX "DISCONNECT"                                            00340000
SAY 'DISC:'SQLCODE                                                      00350000
ADDRESS 'TSO'                                                           00360000
INFILE='USER.ADDOUT'                                                    00470000
IF SYSDSN(INFILE) <> "OK" THEN DO                                       00480000
   "ALLOC FI(INDD) DA("INFILE") NEW",                                   00490000
   "SPACE(10,10) CYL",                                                  00500000
   "RECFM(F B) LRECL(50)"                                               00510000
   END                                                                  00520000
SAY RC                                                                  00530000
"ALLOC FI(INDD) DA("INFILE") SHR REU"                                   00540000
B.1=DOB                                                                 00550000
"ALLOC FI(INDD) DA("INFILE") OLD REU"                                   00560000
"EXECIO * DISKW INDD (STEM B. FINIS"                                    00570000
"FREE FI(INDD)"                                                         00580000
SAY RC                                                                  00590000
