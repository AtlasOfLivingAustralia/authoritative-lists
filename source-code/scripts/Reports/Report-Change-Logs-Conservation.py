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
