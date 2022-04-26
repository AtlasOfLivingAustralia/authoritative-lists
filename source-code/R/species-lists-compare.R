#species-list-compare.R
#downloadsets lists from the list tool and compare them


options(java.parameters = "-Xmx8000m") # for extra memory for xlsx which uses the java poi libraries

library(dplyr)
library(jsonlite)
library(tidyr) #spread
library(xlsx)


# function to unwrap kvp
columniseKeyValuePairs <- function(df) {
  # create a dataframe of key, value plus add the id for each
  x <- Reduce(rbind,apply(df,1,function(i) data.frame(i$kvpValues) %>% mutate(id=i$id)))
  # turn the keys into columns and values in the row
  x2 <- x %>% spread(key,value)
  #remove the kvp list
  df <- select(df,-kvpValues)
  # join back to the original dataset
  return(left_join(df,x2,by="id")) 
}

downloadLists <- function(stateCode,asIsListId,toBeListId) {
  
  # download the lists
  #listsUrl <- "https://lists.ala.org.au/ws/speciesListItems/"
  asIsList <- fromJSON(paste0(listsUrl,asIsListId,"?includeKVP=true"))
  asIsList <- columniseKeyValuePairs(asIsList) 
  toBeList <- fromJSON(paste0(listsUrl,toBeListId,"?includeKVP=true"))
  toBeList <- columniseKeyValuePairs(toBeList)
  
  #write to file

  write.csv(asIsList,paste0(directory,stateCode,"-",asIsListId,".csv"))
  write.csv(toBeList,paste0(directory,stateCode,"-",toBeListId,".csv"))
}

writeListComparison <- function(s, asIsListId, toBeListId) {

  s <- as.character(s) 
  asIsList <- read.csv(paste0(directory,s,"-",asIsListId,".csv"))
  toBeList <- read.csv(paste0(directory,s,"-",toBeListId,".csv"))
  
  #sanity check
  print(paste(s,"previous list"))
  print(asIsList %>% count(status))
  print(paste(s,"new list"))
  print(toBeList %>% count(status))
  
  # join the lists on scientificName, find which are new, deleted, and changed
  listjoin <- full_join(asIsList,toBeList, by=c("scientificName"="scientificName"),suffix=c(".old",".new"),keep = TRUE,na_matches = "never")
  listjoin <- listjoin %>% select(dataResourceUid.old,name.old,scientificName.old,lsid.old,commonName.old,status.old,
                                  dataResourceUid.new,name.new,scientificName.new,lsid.new,commonName.new,status.new)
  listjoin <- listjoin %>% mutate_if(is.factor,as.character)
  listjoin <- listjoin %>% mutate(diff = case_when(scientificName.old==scientificName.new & status.old==status.new ~ "UNCHANGED",
                                                 scientificName.old==scientificName.new & status.old!=status.new ~ "STATUS CHANGE",
                                                 is.na(dataResourceUid.new) ~ "REMOVED",
                                                 is.na(dataResourceUid.old) ~ "ADDED",  TRUE ~ "?")) %>%
  arrange(diff,name.new,name.old)
  
  # report on counts and matches
  stateCode <- s
  asIsCount <- count(asIsList)
  toBeCount <- count(toBeList)
  asIsCountMatched <- count(asIsList %>% filter(!is.na(lsid)))
  toBeCountMatched <- count(toBeList %>% filter(!is.na(lsid)))
  asIsMatchProportion <- asIsCountMatched/asIsCount
  toBeMatchProportion <- toBeCountMatched/toBeCount
  
  matchReportDf <- data.frame(stateCode,asIsListId,toBeListId,asIsCount,toBeCount,asIsCountMatched,toBeCountMatched,asIsMatchProportion,toBeMatchProportion)
  names(matchReportDf) <- c("stateCode","asIsListId","toBeListId","asIsCount","toBeCount","asIsCountMatched","toBeCountMatched","asIsMatchProportion","toBeMatchProportion")

  # report on status counts
  asIsStatuses <- asIsList %>% count(status) %>% mutate(listID = asIsListId, listType="as-is") %>% rename(count = n)
  toBeStatuses <- toBeList %>% count(status) %>% mutate(listID = toBeListId, listType="to-be") %>% rename(count = n)
  statusDf <- union(asIsStatuses,toBeStatuses) %>% mutate(stateCode = s)

  # write to excel - state lists to compare
  if(file.exists(xlsxfile)) {
    wb <- loadWorkbook(xlsxfile)
  } else {
    wb <- createWorkbook()
    tempSheet <- createSheet(wb,sheetName="Sheet1")
    saveWorkbook(wb,xlsxfile)
    
  }
  sheets <- getSheets(wb) 
  if(s %in% names(sheets)) {
    removeSheet(wb,sheetName = s)
    saveWorkbook(wb,xlsxfile)
  }
  stateSheet <- createSheet(wb,sheetName = s)
  addDataFrame(listjoin,stateSheet,row.names=FALSE)
  saveWorkbook(wb, xlsxfile)
  
  # write to excel - match report
  if("matchReport" %in% names(sheets)) {
    prevMatchReportDf <- read.xlsx(xlsxfile,"matchReport")
    prevMatchReportDf <- prevMatchReportDf %>% filter(stateCode != s) 
    matchReportDf <- union(prevMatchReportDf,matchReportDf)
    removeSheet(wb, sheetName = "matchReport")
  } 
  matchSheet <- createSheet(wb, sheetName = "matchReport")
  addDataFrame(matchReportDf,matchSheet,row.names = FALSE)
  saveWorkbook(wb,xlsxfile)
  
  # write to excel - status report
  if("statusReport" %in% names(sheets)) {
    prevStatusReportDf <- read.xlsx(xlsxfile,"statusReport")
    prevStatusReportDf <- prevStatusReportDf %>% filter(stateCode != s)
    statusDf <- union(prevStatusReportDf,statusDf)
    removeSheet(wb, sheetName = "statusReport")
  }
  statusSheet <- createSheet(wb, sheetName = "statusReport")
  addDataFrame(statusDf,statusSheet,row.names = FALSE)
  saveWorkbook(wb,xlsxfile)

}

#globals

env <- "TEST"

if (env == "PROD") {
  listsUrl <<- "https://lists.ala.org.au/ws/speciesListItems/"
  directory <<- "data/species-lists/species-list-compare/prod/"
  xlsxfile <<- paste0(directory,"conservation-list-compare.xlsx")
  conservationLists <- data.frame(t(data.frame(c("EPBC","dr656","dr18735"),
                                               c("ACT","dr649","dr18718"),
                                               c("NSW","dr650","dr18736"),
                                               c("NT","dr651","dr18704"),
                                               c("QLD","dr652","dr18703"),
                                               c("SA","dr653","dr18701"),
                                               c("TAS","dr654","dr18705"),
                                               c("VIC","dr655","dr18706"),
                                               c("WA","dr2201","dr18714"))),row.names = NULL,stringsAsFactors = FALSE)
  conservationLists <- setNames(conservationLists,c("stateCodes","asIsListIds","toBeListIds"))
} else if (env == "TEST") {
  listsUrl <<- "https://lists-test.ala.org.au/ws/speciesListItems/"
  directory <<- "data/species-lists/species-list-compare/test/"
  xlsxfile <<- paste0(directory,"conservation-list-compare.xlsx")
  conservationLists <- data.frame(t(data.frame(c("EPBC","dr656","dr18397"),
                                               c("ACT","dr649","dr18396"),
                                               c("NSW","dr650","dr18437"),
                                               c("NT","dr651","dr18398"),
                                               c("QLD","dr652","dr18399"),
                                               c("SA","dr653","dr18400"),
                                               c("TAS","dr654","dr18401"),
                                               c("VIC","dr655","dr18402"),
                                               c("WA","dr2201","dr18456"))),row.names = NULL,stringsAsFactors = FALSE)
  conservationLists <- setNames(conservationLists,c("stateCodes","asIsListIds","toBeListIds"))
}

for(i in 1:nrow(conservationLists)) {
  downloadLists(conservationLists[i,1],conservationLists[i,2],conservationLists[i,3])
  writeListComparison(conservationLists[i,1],conservationLists[i,2],conservationLists[i,3])
}

# debugging - for line by line walk through function
# asIsListId <- "dr652"
# toBeListId <- "dr18703"
# s = "QLD"
# downloadLists(s,asIsListId,toBeListId)
# writeListComparison(s,asIsListId,toBeListId)

