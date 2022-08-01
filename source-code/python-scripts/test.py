# WA Conservation and Sensitive Lists
# WA has the same list for both conservation and sensitive lists
#import essential libraries
# import essential libraries
#%%
import pandas as pd
import requests
import xlrd

#%%
# top level directory
projectdir = "/Users/oco115/PycharmProjects/auth-lists-updates/"
basedir = "/Users/oco115/PycharmProjects/authoritative-lists/"

#Species List and Species codes URLS
# faunalisturl = "https://www.dpaw.wa.gov.au/images/documents/plants-animals/threatened-species/Listings/Threatened%20and%20Priority%20Fauna%20List.xlsx"
# floralisturl = "https://www.dpaw.wa.gov.au/images/documents/plants-animals/threatened-species/Listings/Threatened%20and%20Priority%20Flora%20List%205%20December%202018.xlsx"

faunafile = projectdir + "source-data/Threatened and Priority Fauna List.xlsx"
florafile = projectdir + "source-data/Threatened and Priority Flora List.xlsx"
#%%
print("Downloading WA Fauna List")
fauna = pd.read_excel(faunafile)
print("Finished Fauna download")


#%%
print("Downloading WA Flora List")
flora = pd.read_excel(florafile,skiprows=1)
print("Finished Flora download")