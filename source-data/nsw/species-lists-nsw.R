

library(jsonlite)
library(dplyr)
library(tidyr) #spread

url <- "https://data.bionet.nsw.gov.au/biosvcapp/odata/SpeciesNames"
nswsp <- fromJSON(url)
nswsp <- nswsp$value
write.csv(nswsp,"data/species-lists/nsw-speciesnames-ws-20220202.csv", row.names = FALSE)

# Where species_id = taxonID these are current records
# Filter StateConservation = conservation list
# Filter sensitivityClass = sensitive list

nswsdssource <- nswsp %>% filter(speciesID == taxonID & sensitivityClass != "Not Sensitive")
nswsdssource <- nswsdssource %>% select(taxonRank,kingdom,class,order,family,genus,scientificName,specificEpithet,vernacularName,establishmentMeans,stateConservation,protectedInNSW,sensitivityClass,TSProfileID,countryConservation,dcterms_modified,speciesID,taxonID)

# current list in ALA
# see https://lists.ala.org.au/ws for more info

listinfourl <- "https://lists.ala.org.au/ws/speciesList/dr487"
nswsdslistinfo <- fromJSON(listinfourl)
listurl <- "https://lists.ala.org.au/ws/speciesListItems/dr487?includeKVP=true"
nswsdslist <- fromJSON(listurl)

#unwrap kvp
columniseKeyValuePairs <- function(df) {
  # create a dataframe of key, value plus add the id for each
  x <- Reduce(rbind,apply(df,1,function(i) data.frame(i$kvpValues) %>% mutate(id=i$id)))
  # turn the keys into columns and values in the row
  x2 <- x %>% spread(key,value)
  # join back to the original dataset
  return(left_join(df,x2,by="id")) 
}

nswsdslist <- columniseKeyValuePairs(nswsdslist)
nswsdslist %>% count(category,generalisation) # what are the existing generalisations 

# new list needs to be updated with the appropriate generalisations
nswsdssource <- nswsdssource %>% mutate(generalisation = case_when(sensitivityClass=="Category 1" ~ "WITHHOLD",
                                                                   sensitivityClass=="Category 2" ~ "10km",
                                                                   sensitivityClass=="Category 3" ~ "1km"))
# sanity check
nswsdssource %>% count(sensitivityClass,generalisation)

# upload this to Lists to check
write.csv(nswsdssource,"data/species-lists/nsw-sds-20220120.csv", row.names = FALSE)

# download the matched list
templisturl <- "https://lists.ala.org.au/ws/speciesListItems/dr18282?includeKVP=true"
templist <- fromJSON(templisturl)
templist <- columniseKeyValuePairs(templist)

# which are the same? 
listjoin <- full_join(nswsdslist,templist, by=c("scientificName"="name"),suffix=c(".old",".new"),keep = TRUE)
listjoin <- listjoin %>% select(dataResourceUid.old,name.old,scientificName.old,lsid.old,`vernacular name.old`,generalisation.old,dataResourceUid.new,name.new,scientificName.new,lsid.new,`vernacular name.new`,generalisation.new)
listjoin <- listjoin %>% mutate(diff = case_when(scientificName.old==scientificName.new & generalisation.old==generalisation.new ~ "UNCHANGED",
                                                 scientificName.old==scientificName.new & generalisation.old!=generalisation.new ~ "CATEGORY CHANGE",
                                                 is.na(dataResourceUid.new) ~ "REMOVED",
                                                 is.na(dataResourceUid.old) ~ "ADDED",  TRUE ~ "?")) %>%
  arrange(diff,name.new,name.old)

write.csv(listjoin,"data/species-lists/nsw-sds-listcompare-20220120.csv", row.names = FALSE)
nswsdslistcompare <- listjoin
#
#
#
# stateConservation List
nswconssource <- nswsp %>% filter(speciesID == taxonID & stateConservation != "Not Listed")
nswconssource <- nswconssource %>% select(taxonRank,kingdom,class,order,family,genus,scientificName,specificEpithet,vernacularName,establishmentMeans,stateConservation,protectedInNSW,sensitivityClass,TSProfileID,countryConservation,dcterms_modified,speciesID,taxonID)

# current list in ALA
# see https://lists.ala.org.au/ws for more info

listurl <- "https://lists.ala.org.au/ws/speciesListItems/dr650?includeKVP=true"
nswconslist <- fromJSON(listurl)
nswconslist <- columniseKeyValuePairs(nswconslist)

# sanity check
nswconssource %>% count(stateConservation)
nswconslist %>% count(status)

# upload to lists to check
write.csv(nswconssource, "data/species-lists/nsw-cons-20220121.csv", row.names = FALSE)

# download the matched list
templisturl <- "https://lists.ala.org.au/ws/speciesListItems/dr18284?includeKVP=true"
templist <- fromJSON(templisturl)
templist <- columniseKeyValuePairs(templist)

# which are the same? 
listjoin <- full_join(nswconslist,templist, by=c("Supplied  Name"="name"),suffix=c(".old",".new"),keep = TRUE)
listjoin <- listjoin %>% select(dataResourceUid.old,`Supplied  Name`,name.old,scientificName.old,lsid.old,`vernacular name.old`,status,dataResourceUid.new,name.new,scientificName.new,lsid.new,`vernacular name.new`,stateConservation)
listjoin <- listjoin %>% mutate(diff = case_when(scientificName.old==scientificName.new & status==stateConservation ~ "UNCHANGED",
                                                 scientificName.old==scientificName.new & status!=stateConservation ~ "STATUS CHANGE",
                                                 is.na(dataResourceUid.new) ~ "REMOVED",
                                                 is.na(dataResourceUid.old) ~ "ADDED",  TRUE ~ "?")) %>%
  arrange(diff,name.new,name.old)

write.csv(listjoin,"data/species-lists/nsw-cons-listcompare-20220120.csv", row.names = FALSE)
nswconslistcompare <- listjoin


# analysis
# source data: Perameles bougainville	fasciata

bodgies <- nswsp %>% filter(grepl("^Perameles bougainville",scientificName) | 
                              grepl("^Thinornis cucullatus",scientificName) | 
                              grepl("^Lerista xanthura",scientificName) | 
                              grepl("^Tyto novaehollandiae",scientificName)) %>%
  mutate(currency = case_when(speciesID!=taxonID ~ "not current",TRUE ~ "current")) %>%
  select(currency,speciesID,taxonID,taxonRank,stateConservation,sensitivityClass,countryConservation,genus,scientificName,specificEpithet,vernacularName,establishmentMeans,protectedInNSW,TSProfileID,dcterms_modified) %>%
  arrange(scientificName,desc(speciesID))
write.csv(bodgies,"data/species-lists/nsw-speciesnames-camsbodgies-20220204.csv", row.names = FALSE)


