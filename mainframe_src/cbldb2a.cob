       IDENTIFICATION DIVISION.                                         00010000
       PROGRAM-ID. CBLDB2A.                                             00020000
       ENVIRONMENT DIVISION.                                            00030000
       INPUT-OUTPUT SECTION.                                            00040000
       FILE-CONTROL.                                                    00040100
           SELECT OUT-FILE      ASSIGN TO OUTDD                         00041000
                                ORGANIZATION SEQUENTIAL                 00042000
                                ACCESS SEQUENTIAL                       00043000
                                FILE STATUS WS-STAT.                    00044000
       DATA DIVISION.                                                   00050000
       FILE SECTION.                                                    00050100
       FD OUT-FILE.                                                     00051000
       01 OUT-REC PIC X(10).                                            00057000
       WORKING-STORAGE SECTION.                                         00060000
       01 WS-SQLCD PIC S9(9) SIGN LEADING SEPARATE.                     00170000
      *COPY COPY1.                                                      00180000
       EXEC SQL                                                         00190000
       INCLUDE COPY1                                                    00200000
       END-EXEC.                                                        00210000
                                                                        00220000
       EXEC SQL                                                         00260000
          INCLUDE SQLCA                                                 00270000
       END-EXEC.                                                        00280000
                                                                        00280100
       01 WS-DOB PIC X(10).                                             00280200
       01 WS-PNAME PIC X(10).                                           00280300
       01 WS-STAT PIC X(02).                                            00280400
       01 ABEND-CODE PIC S9(9) COMP.                                    00280500
                                                                        00281000
       LINKAGE SECTION.                                                 00290000
                                                                        00330000
       PROCEDURE DIVISION.                                              00340000
       A-PARA.                                                          00350000
           DISPLAY 'CBLDB2A'.                                           00360000
           ACCEPT WS-DOB                                                00370000
           ACCEPT WS-PNAME                                              00371000
           DISPLAY 'DOB:'WS-DOB                                         00380000
           DISPLAY 'PNAME:'WS-PNAME                                     00390000
           OPEN OUTPUT OUT-FILE.                                        00400000
           DISPLAY 'OUTPUT STATUS:'WS-STAT.                             00410000
                                                                        01010000
           EXEC SQL                                                     01020000
              INSERT INTO PERSNLDTL(PNAME,DOB)                          01030000
              VALUES(:WS-PNAME,:WS-DOB)                                 01031000
           END-EXEC.                                                    01050000
                                                                        01110000
           EVALUATE SQLCODE                                             01120000
              WHEN +0                                                   01130000
                 DISPLAY 'SUCESS INST'                                  01140000
                 MOVE SQLCODE TO WS-SQLCD                               01150000
                 DISPLAY 'WS-SQLCD:'WS-SQLCD                            01170000
                 DISPLAY 'SQLERRD:'SQLERRD(3)                           01171000
              WHEN OTHER                                                01180000
                 MOVE SQLCODE TO WS-SQLCD                               01190000
                 DISPLAY 'SQLCODE:'SQLCODE, WS-SQLCD                    01200000
                 DISPLAY 'FAIL INST'                                    01230000
                 MOVE  200 TO ABEND-CODE                                01231000
                 CALL 'CEE3ABD' USING ABEND-CODE                        01232000
           END-EVALUATE.                                                01240000
                                                                        01240100
           MOVE WS-SQLCD TO OUT-REC.                                    01241000
           WRITE OUT-REC.                                               01242000
           DISPLAY 'WRITE STATUS:'WS-STAT.                              01243000
                                                                        01243100
           CLOSE OUT-FILE.                                              01244000
           DISPLAY 'CLOSE STATUS:'WS-STAT.                              01245000
                                                                        01250000
           STOP RUN.                                                    01290000
       A-EXIT.                                                          01300000
           EXIT.                                                        01310000
