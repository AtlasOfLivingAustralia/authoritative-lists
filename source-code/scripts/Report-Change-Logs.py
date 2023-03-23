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
#     2. Sensitive lists 
#  
# Output change log files to : ..\authoritative-lists\analysis\change-log 
#  
#
import datetime
import os
import sys
import list_functions as lf

projectdir = "/Users/oco115/PycharmProjects/authoritative-lists/"
changedir = projectdir + "analysis/change-log/"
sys.path.append(os.path.abspath(projectdir + "source-code/includes"))
monthStr = datetime.datetime.now().strftime('%Y%m%d')


###############################################################################################################

# Conservation Lists 
#
ltype = "C"

# ACT Conservation
filename = "ACT-conservation.csv"
testdr = "dr649"
proddr = "dr649"
changelist = lf.get_changelist(testdr, proddr, ltype)
changelist.to_csv(projectdir + changedir + monthStr + "-" + filename, encoding="UTF-8", index=False)

# EPBC Conservation
filename = "EPBC-conservation.csv"
testdr = "dr656"
proddr = "dr656"
changelist = lf.get_changelist(testdr, proddr, ltype)
changelist.to_csv(projectdir + changedir + monthStr + "-" + filename, encoding="UTF-8", index=False)

# NSW conservation
filename = "NSW-conservation.csv"
testdr = "dr650"
proddr = "dr650"
changelist = lf.get_changelist(testdr, proddr, ltype)
changelist.to_csv(projectdir + changedir + monthStr + "-" + filename, encoding="UTF-8", index=False)

# NT Conservation
filename = "NT-conservation.csv"
testdr = "dr651"
proddr = "dr651"
changelist = lf.get_changelist(testdr, proddr, ltype)
changelist.to_csv(projectdir + changedir + monthStr + "-" + filename, encoding="UTF-8", index=False)

# Qld Conservation
filename = "QLD-conservation.csv"
testdr = "dr652"
proddr = "dr652"
changelist = lf.get_changelist(testdr, proddr, ltype)
changelist.to_csv(projectdir + changedir + monthStr + "-" + filename, encoding="UTF-8", index=False)

# SA Conservation
filename = "SA-conservation.csv"
testdr = "dr653"
proddr = "dr653"
changelist = lf.get_changelist(testdr, proddr, ltype)
changelist.to_csv(projectdir + changedir + monthStr + "-" + filename, encoding="UTF-8", index=False)

# TAS Conservation
filename = "TAS-conservation.csv"
testdr = "dr654"
proddr = "dr654"
changelist = lf.get_changelist(testdr, proddr, ltype)
changelist.to_csv(projectdir + changedir + monthStr + "-" + filename, encoding="UTF-8", index=False)

# VIC Conservation
filename = "VIC-conservation.csv"
testdr = "dr655"
proddr = "dr655"
changelist = lf.get_changelist(testdr, proddr, ltype)
changelist.to_csv(projectdir + changedir + monthStr + "-" + filename, encoding="UTF-8", index=False)

# WA Conservation
filename = "WA-conservation.csv"
testdr = "dr2201"
proddr = "dr2201"
changelist = lf.get_changelist(testdr, proddr, ltype)
changelist.to_csv(projectdir + changedir + monthStr + "-" + filename, encoding="UTF-8", index=False)

###############################################################################################################
# Sensitive  Lists

ltype = "S"
# ACT Sensitive
filename = "ACT-sensitive.csv"
testdr = "dr2627"
proddr = "dr2627"
changelist = lf.get_changelist(testdr, proddr, ltype)
changelist.to_csv(projectdir + changedir + monthStr + "-" + filename, encoding="UTF-8", index=False)

# NSW Sensitive
filename = "NSW-sensitive.csv"
testdr = "dr18457"
proddr = "dr487"
changelist = lf.get_changelist(testdr, proddr, ltype)
changelist.to_csv(projectdir + changedir + monthStr + "-" + filename, encoding="UTF-8", index=False)

# NT Sensitive
filename = "NT-sensitive.csv"
testdr = "dr492"
proddr = "dr492"
changelist = lf.get_changelist(testdr, proddr, ltype)
changelist.to_csv(projectdir + changedir + monthStr + "-" + filename, encoding="UTF-8", index=False)

# Qld Sensitive
filename = "QLD-sensitive.csv"
testdr = "dr18404"
proddr = "dr493"
changelist = lf.get_changelist(testdr, proddr, ltype)
changelist.to_csv(projectdir + changedir + monthStr + "-" + filename, encoding="UTF-8", index=False)

# SA Sensitive
filename = "SA-sensitive.csv"
testdr = "dr18706"
proddr = "dr884"
changelist = lf.get_changelist(testdr, proddr, ltype)
changelist.to_csv(projectdir + changedir + monthStr + "-" + filename, encoding="UTF-8", index=False)

# TAS Sensitive - not currently in Test
# filename = "TAS-sensitive.csv"
# testdr = "NA"
# proddr = "dr491"
# changelist = lf.get_changelist(testdr, proddr, ltype)
# changelist.to_csv(projectdir + changedir + monthStr + "-" + filename, encoding="UTF-8", index=False)
# changelist

# VIC Sensitive
filename = "VIC-sensitive.csv"
testdr = "dr18669"
proddr = "dr490"
changelist = lf.get_changelist(testdr, proddr, ltype)
changelist.to_csv(projectdir + changedir + monthStr + "-" + filename, encoding="UTF-8", index=False)

# WA Sensitive
filename = "WA-sensitive.csv"
testdr = "dr18406"
proddr = "dr467"
changelist = lf.get_changelist(testdr, proddr, ltype)
changelist.to_csv(projectdir + changedir + monthStr + "-" + filename, encoding="UTF-8", index=False)

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
    prodList.to_csv(projectdir + "historical-lists/conservation/" + filename, encoding="UTF-8", index=False)
print('Finished downloading conservation historical list')

#
# Sensitive Lists
drList = {"TAS": "dr491"}  # Notebook is dying on empty kvpValues when in Jupyter notebook. runs fine in py script
# drList = {"ACT":"dr2627", "NSW":"dr487", "NT":"dr492", "QLD":"dr493", "SA":"dr884","TAS":"dr491", 
# "VIC":"dr490", "WA":"dr467"}
# drList = {"ACT":"dr2627", "NSW":"dr487", "NT":"dr492", "QLD":"dr493", "SA":"dr884", "VIC":"dr490", "WA":"dr467"}
for state, dr in drList.items():
    filename = state + "-" + dr + "-sensitive.csv"
    print(dr)
    prodListUrl = "https://lists.ala.org.au/ws/speciesListItems/" + dr + "?max=10000&includeKVP=true"
    prodList = lf.download_ala_list(prodListUrl)  # save the prod list to the historical lists directory
    prodList = lf.kvp_to_columns(prodList)
    prodList.to_csv(projectdir + "historical-lists/sensitive/" + filename, encoding="UTF-8", index=False)
print('Finished downloading sensitive historical list')
