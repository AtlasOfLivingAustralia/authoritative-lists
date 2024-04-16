
library(dplyr)
library(jsonlite)
library(tidyr) 
library(openxlsx)
source("./source-code/R/config.R")


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
    tempSheet <- addWorksheet(wb,sheetName="Sheet1")
    saveWorkbook(wb,xlsxfile)
    
  }
  sheets <- getSheetNames(xlsxfile) 
  if(s %in% sheets) {
    removeWorksheet(wb,sheet = s)
    saveWorkbook(wb,xlsxfile,overwrite=TRUE)
  }
  stateSheet <- addWorksheet(wb,sheet = s) 
  writeData(wb,stateSheet,listjoin,rowNames=FALSE)
  saveWorkbook(wb, xlsxfile,overwrite=TRUE)
  
  # write to excel - match report
  if("matchReport" %in% sheets) {
    prevMatchReportDf <- read.xlsx(xlsxfile,"matchReport")
    prevMatchReportDf <- prevMatchReportDf %>% filter(stateCode != s) 
    matchReportDf <- union(prevMatchReportDf,matchReportDf)
    removeWorksheet(wb, sheet = "matchReport")
  } 
 
  matchSheet <- addWorksheet(wb,sheet = "matchReport") 
  writeData(wb,matchSheet,matchReportDf,rowNames=FALSE)
  saveWorkbook(wb, xlsxfile,overwrite=TRUE)
  
  # write to excel - status report
  if("statusReport" %in% sheets) {
    prevStatusReportDf <- read.xlsx(xlsxfile,"statusReport")
    prevStatusReportDf <- prevStatusReportDf %>% filter(stateCode != s)
    statusDf <- union(prevStatusReportDf,statusDf)
    removeWorksheet(wb, sheet = "statusReport")
  }
  statusSheet <- addWorksheet(wb,sheet = "statusReport") 
  writeData(wb,statusSheet,statusDf,rowNames=FALSE)
  saveWorkbook(wb, xlsxfile,overwrite=TRUE)

}

