# R Scripts
This directory contains utility scripts used for analysing Species Lists
##Base Files
| **File Name**| **Description**|
|----------------|----------------|
| config.R| Configuration file |
| species-lists-compare.R| Original script using R package 'xlsx' to write to Excel. No config file required|
| species-lists-compare-Openxlsx.R| Script using R package 'openxlsx' to write to Excel - no Java dependency, uses config file|

## Split Files
The code has been split to have all functions in a separate file. Why? When using the debugger, in order to set breakpoints you need to 'source' the code when functions
are included. This made debugging difficult. By separating the functions and using the **source** command to include the functions, breakpoints can immediately be set
within the function code. The code below is based on the **species-lists-compare-Openxlsx.R** source.

| **File Name**| **Description**|
|----------------|----------------|
| config.R| Configuration file |
| species-lists-functions.R| Functions specification|
| species-lists-main.R| Main processing|
