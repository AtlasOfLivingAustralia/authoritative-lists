env <- "PROD"
#env <- "TEST"

if (env == "PROD") {
  listsUrl <<- "https://lists.ala.org.au/ws/speciesListItems/"
  directory <<- "C:/Users/oco115/Documents/data/prod/"
  xlsxfile <<- paste0(directory,"conservation-list-compare-prod.xlsx")
  conservationLists <- data.frame(t(data.frame(c("EPBC","dr656","dr18735"),
                                               c("ACT","dr649","dr18718"),
                                               c("NSW","dr650","dr18736"),
                                               c("NT","dr651","dr18704"),
                                               c("QLD","dr652","dr18703"),
                                               c("SA","dr653","dr18701"),
                                               c("TAS","dr654","dr18705"),
                                               c("VIC","dr655","dr18706"),
                                               c("WA","dr2201","dr18714"))),row.names = NULL,stringsAsFactors = FALSE)
} else if (env == "TEST") {
  listsUrl <<- "https://lists-test.ala.org.au/ws/speciesListItems/"
  directory <<- "C:/Users/oco115/Documents/data/test/"
  xlsxfile <<- paste0(directory,"conservation-list-compare-test.xlsx")
  conservationLists <- data.frame(t(data.frame(c("EPBC","dr656","dr18397"),
                                               c("ACT","dr649","dr18396"),
                                               c("NSW","dr650","dr18437"),
                                               c("NT","dr651","dr18398"),
                                               c("QLD","dr652","dr18399"),
                                               c("SA","dr653","dr18400"),
                                               c("TAS","dr654","dr18401"),
                                               c("VIC","dr655","dr18402"),
                                               c("WA","dr2201","dr18456"))),row.names = NULL,stringsAsFactors = FALSE)
}