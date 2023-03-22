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
for state, dr in drList.items():
    filename = state + "-" + dr + "-sensitive.csv"
    print(dr)
    prodListUrl = "https://lists.ala.org.au/ws/speciesListItems/" + dr + "?max=10000&includeKVP=true"
    prodList = lf.download_ala_list(prodListUrl)  # save the prod list to the historical lists directory
    prodList = lf.kvp_to_columns(prodList)
    prodList.to_csv(projectdir + "historical-lists/sensitive/" + filename, encoding="UTF-8", index=False)
print('Finished downloading sensitive historical list')







