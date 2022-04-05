Directory containing new:
1. Conservation Lists
2. Sensitive Lists


# Status/Source Status Values
The table below indicates the Source status values provided by State organisations and the values assigned for ALA upload. <br>
<br>**Note:** Status value is a minimum requirement for Species List records. Any records without a status were removed from the dataset prior to upload. 

| **State** | **Source Status**|**Status Applied**|**Notes**|
| --------- | ------------------|-----------------|---------|
|	ACT	|	Critically endangered	|	Critically endangered	| |
|	ACT	|	Endangered	|	Endangered	| |
|	ACT	|	Vulnerable	|	Vulnerable	| |
| ACT|Regionally Conservation Dependent| Regionally Conservation Dependent|No mapping available| 
|	EPBC	|	Extinct in wild	|	Extinct	| |
|	EPBC	|	Vulnerable	|	Vulnerable	| |
|	EPBC	|	Critically Endangered	|	Critically endangered	| |
|	EPBC	|	Conservation dependent	|	Conservation dependent	| |
|	EPBC	|	Endangered |	Endangered	| |
|	EPBC	|	Extinct	|	Extinct	| |
|	NT	|	Endangered	|	Endangered	| |
|	NT	|	Vulnerable	|	Vulnerable	| |
|	NT	|	Critically endangered	|	Critically endangered	| |
|	NT	|	Listed nationally but not under NT legislation	|	<remove record - covered by EPBC>	| |
|	NT	|	Endangered (extinct in NT)	|	Endangered	| |
|	NT	|	Extinct	|	Extinct	| |
|	NT	|	Listed nationally but not under NT legislation Bird	|	<remove record - covered by EPBC>	| |
|	NT	|	Least concern (extinct in NT)	|	Least concern	| |
|	NT	|	Vulnerable (extinct in NT)	|	Vulnerable	| |
|	NT	|	Endangered (extinct in wild in NT)	|	Endangered	| |
|	NT	|	Critically endangered (possibly extinct)	|	Critically endangered	| |
|	SA	|	SA:E	|	Endangered	|Fauna |
|	SA	|	SA:R	|	Rare	| Fauna |
|	SA	|	SA:V	|	Vulnerable	| Fauna |
|	SA	|	SA:E	|	Endangered	| Fauna |
|	SA	|	Declared	|	Declared	| Flora|
|	SA	|	Endangered	|	Endangered	| Flora|
|	SA	|	Rare	|	Rare	| Flora|
|	SA	|	Vulnerable	|	Vulnerable	| Flora|
|	QLD	|	EX  |	Extinct	|
|	QLD	|	E  |	Endangered	|
|	QLD	|	PE	|	Extinct in the wild	|
|	QLD	|	CR  |	Critically endangered	|
|	QLD	|	V	|	Vulnerable	|
|	QLD	|	NT  |	Near threatened wildlife	|
|	QLD	|	SL	|	Special least concern	|
|	QLD	|	C   |	least concern wildlife	|
|	QLD	|	I	|	International wildlife	|
| TAS| e |Endangered |Threatened Species Protection Act 1995 - Schedule 3.1|
| TAS| x |Presumed Extinct  |Threatened Species Protection Act 1995 - Schedule 3.2|
| TAS| v |Vulnerable|Threatened Species Protection Act 1995 - Schedule 4|
| TAS| r |Rare |Threatened Species Protection Act 1995 - Schedule 5|
|	VIC|	EX and X  |Presumed	extinct	|
|	VIC	|	E and EN |	Endangered	|
| VIC	|	RX	|	Regionally extinct	|
|	VIC|	WX |Extinct in the wild	|
|	VIC	|	CR  |	Critically endangered	|
|	VIC	|	VU	|	Vulnerable	|
|	VIC	|	NT  |	Near threatened	wildlife|
|	VIC	|	SL	|	Data deficient	|
|	VIC	|	P   |	All ssp threatened	|
|	VIC	|	K   |	Poorly known	|

# Data Processing
Datasets provided have been in a variety of formats requiring extensive manual processing to format for upload to ALA, in addition to the status mappings described above. The table below summarises the types of data received and the effort required to format the data for upload. <br>
<br>
| **State** | **List Type**| **Extract source**|**Processing/Rules**|
| --------- | ------------------|--------------|--------------------|
  |	ACT	|	Sensitive	|Webpage|<ol><li>Webpage has list in MS WORD, PDF and HTML format</li><li>Open HTML </li><li>Manual copy and paste to to Excel spreadsheet, save as CSV</li><li>Data processed using text editor Vim/Regex: </li><ul><li>Adding commas to separate columns</li><li>Splitting single species name column into 2 separate columns for *vernacularName* and *scientificName*</li><li>Remove brackets from *vernacularName*</li><li>Created additional DWC columns for known values</li></ul></ol> |
|	ACT	|	Conservation	|Webpage/MS Word|<ol><li> Website has MS WORD, PDF and HTML format</li><li>Downloaded MS Word document</li><li>Manual copy and paste to to Excel spreadsheet</li><li>Data processed using Jupyter notebook including: </li><ul><li>Mapping DWC terms</li></ul></ol> |
|	EPBC	|	Conservation	|Webpage/Text|<ol><li> Two separate flora and fauna lists were available on the website</li><li>These lists were copied from webpage to a CSV file along with hyperlinks and separate categories i.e. frogs, birds, reptiles etc</li><li>Data was cleaned and processed using Jupyter notebook including: </li><ul> Extracting hyperlinks from the text </li> <li>Mapping DWC terms </li> <li>Date format conversion </li> <li>Creating additional DWC columns for known values</li> <li>Merging processed flora and fauna files</li> </ul></ol> |
|	NSW	|	Sensitive	|Webpage	|<ol><li> xxxxx</li> <li>xxxxxx</li> <li>Data processed including: </li> <li>Creating additional DWC columns for known values</li> </ul></ol> |
|	NSW	|	Conservation	|Webpage	|<ol><li> xxxxx</li> <li>xxxxxx</li> <li>Data processed including: </li> <li>Creating additional DWC columns for known values</li> </ul></ol> |
|	NT	|	Conservation	|Webpage/Text	|<ol><li> Two separate flora and fauna lists were available on the website</li> <li>Lists text copied from webpage to a CSV file</li> <li>Data was cleaned and processed using Jupyter notebook including: </li><li>Splitting single species name column into 2 separate columns for *vernacularName* and *scientificName* <li>Mapping DWC terms</li> <li>Creating additional DWC columns for known values</li> <li>Merging processed flora and fauna files together</li></ul></ol> |
|	QLD	|	Sensitive	|Webpage/MS Excel	|<ol><li> Downloaded Excel spreadsheet and processed using Jupyter notebook including: </li><ul> <li>Mapping DWC terms</li> <li>Deleting data without a status</li> <li>Mapping provided status to status codes</li> <li>Rearanging data and encoding-decoding formatting</li></ul></ol>|
|	QLD	|	Conservation	|Webpage/MS Excel	|<ol><li> Downloaded Excel spreadsheet and processed using Jupyter notebook including: </li><ul> <li>Mapping DWC terms <li>Deleting data without a status</li> <li>Mapping provided status to status codes</li> <li>Rearanging data and encoding-decoding formatting</li></ul></ol>|
|	SA	|	Sensitive	|Webpage	|<ol><li> xxxxx</li> <li>xxxxxx</li> <li>Data processed including: </li> <li>Creating additional DWC columns for known values</li> </ul></ol> |
|	SA	|	Conservation	|Webpage	|<ol><li> xxxxx</li> <li>xxxxxx</li> <li>Data processed including: </li> <li>Creating additional DWC columns for known values</li> </ul></ol> |
|	TAS	|	Conservation	|Webpage	|<ol><li> xxxxx</li> <li>xxxxxx</li> <li>Data processed including: </li> <li>Creating additional DWC columns for known values</li> </ul></ol> |
|	VIC	|	Sensitive	||<ol><li> GIS files (zip) provided</li> <li>Required data in  .SHP file</li> <li>Data processed including: </li><ul> <li>Extract .SHP data to dataframe</li> <li>Save to CSV</li> <li>Deleting data without a status</li> <li>Mapping DWC terms</li> <li>Mapping provided status to status codes</li> li>Rearanging data and encoding-decoding formatting</li> <li>Creating additional DWC columns for known values</li> </ul></ol> |
|	VIC	|	Conservation	|Webpage	|<ol><li> xxxxx</li> <li>xxxxxx</li> <li>Data processed including: </li> <li>Creating additional DWC columns for known values</li> </ul></ol> |
|	WA|	Sensitive	|Webpage	|<ol><li> xxxxx</li> <li>xxxxxx</li> <li>Data processed including: </li> <li>Creating additional DWC columns for known values</li> </ul></ol> |
|	WA|	Conservation	|Webpage	|<ol><li> xxxxx</li> <li>xxxxxx</li> <li>Data processed including: </li> <li>Creating additional DWC columns for known values</li> </ul></ol> |
