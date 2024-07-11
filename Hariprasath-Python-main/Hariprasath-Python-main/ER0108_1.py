import os
# import subprocess
import logging
# import cx_Oracle
from datetime import datetime
#import moconfig
import sys
#import helperfunctions
import helperFunctions_v3 as helperfunctions1

# Environment variables and directory setup
CURDIR = os.getcwd()
WGDIR = os.path.dirname(CURDIR)
REPTDIR = os.path.dirname(WGDIR)
AST_SCRIPTS = WGDIR
os.environ['CURDIR'] = CURDIR
os.environ['WGDIR'] = WGDIR
os.environ['REPTDIR'] = REPTDIR
os.environ['AST_SCRIPTS'] = AST_SCRIPTS


# file3=open('Hari _297_client_profile_managed_account.txt','x')

RDB_FOLDER = "Hari_297"
APFILENAME = "Hari_297_{}".format(datetime.now().strftime('%Y%m%d'))
# print(APFILENAME)

# os.chdir(os.path.join(AST_SCRIPTS, RDB_FOLDER))
LOG = os.path.join(AST_SCRIPTS, RDB_FOLDER, os.path.basename(__file__) + '.log')
os.environ['LOG'] = LOG
# Process name variable
PROCESS = os.path.basename(__file__).split('.')[0]
print(PROCESS)
logging.info(PROCESS)

inFile = 'Hari_297_temp_file.txt'
inFile1 = 'Hari_297_ER0108'
inFile2 = 'Hari_297_match.csv'
inFile3 = 'protagonist.csv'

sftp_in = os.path.join(AST_SCRIPTS)  # Path for SFTP incoming files
# datapath = os.path.join(AST_SCRIPTS,'content3') 

def dropTable( table_name, suppress_error=True):
    statement = ""
    if suppress_error:
        statement ='''
        BEGIN b         
        EXECUTE IMMEDIATE 'TRUNCATE TABLE {}';
        EXECUTE IMMEDIATE 'DROP TABLE {}';
        EXCEPTION
        WHEN OTHERS THEN
            IF sqlcode != -0942 THEN RAISE; 
            END IF;
        END;
        '''.format(table_name,table_name)
    else:
        statement = "drop table {}".format( table_name)
    if not helperfunctions1.executeSQL(statement):
        logging.error("Error in executing sql")

# Beginning of program
logging.info("Started Hari_297_ER0108 reports at {}".format(datetime.now()))
sql_to_execute = """BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE Hari_297_accnt_input';
EXCEPTION
   WHEN OTHERS THEN
      IF SQLCODE != -942 THEN
         RAISE;
      END IF;
END;"""

# if not helperfunctions1.executeSQL(sql_to_execute):
#     logging.error("Error in executing sql")
#     sys.exit(101)
sql_to_execute ="""
CREATE TABLE Hari_297_accnt_input
(
branch VARCHAR2(3),
branch_name VARCHAR2(30),
representative VARCHAR2(3),
representative_name VARCHAR2(50),
client_id NUMBER,
client_name VARCHAR2(100),
account_id VARCHAR2(20),
date_added VARCHAR2(8),
inv_obj_income VARCHAR2(10),
inv_obj_gs VARCHAR2(10),
inv_obj_gm VARCHAR2(10),
inv_obj_gl VARCHAR2(10),
risk_tol_low VARCHAR2(10),
risk_tol_med VARCHAR2(10),
risk_tol_high VARCHAR2(10)
)"""
# if not helperfunctions1.executeSQL(sql_to_execute):
#     logging.error("Error in executing sql")
#     sys.exit(101)
sql_to_execute = """BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE Hari_297_match';
EXCEPTION
   WHEN OTHERS THEN
      IF SQLCODE != -942 THEN
         RAISE;
      END IF;
END;"""
# if not helperfunctions1.executeSQL(sql_to_execute):
#     logging.error("Error in executing sql")
#     sys.exit(101)
sql_to_execute = """
CREATE TABLE Hari_297_match (
    orig_representative VARCHAR2(6),
    representative VARCHAR2(6),
    fckey VARCHAR2(6),
    orig_branch VARCHAR2(8),
    branch VARCHAR2(100),
    branchCode VARCHAR2(100),
    region VARCHAR2(100),
    owner_domain VARCHAR2(100),
    owner_id VARCHAR2(100),
    folder_id VARCHAR2(255)
)
"""


# if not helperfunctions1.executeSQL(sql_to_execute):
#     logging.error("Error in executing sql")
#     sys.exit(101)

sql_to_execute = """BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE Hari_297_Qr';
EXCEPTION
   WHEN OTHERS THEN
      IF SQLCODE != -942 THEN
         RAISE;
      END IF;
END;"""
# if not helperfunctions1.executeSQL(sql_to_execute):
#     logging.error("Error in executing sql")
#     sys.exit(101)
sql_to_execute = """
CREATE TABLE Hari_297_QR (
    MO_branch VARCHAR2(50),
    branchCode VARCHAR2(50),
    MO_branch_name VARCHAR2(500)
)
"""
# Values to insert
# sql_query="""INSERT INTO Hari_297_accnt_input (branch, branch_name, representative, representative_name, client_id, client_name, account_id, date_added, inv_obj_income, inv_obj_gs, inv_obj_gm, inv_obj_gl, risk_tol_low, risk_tol_med, risk_tol_high)
# VALUES ('003', 'Branch 3', '003', 'Suresh', 1003, 'Client C', 'ACC1003', '20240103', 'High', 'Low', 'Medium', 'Medium', 'Low', 'Medium', 'High')
# """
sql_query="""SELECT *FROM  Hari_297_accnt_input"""
# helperfunctions1.executeSQL(sql_query)
helperfunctions1.exportTableDataToCSV("Hari_297_ER0108",sql_query)

# if not helperfunctions1.executeSQL(sql_to_execute):
#     logging.error("Error in executing sql")
#     sys.exit(101)

if helperfunctions1.file_exists_case_sensitive_generic(CURDIR,inFile):
    logging.info(f"File {inFile} exists")
else:
    logging.info(f"File {inFile} does not exist. Exiting")
    sys.exit(105)  #new change

if not helperfunctions1.copyFile(f"{CURDIR}/{inFile}", f"./{inFile1}"):#new change remove $
    logging.error(f"Copy of {inFile} failed!")
    sys.exit(105)


helperfunctions1.dos2unix(inFile)
curr_date = datetime.now().strftime('%Y%m%d')
logging.info("Current business date is {}".format(curr_date))
# sql_query="Select *From Hari_297_QR"
# Check the date in the file. It should be the current business date.
logging.info("Getting the header date in the file")

with open(inFile1, 'r') as input_file:
    first_line = input_file.readline()
    print(first_line)
with open('file1.txt', 'w') as output_file:
    output_file.write(first_line)
with open('file1.txt', 'r') as in_file:
    header = in_file.readline().split(',')[1].strip()
    
logging.info("The header date of the file is {}".format(header))

if header != curr_date:
    logging.error("Error: Invalid input file as it doesn't contain the current business date in the file header")
    #exit(2)
else:
    logging.info("The input file is correct and contains the current business date")

# Get record count in trailer record
logging.info("Getting the record count in the trailer of the file")
with open(inFile, 'r') as f:
    for line in f:
        pass
    trailer = line.split(',')[1].strip()
logging.info("The count in the trailer is {}".format(trailer))

# Remove header and footer from input files
logging.info("Deleting header and trailer from Hari _297_client_profile_managed_account.txt")
try: 
    with open(inFile, 'r') as f, open('Hari _297_temp_file.txt', 'w') as Hari_297_temp_file:
        lines = f.readlines()[2:-1]  # Skip first two lines and the last line
        Hari_297_temp_file.writelines(lines)
except Exception as e:
    logging.error("Error #105d: delete header and footer In {} Failed".format(inFile))
    #exit(105)

# Removing the first column from the input file which is the record indicator
logging.info("Deleting the indicator field from the temp file")

try:
    with open('Hari _297_temp_file.txt', 'r') as Hari_297_temp_file, open(inFile1, 'w') as final_file:
        for line in Hari_297_temp_file:
            final_file.write(','.join(line.split(',')[1:]))
except Exception as e:
    logging.error("Error #105d: delete indicator field In {} Failed".format(inFile1))
    #exit(105)

# Check rowcount of the input file
logging.info("Getting the record count of the file")
with open(inFile1, 'r') as f:
    x = sum(1 for _ in f)
logging.info("The record count of the file {} is {}".format(inFile1, x))

if str(trailer) != str(x):
    logging.error("Error: Invalid record count in {inFile1}")
    #exit(2)
else:
    logging.info("Valid record count in Hari _297_client_profile_managed_account.txt")

strRepresentativeMatchInsertQuery = "insert into representative_match values (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10) "
if not helperfunctions1.importTableDataFromCSV(inFile2, strRepresentativeMatchInsertQuery, False, ","):
    logging.error("Error: bcp in for {$inFile2}")
    sys.exit(103)
logging.info("bcp in {} worked.".format(inFile2))


if helperfunctions1.file_exists_case_sensitive_generic(CURDIR,inFile3):
    logging.info(f"File {inFile3} exists")
else:
    logging.info(f"File {inFile3} does not exist. Exiting")
    sys.exit(105)

if not helperfunctions1.copyFile(f"{sftp_in}/{inFile3}", f"./{inFile1}"):
    logging.error(f"Copy of ${inFile1} failed!")
    sys.exit(105)

helperfunctions1.dos2unix(inFile2)
strRepresentativeMatchInsertQuery = "insert intoHari _297_match values (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10) "
if not helperfunctions1.importTableDataFromCSV(inFile2, strRepresentativeMatchInsertQuery, False, "^@"):
    logging.error("Error: bcp in for {$inFile2}")
    sys.exit(103)
logging.info("bcp in {} worked.".format(inFile2))

if helperfunctions1.file_exists_case_sensitive_generic(CURDIR,inFile3):
    logging.info(f"File {inFile3} exists")
else:
    logging.info(f"File {inFile3} does not exist. Exiting")
    sys.exit(105)

if not helperfunctions1.copyFile(f"{sftp_in}/{inFile3}", f"./{inFile3}"):
    logging.error(f"Copy of ${inFile3} failed!")
    sys.exit(105)

helperfunctions1.dos2unix(inFile3)
strBranchQRInsertQuery = "insert into Hari _297_QR values (:1,:2,:3,:4) "
if not helperfunctions1.importTableDataFromCSV('Hari _297_QR.csv', strBranchQRInsertQuery, True, ','):
    logging.error("Error: bcp in for {Hari _297_QR.csv}")
logging.info("bcp in {} worked.".format(inFile3))

sql_to_execute ="""
UPDATE Hari_accnt_input
SET account_id = '00' || SUBSTR(account_id,1,3) || '00000' || SUBSTR(account_id,5,5)"""
if not helperfunctions1.executeSQL(sql_to_execute):
    logging.error("Error in executing sql")
    sys.exit(101)

dropTable('Hari _297_Latest_date')
sql_to_execute="""
CREATE TABLE Hari _297_Latest_date AS
SELECT currency, MAX(fx_rate_date) fx_rate_date
FROM exchange_rate
WHERE fx_rate_date <= (SELECT business_date_current FROM system_control)
GROUP BY currency
"""
if not helperfunctions1.executeSQL(sql_to_execute):
    logging.error("Error in executing sql")

# -- Assuming error_check_sp and related logic is handled differently in Oracle as there's no direct @@error, @@rowcount in Oracle.
dropTable('Hari _297_Latest_rate')
sql_to_execute="""
CREATE TABLE Hari _297_Latest_rate  AS
    SELECT l.currency, e.fx_spot_rate
    FROM Hari _297_Latest_date l JOIN exchange_rate e ON l.currency = e.currency AND l.fx_rate_date = e.fx_rate_date
"""
if not helperfunctions1.executeSQL(sql_to_execute):
    logging.error("Error in executing sql")

sql_to_execute="""
INSERT INTO Hari _297_Latest_rate (currency, fx_spot_rate)
VALUES ('CAD', 1)
"""
#if not helperfunctions.executeSQL(sql_to_execute):
    #   logging.error("Error in executing sql")

sql_to_execute="""
CREATE INDEX idx_curr ON Hari _297_Latest_rate(currency)
"""
if not helperfunctions1.executeSQL(sql_to_execute):
    logging.error("Error in executing sql")

dropTable( 'Hari _297_holdings')
sql_to_execute="""
CREATE TABLE Hari_297_holdings AS
    SELECT DISTINCT a.account_id, tr.ti, tr.currency, tr.curr_mkt_value
    FROM tran_summ tr JOIN Hari_accnt_input a ON a.account_id = tr.account_id
"""
if not helperfunctions1.executeSQL(sql_to_execute):
    logging.error("Error in executing sql")

sql_to_execute="""
CREATE INDEX indx_ti ON Hari _297_holdings(ti)
    """
if not helperfunctions1.executeSQL(sql_to_execute):
    logging.error("Error in executing sql")

# --market value
sql_to_execute="""
UPDATE Hari_297_holdings h
SET h.curr_mkt_value = (SELECT NVL((h.curr_mkt_value * lr.fx_spot_rate),0)
                        FROM Hari _297_Latest_rate lr
                        WHERE h.currency = lr.currency)
"""
if not helperfunctions1.executeSQL(sql_to_execute):
    logging.error("Error in executing sql")
    
# --Total Hari _297_holdings
dropTable( 'Hari_297_hold')
sql_to_execute="""
CREATE TABLE hold  AS
    SELECT account_id, NVL(SUM(curr_mkt_value), 0) AS total_Hari _297_holdings_cdn
    FROM Hari _297_holdings
    GROUP BY account_id
"""
if not helperfunctions1.executeSQL(sql_to_execute):
    logging.error("Error in executing sql")

# --get Total Hari _297_cash Balance for accounts
dropTable( 'Hari _297_cash')
sql_to_execute="""
CREATE TABLE Hari_297_cash  AS
    SELECT a.account_id, NVL(SUM(r.fx_spot_rate * mm.td_net_amt * -1),0) total_Hari _297_cash_cdn
    FROM Hari_accnt_input a, sub_accnt_summ mm, Hari _297_Latest_rate r
    WHERE mm.currency = r.currency AND mm.account_id = a.account_id
    GROUP BY a.account_id
"""
if not helperfunctions1.executeSQL(sql_to_execute):
    logging.error("Error in executing sql")

sql_to_execute="""
ALTER TABLE Hari_accnt_input
ADD total_asset NUMBER(20,2)
"""
if not helperfunctions1.executeSQL(sql_to_execute):
    logging.error("Error in executing sql")

# -- get total asset for accounts into final table
sql_to_execute="""
MERGE
INTO    Hari_accnt_input ci
USING   (
    SELECT ci.account_id, NVL((h.total_Hari _297_holdings_cdn + c.total_Hari _297_cash_cdn),0) AS val
                    FROM Hari_accnt_input ci JOIN hold h  ON ci.ACCOUNT_ID =h.account_id FULL JOIN Hari _297_cash c ON ci.account_id = h.account_id AND ci.account_id = c.account_id
                    WHERE ci.account_id = h.account_id OR ci.account_id = c.account_id
    ) src
ON      (ci.account_id = src.account_id)
WHEN MATCHED THEN UPDATE
SET ci.TOTAL_ASSET  = src.val
"""
if not helperfunctions1.executeSQL(sql_to_execute):
    logging.error("Error in executing sql")

sql_to_execute="""
UPDATE Hari_accnt_input
SET account_id = SUBSTR(account_id,3,3) || '-' || SUBSTR(account_id,11,5)
    """
if not helperfunctions1.executeSQL(sql_to_execute):
    logging.error("Error in executing sql")
    sys.exit(101)

# # Parse commas
strClientAccntInputHari_297_ER0108ParseCommas = """update Hari_accnt_input
                                            set branch_name = replace(branch_name, ',', ' '), 
                                            representative_name = replace(representative_name, ',', ' '),
                                            client_name = replace(client_name, ',', ' ')"""

if not helperfunctions1.executeSQL(strClientAccntInputHari_297_ER0108ParseCommas):
    logging.error("Error in executing sql")
    sys.exit(101)
# logging.info("Create RDBW672 report to store the report on NAS drive")
helperfunctions1.exportTableDataToCSVWithHeader(AST_SCRIPTS + "/" + APFILENAME+'.csv', "select BRANCH,BRANCH_NAME,REPRESENTATIVE,REPRESENTATIVE_NAME,CLIENT_ID,CLIENT_NAME,ACCOUNT_ID,DATE_ADDED,INV_OBJ_INCOME,INV_OBJ_GS,INV_OBJ_GM,INV_OBJ_GL,RISK_TOL_LOW,RISK_TOL_MED,RISK_TOL_HIGH,cast( TOTAL_ASSET as integer) as TOTAL_ASSET from Hari_accnt_input")


strHari_297_QR_Standard =   """
                    create table Hari _297_QR_Standard (
                        reportId int NULL, fckey int NULL, branchCode int NULL, regionCode char(1) NULL, 
                        fielda varchar(100) NULL, fieldb varchar(100) NULL, fieldc varchar(100) NULL, 
                        fieldd varchar(100) NULL, fielde varchar(100) NULL, fieldf varchar(100) NULL, 
                        fieldg varchar(100) NULL, fieldh varchar(100) NULL, fieldi varchar(100) NULL, 
                        fieldj varchar(100) NULL, fieldk varchar(100) NULL, fieldl varchar(100) NULL, 
                        fieldm varchar(100) NULL, fieldn varchar(100) NULL, fieldo varchar(100) NULL, 
                        fieldp varchar(100) NULL, fieldq varchar(100) NULL, fieldr varchar(100) NULL, 
                        fields varchar(100) NULL, fieldt varchar(100) NULL)"""

helperfunctions1.dropCreateTempTables("Hari _297_QR_Standard", strHari_297_QR_Standard)

logging.info("Calling dropCreateTempTables helper function to check, drop and create strHari _297_QR_Standard table is successful.")
logging.info("")

sql_to_execute = """
BEGIN
    EXECUTE IMMEDIATE 'create index ind_id_qrs on Hari _297_QR_Standard(reportId)';
END;"""
if not helperfunctions1.executeSQL(sql_to_execute):
    logging.error("Error in executing sql")
    sys.exit(101)

strHari_297_QR_Date =   """
                    create table Hari _297_QR_Date (reportId int NULL, report_date	varchar(20) NULL)"""

helperfunctions1.dropCreateTempTables("Hari _297_QR_Date", strHari_297_QR_Date)
sql_to_execute = """
BEGIN
    EXECUTE IMMEDIATE 'create index ind_id_qrd on Hari_297_QR_Date(reportId)';
END;"""
if not helperfunctions1.executeSQL(sql_to_execute):
    logging.error("Error in executing sql")
    sys.exit(101)

if not helperfunctions1.file_exists_case_sensitive_generic(f"{CURDIR}","Hari_297_QR_Standard.txt"):
    with open(f"{CURDIR}/Hari_297_QR_Standard.txt", 'w') as f:
        os.chmod(f"{CURDIR}/Hari_297_QR_Standard.txt", 0o777)

if not helperfunctions1.file_exists_case_sensitive_generic(f"{CURDIR}","Hari_297_QR_Date.txt"):
    with open(f"{CURDIR}/Hari_297_QR_Date.txt", 'w') as f:
        os.chmod(f"{CURDIR}/Hari_297_QR_Date.txt", 0o777)

strQRStandardInsertQuery = "insert into Hari _297_QR_Standard values (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15,:16,:17,:18,:19,;20,:21,:22,:23) "
if not helperfunctions1.importTableDataFromCSV(f"{CURDIR}/Hari _297_QR_Standard.txt",strQRStandardInsertQuery, False, "^@"):
    logging.error("Error: bcp in for {DATAPATH}/Hari _297_QR_Standard.txt")
    

logging.info("bcp in {}/Hari _297_QR_Standard.txt worked.".format(CURDIR))

strQRDateInsertQuery = "insert into Hari _297_QR_Date values (:1,:2) "
if not helperfunctions1.importTableDataFromCSV(f"{CURDIR}/Hari _297_QR_Date.txt",strQRDateInsertQuery, False, "^@"):
    logging.error("Error: bcp in for {DATAPATH}/Hari _297_QR_Date.txt")
    sys.exit(103)

logging.info("bcp in {}/Hari _297_QR_Date.txt worked.".format(CURDIR))


dropTable('Hari _297_Hari _297_ER0108_final')
sql_to_execute = """
--Oracle equivalent statements
BEGIN
    EXECUTE IMMEDIATE 'CREATE TABLE Hari _297_Hari _297_ER0108_final  AS SELECT 
        CAST(rm.fckey AS NUMBER(38)) AS fckey,
        CAST(rm.branchCode AS NUMBER(38)) AS branchCode,
        c.branch,
        c.representative,
        c.representative_name,
        TO_CHAR(c.client_id) AS client_id,
        c.client_name,
        c.account_id,
        c.date_added,
        c.inv_obj_income,
        c.inv_obj_gs,
        c.inv_obj_gm,
        c.inv_obj_gl,
        c.risk_tol_low,
        c.risk_tol_med,
        c.risk_tol_high,
        TO_CHAR(c.total_asset) AS total_asset
    FROM Hari_accnt_input c
    LEFT JOINHari _297_match rm ON c.representative = rm.orig_representative
    ORDER BY c.client_id, c.account_id';
EXCEPTION WHEN OTHERS THEN
    IF SQLCODE = -955 THEN
        NULL; -- ignore error if table exists
    ELSE
        RAISE;
    END IF;
END;
"""
if not helperfunctions1.executeSQL(sql_to_execute):
    logging.error("Error in executing sql")
    sys.exit(101)

sql_to_execute="""
UPDATE Hari _297_Hari _297_ER0108_final a
SET a.branchCode = (SELECT CAST(br.branchCode AS NUMBER(38)) 
                    FROM Hari _297_QR br 
                    WHERE a.branch = br.MO_branch)
WHERE a.branchCode IS NULL
"""
if not helperfunctions1.executeSQL(sql_to_execute):
    logging.error("Error in executing sql")
    sys.exit(101)
dropTable('split_codes')

sql_to_execute="""
BEGIN
    EXECUTE IMMEDIATE 'CREATE TABLE Hari _297_split_codes  AS SELECT account_id
    FROM Hari _297_Hari _297_ER0108_final
    GROUP BY account_id
    HAVING COUNT(account_id) > 1';
EXCEPTION WHEN OTHERS THEN
    IF SQLCODE = -955 THEN
        NULL; -- ignore error if table exists
    ELSE
        RAISE;
    END IF;
END;
"""
if not helperfunctions1.executeSQL(sql_to_execute):
    logging.error("Error in executing sql")
    sys.exit(101)

sql_to_execute="""
UPDATE Hari _297_Hari _297_ER0108_final a
SET a.branchCode = NULL
WHERE a.account_id IN (SELECT b.account_id FROM Hari _297_split_codes b)
AND a.fckey NOT IN (
    SELECT MAX(fckey) FROM Hari _297_Hari _297_ER0108_final
    GROUP BY account_id HAVING COUNT(account_id) > 1
)
"""
if not helperfunctions1.executeSQL(sql_to_execute):
    logging.error("Error in executing sql")
    sys.exit(101)

sql_to_execute="""
DELETE FROM Hari _297_QR_Standard
WHERE reportId IN (108)
"""
if not helperfunctions1.executeSQL(sql_to_execute):
    logging.error("Error in executing sql")
    sys.exit(101)
sql_to_execute="""
INSERT INTO Hari _297_QR_Standard
SELECT 108,
    fckey,
    branchCode,
    NULL,
    representative,
    representative_name,
    client_id,
    client_name,
    account_id, 
    date_added,
    inv_obj_income,
    inv_obj_gs,
    inv_obj_gm, 
    inv_obj_gl,
    risk_tol_low,
    risk_tol_med,
    risk_tol_high,
    TO_CHAR(total_asset),
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL
FROM Hari _297_Hari _297_ER0108_final
"""
if not helperfunctions1.executeSQL(sql_to_execute):
    logging.error("Error in executing sql")
    sys.exit(101)
sql_to_execute="""
INSERT INTO Hari _297_QR_Date
SELECT 108, TO_CHAR(SYSDATE, 'MM/DD/YYYY')
FROM dual
"""
if not helperfunctions1.executeSQL(sql_to_execute):
    logging.error("Error in executing sql")
    sys.exit(101)

# # Run Hari _297_QR_Standard_bcp_out.ksh
logging.info("Run Hari _297_QR_Standard_bcp_out.ksh")
logging.info("KSHPATH :  {}".format(os.getenv('KSHPATH')))
logging.info("AST_SCRIPTS :  {}".format(AST_SCRIPTS))

if not helperfunctions1.file_exists_case_sensitive_generic(f"{CURDIR}","Hari _297_QR_Standard.txt"):
    with open(f"{CURDIR}/Hari _297_QR_Standard.txt", 'w') as f:
        os.chmod(f"{CURDIR}/Hari _297_QR_Standard.txt", 0o777)

if not helperfunctions1.file_exists_case_sensitive_generic(f"{CURDIR}","Hari _297_QR_Date.txt"):
    with open(f"{CURDIR}/Hari _297_QR_Date.txt", 'w') as f:
        os.chmod(f"{CURDIR}/Hari _297_QR_Date.txt", 0o777)

logging.info("Begin BCP OUT Hari _297_QR_Standard and Hari _297_QR_Date at {}".format(datetime.now()))

strExportQRStandardQuery = """  select   to_char(REPORTID) || '^', coalesce(to_char(FCKEY), '') || '^',
                            coalesce(to_char(BRANCHCODE), '') || '^', coalesce(to_char(REGIONCODE), '') || '^',
                            coalesce(to_char(FIELDA), '') || '^', coalesce(to_char(FIELDB), '') || '^',
                            coalesce(to_char(FIELDC), '') || '^', coalesce(to_char(FIELDD), '') || '^',
                            coalesce(to_char(FIELDE), '') || '^', coalesce(to_char(FIELDF), '') || '^',
                            coalesce(to_char(FIELDG), '') || '^', coalesce(to_char(FIELDH), '') || '^',
                            coalesce(to_char(FIELDI), '') || '^', coalesce(to_char(FIELDJ), '') || '^',
                            coalesce(to_char(FIELDK), '') || '^', coalesce(to_char(FIELDL), '') || '^',
                            coalesce(to_char(FIELDM), '') || '^', coalesce(to_char(FIELDN), '') || '^',
                            coalesce(to_char(FIELDO), '') || '^', coalesce(to_char(FIELDP), '') || '^',
                            coalesce(to_char(FIELDQ), '') || '^', coalesce(to_char(FIELDR), '') || '^',
                            coalesce(to_char(FIELDS), '') || '^', coalesce(to_char(FIELDT), '')  
                            from Hari _297_QR_Standard """
if not  helperfunctions1.exportTableDataToCSVWithSeparator(f"{CURDIR}/Hari _297_QR_Standard.txt",strExportQRStandardQuery, "@"):
    logging.error("Error: bcp out for $temp_mis..Hari _297_QR_Standard")
    sys.exit(103)

strExportQRDateQuery =  "select to_char(REPORTID) || '^',  REPORT_DATE from Hari _297_QR_Date"
if not helperfunctions1.exportTableDataToCSVWithSeparator(f"{CURDIR}/Hari _297_QR_Date.txt",strExportQRDateQuery, "@"):
    logging.error("Error: bcp out for $temp_mis..Hari _297_QR_Date")
    sys.exit(103)

logging.info("**********************************************************************")
logging.info(" BCP OUT Hari _297_QR_Standard process completed successfully at {}".format(datetime.now()))
logging.info("**********************************************************************")
sql_to_execute = """
BEGIN
EXECUTE IMMEDIATE 'DROP TABLE Hari _297_accnt_input;
EXCEPTION
WHEN OTHERS THEN
    IF SQLCODE != -942 THEN
        RAISE;
    END IF;
END;
"""
if not helperfunctions1.executeSQL(sql_to_execute):
    logging.error("Error in executing sql")
    sys.exit(101)
sql_to_execute="""
BEGIN
EXECUTE IMMEDIATE 'DROP TABLEHari _297_match';
EXCEPTION
WHEN OTHERS THEN
    IF SQLCODE != -942 THEN
        RAISE;
    END IF;
END;
"""
if not helperfunctions1.executeSQL(sql_to_execute):
    logging.error("Error in executing sql")
    sys.exit(101)

APFILENAME2 = "CPMA_Hari _297_ER0108_NL_{}".format(datetime.now().strftime('%Y%m%d'))

# # Convert csv file to pipe delimited and move to out_qr_nas directory
logging.info("Convert csv file to pipe delimited.")
with open(os.path.join(AST_SCRIPTS, '{}.csv'.format(APFILENAME)), 'r') as csv_file, open(AST_SCRIPTS+'/sftp/outgoing/out_ext/{}.txt'.format(APFILENAME2), 'w') as pipe_file:
    for line in csv_file:
        pipe_file.write(line.replace(',', '|'))

# # Removing all the temporary files
logging.info("Removing all the temporary files")
try:
    os.remove(os.path.join(AST_SCRIPTS, RDB_FOLDER, 'Hari _297_client_profile_managed_account.txt'))
    os.remove(os.path.join(AST_SCRIPTS, RDB_FOLDER, 'Hari _297_client_profile_managed_account_new.txt'))
    os.remove(os.path.join(AST_SCRIPTS, RDB_FOLDER, 'Hari _297_QR.csv'))
    os.remove(os.path.join(AST_SCRIPTS, RDB_FOLDER, 'Hari _297_match.csv'))
    os.remove(os.path.join(AST_SCRIPTS, RDB_FOLDER, 'Hari _297_temp_file.txt'))
    os.remove(os.path.join(AST_SCRIPTS, RDB_FOLDER, 'Hari _297_ER0108_date.txt'))
except Exception as e:
    logging.error(" - ** ERROR: Copy of {}.csv failed!".format(APFILENAME))
    exit(1)




