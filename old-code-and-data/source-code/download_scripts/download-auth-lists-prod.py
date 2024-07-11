#%% 
# Download conservation lists from Prod
#  
#
import datetime
import os
import sys

projectDir = "/Users/oco115/PycharmProjects/authoritative-lists/"
downloadDir = "/Users/oco115/PycharmProjects/auth-lists-local/"
sys.path.append(os.path.abspath(projectDir + "source-code/includes"))
monthStr = datetime.datetime.now().strftime('%Y%m%d')
import list_functions as lf

###############################################################################################################
# Download Conservation lists

drList = {"ACT": "dr649", "NSW": "dr650", "NT": "dr651", "QLD": "dr652", "SA": "dr653", "TAS": "dr654",
          "VIC": "dr655", "EPBC": "dr656", "WA": "dr2201"}

print("Downloading Conservation lists to: ", downloadDir + "conservation/")
for state, dr in drList.items():
    filename = state + "-" + dr + "-conservation.csv"
    print("... Dataresource: ", filename)
    prodListUrl = "https://lists.ala.org.au/ws/speciesListItems/" + dr + "?max=10000&includeKVP=true"
    prodList = lf.download_ala_specieslist(prodListUrl)
    prodList = lf.kvp_to_columns(prodList)
    prodList.to_csv(downloadDir + "conservation/" + filename, encoding="UTF-8", index=False)
print('Finished downloading conservation lists')

# Download Sensitive lists
#
drList = {"ACT":"dr2627", "NSW":"dr487", "NT":"dr492", "QLD":"dr493", "SA":"dr884","TAS":"dr491",
"VIC":"dr490", "WA":"dr467"}

print("Downloading Sensitive lists to: ", downloadDir + "sensitive/")
for state, dr in drList.items():
    print("... Dataresource: ", filename)
    filename = state + "-" + dr + "-sensitive.csv"
    prodListUrl = "https://lists.ala.org.au/ws/speciesListItems/" + dr + "?max=10000&includeKVP=true"
    prodList = lf.download_ala_specieslist(prodListUrl)
    prodList = lf.kvp_to_columns(prodList)
    prodList.to_csv(downloadDir + "sensitive/" + filename, encoding="UTF-8", index=False)
print('Finished downloading sensitive lists')
