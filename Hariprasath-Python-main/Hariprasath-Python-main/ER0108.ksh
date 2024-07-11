#!/bin/ksh
#--------------------------------------------------------------------------------
# PROGRAM:      RDBW672
# CREATED BY:	Mandy (Mandeep Kaur)
# CREATION DATE:	November 9, 2011
# REQUESTOR:	Sabrina Tam 
# FREQUENCY:	daily
# INTAKE:       BT2015-116
# PURPOSE:     	The report will list all clients where the accounts are being managed at the portfolio level.           
#               The report extract is based on the input file provided by GOW team
# INPUT FILE USED:	client_profile_managed_account.txt
#--------------------------------------------------------------------------------
# environment setting
#--------------------------------------------------------------------------------

cd `dirname $0`
CURDIR=$PWD
WGDIR=`dirname $CURDIR`
REPTDIR=`dirname $WGDIR`
AST_SCRIPTS=$WGDIR

export CURDIR
export WGDIR
export REPTDIR
export AST_SCRIPTS


. $WGDIR/rptProfile
. /opt/work_12/reports/QuickFiles/qfProfile

RDB_FOLDER=RDBW672
APFILENAME=RDBW672_`date +%Y%m%d`

cd $AST_SCRIPTS/$RDB_FOLDER
LOG=$AST_SCRIPTS/$RDB_FOLDER/`basename $0`.log
export LOG

#Process name variable
PROCESS=`basename $0 | cut -f1 -d'.'`
echo $PROCESS

inFile=client_profile_managed_account.txt
inFile1=client_profile_managed_account_new.txt
inFile2=representative_match.csv
inFile3=branch_QR.csv


#----------------------------------------------------------------------------
# Beginning of program
#----------------------------------------------------------------------------
echo "%TStarted ER0108 reports at `date`" > $LOG
#----------------------------------------------------------------------------


echo "Drop table in $temp_mis at `date`" >> $LOG
isql -U$AST_DBUSER -P`cat $PASSWDFILE` -S$DSQUERY -w256 -e<<%EOF >> $LOG

use $temp_mis
go

if exists (select name from $temp_mis..sysobjects where name = "client_accnt_input" and type = "U")
     drop table $temp_mis..client_accnt_input
go

if exists (select name from $temp_mis..sysobjects where name = "representative_match" and type = "U")
     drop table $temp_mis..representative_match
go

if exists (select name from $temp_mis..sysobjects where name = "branch_QR" and type = "U")
     drop table $temp_mis..branch_QR
go

create table branch_QR
        (
        MO_branch varchar(50) null,
        branchCode varchar(50) null,
        MO_branch_name varchar(500) null
        )
GO

create table $temp_mis..client_accnt_input (
	branch varchar(3) null,
	branch_name varchar(30) null,
	representative varchar(3) null,
	representative_name varchar(50) null,
	client_id int null,
	client_name varchar(100) null,
	account_id varchar(20) null,
	date_added varchar(8) null,
	inv_obj_income varchar(10) null,
	inv_obj_gs varchar(10) null,
	inv_obj_gm varchar(10) null,
	inv_obj_gl varchar(10) null,
	risk_tol_low varchar(10) null,
	risk_tol_med varchar(10) null,
	risk_tol_high varchar(10) null) 
go

exec $PERM_DATABASE..error_check_sp @@error, @@rowcount, $PROCESS, 1,'$temp_mis..client_accnt_input create statement'
go

create table tempdbmis..representative_match (
	orig_representative varchar(6) null,
	representative varchar(6) null,
	fckey varchar(6) null,
	orig_branch varchar(8) null,
	branch varchar(100) null,
	branchCode varchar(100) null,
	region varchar(100) null,
	owner_domain varchar(100) null,
	owner_id varchar(100) null,
	folder_id varchar(255) null)
go

exec $PERM_DATABASE..error_check_sp @@error, @@rowcount, $PROCESS, 1,'$temp_mis..representative_match create statement'
go

%EOF

# Check for successful execution of SQL stored procedure
if (( $? )) ;then exit 101; fi

# Check log file for error messages
echo "Checking 1 LOG file for errors on `date`" >> $LOG
if (grep "Msg 999998" $LOG); then
		echo "Error Code 101 on `date`" >> $LOG
		echo >> $LOG
		exit 101
	else 
		echo "NO ERROR FOUND" >> $LOG
	fi


if (( $? ))
then 
echo "Error Code 101 on `date`" >> $LOG
echo >> $LOG
exit 101
fi

#----------------------------------------------------------------------
# BCP in input files 
#----------------------------------------------------------------------

echo "Get ${inFile} from ${sftp_in}. $(date)"           >> $LOG

if [ -f ${sftp_in}/${inFile} ];
then
        echo "File $inFile exists." >> $LOG

else
        echo "File $inFile does not exist. Exiting"  >> $LOG
        exit 105
fi


cp ${sftp_in}/${inFile} ./${inFile}                     >> $LOG 

if (( $? )); then
        echo " - ** ERROR: Copy of ${inFile} failed!"   >> $LOG
        exit ${err_ksh}
fi

dos2unix -850 ${inFile} ${inFile}    
curr_date=`date +%Y%m%d`
echo "Current business date is ${curr_date} \n" >> $LOG

# check the date in the file. It should be the current business date.
echo "Getting the header date in the file \n" >> $LOG
head -1 $inFile > ER0108_date.txt
header=`cut -f2 -d '|' ER0108_date.txt`
echo "The header date of the file is ${header} \n" >> $LOG

if [ $header -ne $curr_date ]
then

        echo "Error:Invalid input file as it doesn't contain the current business date in the file header \n" >> $LOG
        exit 2
else
        echo "The input file is correct and contains the current business date \n" >> $LOG
fi  

#get record count in trailer record
echo "Getting the record count in the trailer of the file  \n" >> $LOG
trailer=`tail -1 $inFile|cut -f2 -d '|'`
echo "The count in the trailer is ${trailer}  \n" >> $LOG 

# Remove header and footer from input files
echo "Deleting header and trailer from client_profile_managed_account.txt at `date` \n" >> $LOG
sed -e '1,2d' -e '$d' $inFile > temp_file.txt
if [ $? -ne 0 ]; then
   echo "Error #105d: delete header and footer In ${inFile} Failed \n" >> $LOG
   exit 105
fi

# Removing the first column from the input file which is the record indicator 
echo "Deleting the indicator field from the temp file  \n" >> $LOG
cut -d '|' -f 2- temp_file.txt > $inFile1
if [ $? -ne 0 ]; then
   echo "Error #105d: delete indicator field In ${inFile1} Failed  \n" >> $LOG
   exit 105
fi
 
#---check rowcount of the input file
echo "Getting the record count of the file \n" >> $LOG
x=`wc -l < ${inFile1}`

echo "The record count of the file ${inFile1} is $x \n" >> $LOG

if [ $trailer -ne $x ]
then

        echo "Error:Invalid record count in client_profile_managed_account.txt at `date`" >> $LOG
        exit 2
else
        echo "Valid record count in client_profile_managed_account.txt at `date`" >> $MSG
fi


bcp $temp_mis..client_accnt_input in $inFile1 -c -t '|' -U$AST_DBUSER -P`cat $PASSWDFILE` -S$DSQUERY >> $LOG

if [ $? -ne 0 ]
then
        echo "Error # 103a: bcp in $inFile1 at `date`" >> $LOG
        exit 103
fi
echo "bcp in $inFile1 at `date` worked.\n" >> $LOG


echo "Get ${inFile2} from ${sftp_in}. $(date)"           >> $LOG

if [ -f ${sftp_in}/${inFile2} ];
then
        echo "File $inFile2 exists." >> $LOG

else
        echo "File $inFile2 does not exist. Exiting"  >> $LOG
        exit 0
fi


cp ${sftp_in}/${inFile2} ./${inFile2}                     >> $LOG 2>&1

if (( $? )); then
        echo " - ** ERROR: Copy of ${inFile2} failed!"   >> $LOG
        exit ${err_ksh}
fi

dos2unix -850 ${inFile2} ${inFile2}

bcp $temp_mis..representative_match in $inFile2 -c -t '^@' -U$AST_DBUSER -P`cat $PASSWDFILE` -S$DSQUERY >> $LOG

if [ $? -ne 0 ]
then
        echo "Error # 103a: bcp in $inFile2 at `date`" >> $LOG
        exit 103
fi
echo "bcp in $inFile2 at `date` worked.\n" >> $LOG

echo "Get ${inFile3} from ${sftp_in}. $(date)"           >> $LOG

if [ -f ${sftp_in}/${inFile3} ];
then
        echo "File $inFile3 exists." >> $LOG

else
        echo "File $inFile3 does not exist. Exiting"  >> $LOG
        exit 0
fi


cp ${sftp_in}/${inFile3} ./${inFile3}                     >> $LOG 2>&1

if (( $? )); then
        echo " - ** ERROR: Copy of ${inFile3} failed!"   >> $LOG
        exit ${err_ksh}
fi

dos2unix -850 ${inFile3} ${inFile3}

bcp $temp_mis..branch_QR in branch_QR.csv -c -t ',' -F 2 -Jiso_1 -U$AST_DBUSER -P`cat $PASSWDFILE` -S$DSQUERY >> $LOG

if [ $? -ne 0 ]
then 
        echo "Error # 103a: bcp in $inFile3 at `date`" >> $LOG
        exit 103
fi
echo "bcp in $inFile3 at `date` worked.\n" >> $LOG

#----------------------------------------------------------------------

#-- calculate the assets of the accounts

isql -U$AST_DBUSER -P`cat $PASSWDFILE` -S$DSQUERY -w256 -e<<%EOF >> $LOG

go

update $temp_mis..client_accnt_input
set account_id = '00' + substring(account_id,1,3) + '00000' +substring(account_id,5,5)
go


--update $temp_mis..client_accnt_input
--set 
--branch_name = str_replace(branch_name,',',''),
--representative_name = str_replace(representative_name,',',''),
--client_name = str_replace(client_name,',','')
--go

---------------
--calculate holdings+cash = assets
---------------
--- Get latest exchange rates for converting to CDN

DECLARE @run_date DATETIME
SELECT @run_date = business_date_current
FROM system_control

SELECT   currency, max(fx_rate_date) fx_rate_date
INTO    #latest_date
FROM    exchange_rate
WHERE    fx_rate_date <= @run_date
GROUP BY currency
GO

exec $PERM_DATABASE..error_check_sp @@error, @@rowcount, $PROCESS, 1,'#latest_date select statement'
go

SELECT  l.currency, e.fx_spot_rate
INTO   #latest_rate
FROM   #latest_date l, exchange_rate e
WHERE   l.currency = e.currency
AND     l.fx_rate_date = e.fx_rate_date
GO

exec $PERM_DATABASE..error_check_sp @@error, @@rowcount, $PROCESS, 1,'#latest_rate select statement'
go

INSERT INTO #latest_rate
SELECT 'CAD', 1
GO

exec $PERM_DATABASE..error_check_sp @@error, @@rowcount, $PROCESS, 1,'#latest_rate insert statement'
go

CREATE INDEX idx_curr ON #latest_rate(currency)
GO

exec $PERM_DATABASE..error_check_sp @@error, @@rowcount, $PROCESS, 1,'#latest_rate create index statement'
go

---------------
-- Get all holdings
---------------
SELECT  distinct a.account_id,
                tr.ti,
                tr.currency,
                tr.curr_mkt_value
INTO    #holdings
FROM    ASTRADE66..tran_summ tr, $temp_mis..client_accnt_input a
WHERE   a.account_id = tr.account_id
GO

exec $PERM_DATABASE..error_check_sp @@error, @@rowcount, $PROCESS, 1,'#holdings select statement'
go

CREATE index indx_ti on #holdings(ti)
go

exec $PERM_DATABASE..error_check_sp @@error, @@rowcount, $PROCESS, 1,'#holdings create index statement'
go

--market value
UPDATE  #holdings
SET     a.curr_mkt_value = CONVERT(NUMERIC(20,2), ISNULL((a.curr_mkt_value * b.fx_spot_rate),0))
FROM    #holdings a,
                #latest_rate  b
WHERE   a.currency = b.currency
go

exec $PERM_DATABASE..error_check_sp @@error, @@rowcount, $PROCESS, 1,'#holdings update statement'
go

--Total holdings
SELECT  account_id,
                CONVERT(NUMERIC(20,2), ISNULL(SUM(curr_mkt_value), 0)) AS total_holdings_cdn
INTO    #hold
FROM    #holdings
GROUP   BY account_id
go

exec $PERM_DATABASE..error_check_sp @@error, @@rowcount, $PROCESS, 1,'#hold select statement'
go

--get Total Cash Balance for accounts

SELECT    a.account_id,
         isnull(sum(r.fx_spot_rate * mm.td_net_amt * -1),0) total_cash_cdn
INTO    #cash
FROM    $temp_mis..client_accnt_input a,
        sub_accnt_summ mm,
        #latest_rate r
WHERE    mm.currency = r.currency
  AND    mm.account_id = a.account_id
GROUP BY a.account_id
go

exec $PERM_DATABASE..error_check_sp @@error, @@rowcount, $PROCESS, 1,'$temp_mis..cash select statement'
go


ALTER table $temp_mis..client_accnt_input
ADD total_asset numeric(20,2) null

exec $PERM_DATABASE..error_check_sp @@error, @@rowcount, $PROCESS, 1,'$temp_mis..cash update statement'
go

-- get total asset for accounts into final table
update $temp_mis..client_accnt_input
set total_asset = CONVERT(NUMERIC(20,2), ISNULL((total_cash_cdn + total_holdings_cdn),0))
FROM $temp_mis..client_accnt_input a, #hold b, #cash c
where a.account_id *= b.account_id
and a.account_id *= c.account_id
go

exec $PERM_DATABASE..error_check_sp @@error, @@rowcount, $PROCESS, 1,'$temp_mis..cash update statement'
go

update $temp_mis..client_accnt_input
set account_id =  substring(account_id,3,3) + '-' +substring(account_id,11,5)
go

exec $PERM_DATABASE..error_check_sp @@error, @@rowcount, $PROCESS, 1,'$temp_mis..cash update statement'
go

%EOF

#----------------------------------------------------------------------
# Parse commas
$AST_SCRIPTS/parseCommas.ksh $temp_mis..client_accnt_input branch_name >> $LOG
$AST_SCRIPTS/parseCommas.ksh $temp_mis..client_accnt_input representative_name >> $LOG
$AST_SCRIPTS/parseCommas.ksh $temp_mis..client_accnt_input client_name >> $LOG

echo "Create RDBW672 report to store the report on NAS drive" >> $LOG
$AST_SCRIPTS/header_mis.ksh client_accnt_input $APFILENAME >> $LOG

#Check for successful export of table
if (( $? ))
then
   # Check for space problem, then bcp problem
   tmp=`df -bk . | awk '{print $5}' | tail -1 | cut -f1 -d%` >> $LOG
   if [[ $tmp == 100 ]]
   then
      echo "Error Code 104 on RDBW672 on `date` \n" >> $LOG
      exit 104
   else
      echo "Error Code 103 on RDBW672 on `date` \n" >> $LOG
      exit 103
   fi
else
   echo "BCP of $APFILENAME was successful on `date` \n" >> $LOG
fi


#----------------------
echo "Create branch level reports" >> $LOG
#----------------------

echo "Recreate the QR_Standard AND QR_Date tables" >> $LOG
$KSHPATH/QR_Standard_create.ksh  >> $LOG
if (( $? ))
then
	echo "Errors in QR_Standard_create.ksh. Please refer to corresponding log file." >> $LOG
	exit 105b
fi
echo "QR_Standard AND QR_Date tables successfully created " >> $LOG

echo "Load QR_Standard and QR_Date tables" >> $LOG
#drop all tables
isql -U$AST_DBUSER -P`cat $PASSWDFILE` -S$DSQUERY -w256 -e<<%EOF >> $LOG
go

Select  convert(int, rm.fckey) as fckey,
        convert(int, rm.branchCode) as branchCode,
        c.branch,
        c.representative,
        c.representative_name,
        convert(varchar,c.client_id) as client_id,
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
        convert(varchar,c.total_asset) as total_asset
into #ER0108_final
from $temp_mis..client_accnt_input c,
     $temp_mis..representative_match rm
where c.representative *= rm.orig_representative
order by c.client_id, c.account_id
go

Update #ER0108_final
set a.branchCode = convert(int,br.branchCode)
from #ER0108_final a, $temp_mis..branch_QR br
where a.branch = br.MO_branch
and a.branchCode = NULL
go

select account_id
into #split_codes
from #ER0108_final
group by account_id
having count(account_id) > 1
go

update #ER0108_final
set branchCode = NULL
from #ER0108_final a join #split_codes b on a.account_id = b.account_id
where fckey not in (select max(fckey) from #ER0108_final
                             group by account_id having count(account_id) > 1)
go


-- Insert into QR_Standard table 
DELETE 	$temp_mis..QR_Standard
WHERE	reportId in (108)
go

insert into $temp_mis..QR_Standard
select 108,
       fckey,
       branchCode,
       NULL,
       c.representative,
       c.representative_name,
       c.client_id,
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
       convert(varchar,c.total_asset),
       NULL,
       NULL,
       NULL,
       NULL,
       NULL,
       NULL
from #ER0108_final c
go
		
INSERT INTO tempdbmis..QR_Date
SELECT 108, convert(char(10), business_date_current, 101)
FROM system_control
GO

%EOF

echo "Run QR_Standard_bcp_out.ksh" >> $LOG
echo "KSHPATH :  $KSHPATH" >> $LOG
echo "AST_SCRIPTS :  $AST_SCRIPTS" >> $LOG


cd $KSHPATH >> $LOG
QR_Standard_bcp_out.ksh  >> $LOG
if (( $? ))
then 
	echo "Errors in QR_Standard_bcp_out.ksh. Please refer to corresponding log file." >> $LOG
	exit 105c
fi
echo " " >> $LOG

echo "Drop tables" >> $LOG
#drop all tables
isql -U$AST_DBUSER -P`cat $PASSWDFILE` -S$DSQUERY -w256 -e<<%EOF >> $LOG

use $temp_mis
go

if exists (select name from $temp_mis..sysobjects where name = "client_accnt_input" and type = "U")
     drop table $temp_mis..client_accnt_input
go

if exists (select name from $temp_mis..sysobjects where name = "representative_match" and type = "U")
     drop table $temp_mis..representative_match
go

--if exists (select name from $temp_mis..sysobjects where name = "branch_QR" and type = "U")
 --    drop table $temp_mis..branch_QR
go

%EOF

# SFTP outgoing changes
#----------------------------------------------------------------------

#       tag_add_hdr_trl

#Date_SQL=$(isql -U$AST_DBUSER -P`cat $PASSWDFILE` -S$DSQUERY -w256 -e<<%EOF
#go
#select str_replace(convert(char(10),convert(date,business_date_current),102),'.', '-') from ASTRADE66..system_control
#go
#%EOF
#)

#Business_Date=`echo $Date_SQL | cut -c113-123`
#Business_Date=`echo $Date_SQL`
#APFILENAME2=CPMA_ER0108_NL_$Business_Date
#echo "Date_SQL: '$Date_SQL'" >> $LOG
APFILENAME2=CPMA_ER0108_NL_`date +%Y%m%d`

#=========================================================================================
#convert csv file to pipe delimited and move to out_qr_nas directory
echo "Convert csv file to pipe delimited. " >> $LOG

#COPY FILE INTO UPLOADING DIRECTORY - BY TARAK  
#cp $AST_SCRIPTS/$APFILENAME.csv /opt/work_12/reports/sftp/outgoing/out_ext/$APFILENAME.csv
#mv /opt/work_12/reports/sftp/outgoing/out_ext/$APFILENAME.csv /opt/work_12/reports/sftp/outgoing/out_ext/$APFILENAME2.csv

sed -e 's/,/|/g' $AST_SCRIPTS/$APFILENAME.csv >> /opt/work_12/reports/sftp/outgoing/out_ext/$APFILENAME2.txt
#sed -e '1 s/,/|/g'  $AST_SCRIPTS/$APFILENAME.csv >> /opt/work_12/reports/sftp/outgoing/out_ext/$APFILENAME2.txt
#sed = /opt/work_12/reports/sftp/outgoing/out_ext/$APFILENAME2.txt | sed '2,$ s/,/|/g'

#=========================================================================================

#move original csv file to out_ext directory
mv $AST_SCRIPTS/$APFILENAME.csv ${sftp_out_qr_nas}/${APFILENAME}.csv >> $LOG 2>&1

if (( $? )); then
        echo " - ** ERROR: Copy of ${APFILENAME}.csv failed!" >> $LOG
        exit ${err_ksh}
fi

echo "File ${APFILENAME}.csv successfully copied." >> $LOG

# Removing all the temporary files
echo "Removing all the temporary files" >> $LOG
rm $AST_SCRIPTS/$RDB_FOLDER/client_profile_managed_account.txt
rm $AST_SCRIPTS/$RDB_FOLDER/client_profile_managed_account_new.txt
rm $AST_SCRIPTS/$RDB_FOLDER/branch_QR.csv
rm $AST_SCRIPTS/$RDB_FOLDER/representative_match.csv
rm $AST_SCRIPTS/$RDB_FOLDER/temp_file.txt
rm $AST_SCRIPTS/$RDB_FOLDER/ER0108_date.txt

if (( $? )); then
        echo " - ** ERROR: Copy of ${APFILENAME}.csv failed!" >> $LOG
        exit ${err_ksh}
fi

# Check log file for error messages
echo "Checking 3 LOG file for errors on `date`" >> $LOG
if (grep "Msg 999998" $LOG); then
		echo "Error Code 101 on `date`" >> $LOG
		echo >> $LOG
		exit 101
	else 
		echo "NO ERROR FOUND" >> $LOG
	fi


if (( $? ))
then 
echo "Error Code 101 on `date`" >> $LOG
echo >> $LOG
exit 101
fi

echo "%Tfinished ER0108.ksh at `date`" >> $LOG

echo "******************************************************" >> $LOG
echo "*          ER0108.ksh finished succesfully!              *" >> $LOG
echo "******************************************************" >> $LOG
exit 0


