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
#     1. Sensitive lists
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
# # Sensitive  Lists
#
ltype = "S"
# # ACT Sensitive
# print('ACT sensitive')
# filename = "ACT-sensitive.csv"
# testdr = "dr2627"
# proddr = "dr2627"
# changelist = lf.get_changelist(testdr, proddr, ltype)
# changelist.to_csv(projectDir + changeDir + monthStr + "-" + filename, encoding="UTF-8", index=False)
# print('Finished ACT sensitive')

# NSW Sensitive
print('NSW sensitive')
filename = "NSW-sensitive.csv"
testdr = "dr18457"
proddr = "dr487"
changelist = lf.get_changelist(testdr, proddr, ltype)
changelist.to_csv(projectDir + changeDir + monthStr + "-" + filename, encoding="UTF-8", index=False)
print('Finished NSW sensitive')

# NT Sensitive
print('NT sensitive')
filename = "NT-sensitive.csv"
testdr = "dr18690"
proddr = "dr492"
changelist = lf.get_changelist(testdr, proddr, ltype)
changelist.to_csv(projectDir + changeDir + monthStr + "-" + filename, encoding="UTF-8", index=False)
print('Finished NT sensitive')

# Qld Sensitive
print('QLD sensitive')
filename = "QLD-sensitive.csv"
testdr = "dr18404"
proddr = "dr493"
changelist = lf.get_changelist(testdr, proddr, ltype)
changelist.to_csv(projectDir + changeDir + monthStr + "-" + filename, encoding="UTF-8", index=False)
print('Finished QLD sensitive')

# SA Sensitive
print('SA sensitive')
filename = "SA-sensitive.csv"
testdr = "dr18706"
proddr = "dr884"
changelist = lf.get_changelist(testdr, proddr, ltype)
changelist.to_csv(projectDir + changeDir + monthStr + "-" + filename, encoding="UTF-8", index=False)
print('Finished SA sensitive')

# TAS Sensitive - not currently in Test
print('TAS sensitive')
filename = "TAS-sensitive.csv"
testdr = "dr18692"
proddr = "dr491"
changelist = lf.get_changelist(testdr, proddr, ltype)
changelist.to_csv(projectDir + changeDir + monthStr + "-" + filename, encoding="UTF-8", index=False)
print('Finished TAS sensitive')

# VIC Sensitive
print('VIC sensitive')
filename = "VIC-sensitive.csv"
testdr = "dr18669"
proddr = "dr490"
changelist = lf.get_changelist(testdr, proddr, ltype)
changelist.to_csv(projectDir + changeDir + monthStr + "-" + filename, encoding="UTF-8", index=False)
print('Finished VIC sensitive')

# WA Sensitive
print('WA sensitive')
filename = "WA-sensitive.csv"
testdr = "dr18406"
proddr = "dr467"
changelist = lf.get_changelist(testdr, proddr, ltype)
changelist.to_csv(projectDir + changeDir + monthStr + "-" + filename, encoding="UTF-8", index=False)
print('Finished WA sensitive')

###############################################################################################################
# Download Production list to Historical Lists directory 
#
# Sensitive Lists
# drList = {"TAS": "dr491"}  # Notebook is dying on empty kvpValues when in Jupyter notebook. runs fine in py script
drList = {"ACT":"dr2627", "NSW":"dr487", "NT":"dr492", "QLD":"dr493", "SA":"dr884","TAS":"dr491",
"VIC":"dr490", "WA":"dr467"}
# drList = {"ACT":"dr2627", "NSW":"dr487", "NT":"dr492", "QLD":"dr493", "SA":"dr884", "VIC":"dr490", "WA":"dr467"}
for state, dr in drList.items():
    filename = state + "-" + dr + "-sensitive.csv"
    print(dr)
    prodListUrl = "https://lists.ala.org.au/ws/speciesListItems/" + dr + "?max=10000&includeKVP=true"
    prodList = lf.download_ala_list(prodListUrl)  # save the prod list to the historical lists directory
    prodList = lf.kvp_to_columns(prodList)
    prodList.to_csv(projectDir + "historical-lists/sensitive/" + filename, encoding="UTF-8", index=False)
print('Finished downloading sensitive historical list')
