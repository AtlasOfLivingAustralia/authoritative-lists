##############################################################################################
#
# List Information Report
# Extract Lists metadata for Test and Production
# Output report
# Output information files to : ..\authoritative-lists\analysis\reports
##############################################################################################
#
import sys
import os

projectdir = "/Users/oco115/PycharmProjects/authoritative-lists/"
outdir = projectdir + "analysis/Monitoring/"
sys.path.append(os.path.abspath(projectdir + "source-code/includes"))
import list_functions as lf
import configuration as cfg

# monthStr = datetime.datetime.now().strftime('%Y%m%d')
##############################################################################################
drList = {"TAS":"dr491"}
# drList = {"ACT":"dr2627", "NSW":"dr487", "NT":"dr492", "QLD":"dr493", "SA":"dr884","TAS":"dr491", "VIC":"dr490", "WA":"dr467"}
# drList = {"ACT":"dr2627", "NSW":"dr487", "NT":"dr492", "QLD":"dr493", "SA":"dr884", "VIC":"dr490", "WA":"dr467"}
for state, dr in drList.items():
    filename = state + "-" + dr + "-sensitive.csv"
    print(dr)
    prodListUrl = "https://lists.ala.org.au/ws/speciesListItems/" + dr + "?max=10000&includeKVP=true"
    prodList = lf.download_ala_list(prodListUrl)  # save the prod list to the historical lists directory
    prodList = lf.kvp_to_columns(prodList)
    prodList.to_csv(projectdir + "historical-lists/sensitive/" + filename, encoding="UTF-8", index=False)
print('Finished downloading sensitive historical list')

# Retrieve Lists information via Lists API from specieslist
# currently API only returns the following information:
#   "dataResourceUid": "dr1820",
#   "listName": "Training project 2",
#   "dateCreated": "2014-11-13T04:11:27Z",
#   "username": "zarni.bear@environment.gov.au",
#   "fullName": null,
#   "itemCount": 0,
#   "isAuthoritative": false,
#   "isInvasive": false,
#   "isThreatened": false,
#   "listType": "LOCAL_LIST"

# Production
listsUrl = cfg.listsProd
proddf = lf.get_listDataframe(listsUrl)
proddf = proddf.sort_values('listName', ascending=True)
# proddf.to_csv(outdir + "Production-lists.csv", index=False, encoding='utf-8')
pconsdf = lf.filterDataframe(proddf, cfg.consDRProd)   # Conservation Lists
psensdf = lf.filterDataframe(proddf, cfg.sensDRProd)   # Sensitive Lists

# Test
listsUrl = cfg.listsTest
testdf = lf.get_listDataframe(listsUrl)
testdf = testdf.sort_values('listName', ascending=True)
# testdf.to_csv(outdir + "Test-lists.csv", index=False, encoding='utf-8')
tconsdf = lf.filterDataframe(testdf, cfg.consDRTest)   # Conservation Lists
tsensdf = lf.filterDataframe(testdf, cfg.sensDRTest)   # Sensitive Lists

##############################################################################################

print('Writing report to markdown')
pmdfile = outdir + "Authoritative_lists.md"
tmdfile = outdir + "Authoritative_lists-test.md"
lf.list_to_markdown("P", pconsdf, psensdf, pmdfile)
lf.list_to_markdown("T", tconsdf, tsensdf, tmdfile)
print('Finished Processing')



