
library(dplyr)
library(jsonlite)
library(tidyr) 
library(openxlsx)
source("./source-code/R/config.R")
source("./source-code/R/species-lists-functions.R")


conservationLists <- setNames(conservationLists,c("stateCodes","asIsListIds","toBeListIds"))

for(i in 1:nrow(conservationLists)) {
  downloadLists(conservationLists[i,1],conservationLists[i,2],conservationLists[i,3])
  writeListComparison(conservationLists[i,1],conservationLists[i,2],conservationLists[i,3])
}

