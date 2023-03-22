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
outdir = projectdir + "analysis/reports/"
sys.path.append(os.path.abspath(projectdir + "source-code/includes"))
import list_functions as lf
import configuration as cfg

# monthStr = datetime.datetime.now().strftime('%Y%m%d')
##############################################################################################
# Retrieve Lists information

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



