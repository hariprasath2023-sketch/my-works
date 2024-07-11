import os
import logging
import datetime
import helperfunctions1 as helperfunctions
import sys
os.chdir(os.path.dirname(__file__))
currentdir=os.getcwd()
wgdir=os.path.dirname(currentdir)
enddir=os.path.dirname(wgdir)
AST_SCRIPTS = enddir
file2= 'demo.txt'
file3='demo2.txt'

os.environ[' currentdir'] = currentdir
os.environ['wgdir'] = wgdir
os.environ['endir'] = enddir
os.environ['AST_SCRIPTS'] = AST_SCRIPTS
process=os.path.basename(__file__)

tota_recs=0
act_res=0
header_found=0

logging.info("Process")

month=datetime.datetime.now().month
year=datetime.datetime.now().year
lastmonth=month-1
if lastmonth==0:
    lastmonth=12
    year-=1
if lastmonth<=9:
    lastmonth="0"+str(lastmonth)

file=f'cibc{year}-{lastmonth}'
file1=file

if not helperfunctions.file_exists_case_sensitive_generic(file2,currentdir):
    logging.info(f"**	-	ERROR : input file <{file3}> - not found .... exiting")
    # sys.exit(105)



logging.info(" - input file found - processing")

if not helperfunctions.copyFile(file2, file3):
    logging.error(f"**	-	ERROR : cp file <{file}> to local directory failed ...exiting")
    sys.exit(102)

if not os.path.isfile(file):
    logging.error(f"** - ERROR : input file <{file}> - not found .... exiting")
    exit(105)

with open(file, 'r') as f:
    hdr_found = 'HEADER' in f.readline()
    print(hdr_found)

if not hdr_found:
    logging.error(f"** - ERROR : Header record missing from file <{file}> ...exiting")
    exit(105)
logging.info(f" - Header record found in file <{file}> ...")