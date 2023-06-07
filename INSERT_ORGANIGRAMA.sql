
INSERT INTO Organigramas(COD_ORG, ORG, FEC) VALUES ('ABC', 'EjemploEmpresa', '2023-05-19');

INSERT INTO Dependencias(COD_DEP, NOM, COD_ORG) VALUES ('AAAA', 'CEO', 'ABC');

INSERT INTO OrgDep(COD_ORG, DEP_MAYOR) VALUES('ABC', 'AAAA');

INSERT INTO Dependencias(COD_DEP, NOM, COD_ORG) VALUES ('ABAA', 'Financias', 'ABC');
INSERT INTO Dependencias(COD_DEP, NOM, COD_ORG) VALUES ('ACAA', 'Produccion', 'ABC');
INSERT INTO Dependencias(COD_DEP, NOM, COD_ORG) VALUES ('ADAA', 'Marketing', 'ABC');
INSERT INTO Dependencias(COD_DEP, NOM, COD_ORG) VALUES ('ABBA', 'Gerencia Industrial', 'ABC');
INSERT INTO Dependencias(COD_DEP, NOM, COD_ORG) VALUES ('ABCA', 'Gerencia de recursos', 'ABC');
INSERT INTO Dependencias(COD_DEP, NOM, COD_ORG) VALUES ('ABDA', 'Gerencia de calidad', 'ABC');

UPDATE Dependencias SET pos_x=600, pos_y=100 WHERE COD_DEP ='AAAA';
UPDATE Dependencias SET pos_x=400, pos_y=200 WHERE COD_DEP ='ABAA';
UPDATE Dependencias SET pos_x=600, pos_y=200 WHERE COD_DEP ='ACAA';
UPDATE Dependencias SET pos_x=800, pos_y=200 WHERE COD_DEP ='ADAA';
UPDATE Dependencias SET pos_x=200, pos_y=300 WHERE COD_DEP ='ABBA';
UPDATE Dependencias SET pos_x=400, pos_y=300 WHERE COD_DEP ='ABCA';
UPDATE Dependencias SET pos_x=600, pos_y=300 WHERE COD_DEP ='ABDA';

INSERT INTO DepDep(DEP_ANT, DEP_SUC) VALUES('AAAA', 'ABAA');
INSERT INTO DepDep(DEP_ANT, DEP_SUC) VALUES('AAAA', 'ACAA');
INSERT INTO DepDep(DEP_ANT, DEP_SUC) VALUES('AAAA', 'ADAA');

INSERT INTO DepDep(DEP_ANT, DEP_SUC) VALUES('ABAA', 'ABBA');
INSERT INTO DepDep(DEP_ANT, DEP_SUC) VALUES('ABAA', 'ABCA');
INSERT INTO DepDep(DEP_ANT, DEP_SUC) VALUES('ABAA', 'ABDA');
