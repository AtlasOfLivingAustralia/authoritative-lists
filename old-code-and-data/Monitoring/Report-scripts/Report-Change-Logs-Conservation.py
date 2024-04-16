#%% 
# Change Log Report - Manual List check 
#  
# **Instructions** 
#  
# 1. Load the lists above into the lists-test tool 
# 2. Check the list name matching score and the text appearance on species pages 
# 3. Unskip the below code and Run the reports below to compare to production. Send the changelog.csv to check.
#    Correct any issues. 
# 4. Save the production list into the `historical lists` directory by uncommenting the code section below. 
# 5. Load the lists into production 
#  
# Compare Test and Production data for: 
#  
#     1. Conservation lists 
#
# Output change log files to : ..\authoritative-lists\analysis\change-log 
#  
#
import datetime
import os
import sys

projectDir = "/Users/oco115/PycharmProjects/authoritative-lists/"
changeDir = "Monitoring/Change-logs/"
sys.path.append(os.path.abspath(projectDir + "source-code/includes"))
monthStr = datetime.datetime.now().strftime('%Y%m%d')
import list_functions as lf

###############################################################################################################

# Conservation Lists 
#
ltype = "C"

# ACT Conservation
print('ACT conservation')
filename = "ACT-conservation.csv"
testdr = "dr649"
proddr = "dr649"
changelist = lf.get_changelist(testdr, proddr, ltype)
changelist.to_csv(projectDir + changeDir + monthStr + "-" + filename, encoding="UTF-8", index=False)
print('Finished ACT conservation')

# EPBC Conservation
print('EPBC conservation')
filename = "EPBC-conservation.csv"
testdr = "dr656"
proddr = "dr656"
changelist = lf.get_changelist(testdr, proddr, ltype)
changelist.to_csv(projectDir + changeDir + monthStr + "-" + filename, encoding="UTF-8", index=False)
print('Finished EPBC conservation')

# NSW conservation
print('NSW conservation')
filename = "NSW-conservation.csv"
testdr = "dr650"
proddr = "dr650"
changelist = lf.get_changelist(testdr, proddr, ltype)
changelist.to_csv(projectDir + changeDir + monthStr + "-" + filename, encoding="UTF-8", index=False)
print('Finished NSW conservation')

# NT Conservation
print('NT conservation')
filename = "NT-conservation.csv"
testdr = "dr651"
proddr = "dr651"
changelist = lf.get_changelist(testdr, proddr, ltype)
changelist.to_csv(projectDir + changeDir + monthStr + "-" + filename, encoding="UTF-8", index=False)
print('Finished NT conservation')

# Qld Conservation
print('QLD conservation')
filename = "QLD-conservation.csv"
testdr = "dr652"
proddr = "dr652"
changelist = lf.get_changelist(testdr, proddr, ltype)
changelist.to_csv(projectDir + changeDir + monthStr + "-" + filename, encoding="UTF-8", index=False)
print('Finished QLD conservation')

# SA Conservation
print('SA conservation')
filename = "SA-conservation.csv"
testdr = "dr653"
proddr = "dr653"
changelist = lf.get_changelist(testdr, proddr, ltype)
changelist.to_csv(projectDir + changeDir + monthStr + "-" + filename, encoding="UTF-8", index=False)
print('Finished SA conservation')

# TAS Conservation
print('TAS conservation')
filename = "TAS-conservation.csv"
testdr = "dr654"
proddr = "dr654"
changelist = lf.get_changelist(testdr, proddr, ltype)
changelist.to_csv(projectDir + changeDir + monthStr + "-" + filename, encoding="UTF-8", index=False)
print('Finished TAS conservation')

# VIC Conservation
print('VIC conservation')
filename = "VIC-conservation.csv"
testdr = "dr655"
proddr = "dr655"
changelist = lf.get_changelist(testdr, proddr, ltype)
changelist.to_csv(projectDir + changeDir + monthStr + "-" + filename, encoding="UTF-8", index=False)
print('Finished VIC conservation')

# WA Conservation
print('WA conservation')
filename = "WA-conservation.csv"
testdr = "dr2201"
proddr = "dr2201"
changelist = lf.get_changelist(testdr, proddr, ltype)
changelist.to_csv(projectDir + changeDir + monthStr + "-" + filename, encoding="UTF-8", index=False)
print('Finished WA conservation')

###############################################################################################################
# Download Production list to Historical Lists directory
#
# Conservation lists

drList = {"ACT": "dr649", "NSW": "dr650", "NT": "dr651", "QLD": "dr652", "SA": "dr653", "TAS": "dr654",
          "VIC": "dr655", "EPBC": "dr656", "WA": "dr2201"}

for state, dr in drList.items():
    filename = state + "-" + dr + "-conservation.csv"
    print(dr)
    prodListUrl = "https://lists.ala.org.au/ws/speciesListItems/" + dr + "?max=10000&includeKVP=true"
    prodList = lf.download_ala_list(prodListUrl)  # save the prod list to the historical lists directory
    prodList = lf.kvp_to_columns(prodList)
    prodList.to_csv(projectDir + "historical-lists/conservation/" + filename, encoding="UTF-8", index=False)
print('Finished downloading conservation historical list')
