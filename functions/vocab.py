# ---------------------------------------------------------------------------
# vocab.py
# 
# This script contains all of the variables that don't change for the lists 
# update that will eventually run weekly.
# 
# NOTE: Do not include SA - they manage their own lists.
# ---------------------------------------------------------------------------

authorize_url = "https://auth-secure.auth.ap-southeast-2.amazoncognito.com/oauth2/authorize"
token_url = "https://auth-secure.auth.ap-southeast-2.amazoncognito.com/oauth2/token"

# URLs for ALA lists for test and production
listsProd = "https://lists.ala.org.au/ws/speciesListItems/"
listsTest = "https://lists-test.ala.org.au/ws/speciesListItems/"
urlSuffix = "?max=10000&includeKVP=true"

# urls for conservation lists
conservation_list_urls = {"Australian Capital Territory": ["https://www.data.act.gov.au/resource/9ikf-qahj.json"], # or is this correct?
             "New South Wales": ["https://data.bionet.nsw.gov.au/biosvcapp/odata/SpeciesNames"],
             "Northern Territory": ["https://ftp-dlrm.nt.gov.au/main.html?download&weblink=1e717d654034af5e5f840d2ba3fd9187&realfilename=NT_Species_List_Fauna.xlsx", #fauna
                                    "https://ftp-dlrm.nt.gov.au/main.html?download&weblink=60088e77ecef6c6cbf515c299f07a420&realfilename=NT_Species_List_Flora.xlsx"], #flora
             "Queensland": ["https://apps.des.qld.gov.au/data-sets/wildlife/wildnet/species.csv"],
             "Tasmania": ["https://nre.tas.gov.au/Documents/TasThreatenedSpecies.xls.xlsx"],
             "Victoria": ["https://vba.biodiversity.vic.gov.au/vba/downloadVSC.do"],
             "Western Australia": ["https://www.dbca.wa.gov.au/management/threatened-species-and-communities"],
             "EPBC": ["https://data.gov.au/data/dataset/threatened-species-state-lists/resource/78401dce-1f40-49d3-92c4-3713d6e34974"]} 

# urls for relevant sensitive lists
sensitive_list_urls = {"New South Wales": ["https://data.bionet.nsw.gov.au/biosvcapp/odata/SpeciesNames"],
             "Queensland": ["https://apps.des.qld.gov.au/data-sets/wildlife/wildnet/qld-confidential-species.csv"],
             "Victoria": ["https://vba.biodiversity.vic.gov.au/vba/downloadVSC.do"], ### TODO: check on this
             "Western Australia": ["https://www.dbca.wa.gov.au/management/threatened-species-and-communities"]}

# all the state lists that are automatically checked every week
conservation_lists = ["Queensland",
         "Northern Territory",
         "New South Wales",
         "Western Australia",
         "Australian Capital Territory", ## Done - sensitive managed by org
         "Tasmania", ## Done - sensitive managed by org
         "Victoria", #authentication error]
         "EPBC"
         ]

sensitive_lists = ["New South Wales",
                    "Queensland",
                    "Victoria",
                    "Western Australia"]

# ALA list ids for all conservation authoritative lists on test
list_ids_conservation_test = {"Australian Capital Territory": "dr649",
                              "New South Wales": "dr650",
                              "Northern Territory": "dr651",
                              "Queensland": "dr652",
                              "South Australia": "dr653",
                              "Tasmania": "dr654",
                              "Victoria": "dr655",
                              "Western Australia": "dr2201",
                              "EPBC": "dr656"}

# ALA list ids for all conservation authoritative lists on prod
list_ids_conservation_prod = {"Australian Capital Territory": "dr649",
                              "New South Wales": "dr650",
                              "Northern Territory": "dr651",
                              "Queensland": "dr652",
                              "Tasmania": "dr654",
                              "Victoria": "dr655",
                              "Western Australia": "dr2201",
                              "EPBC": "dr656"}

# ALA list ids for all sensitive authoritative lists on test we are updating
list_ids_sensitive_test = {"New South Wales": "dr18457",
                           "Queensland": "dr18404",
                           "Victoria": "dr18669",
                           "Western Australia": "dr18406"}

# ALA list ids for all sensitive authoritative lists on test we are updating
list_ids_sensitive_prod = {"New South Wales": "dr487",
                           "Queensland": "dr493",
                           "Victoria": "dr490",
                           "Western Australia": "dr467"}

list_names_sensitive_test = {"New South Wales": "NSW Sensitive Species List",
                             "Queensland": "Queensland Confidential Species",
                             "Victoria": "Victorian Restricted Species List",
                             "Western Australia": "Western Australia: Sensitive Species"}

list_names_conservation_test = {"Australian Capital Territory": "Australian Capital Territory : Conservation Status",
                                "New South Wales": "New South Wales : Conservation Status",
                                "Northern Territory": "Northern Territory : Conservation Status",
                                "Queensland": "Queensland : Conservation Status",
                                "Tasmania": "Tasmania : Conservation Status",
                                "Victoria": "Victoria : Conservation Status",
                                "Western Australia": "Western Australia: Conservation Status",
                                "EPBC": "EPBC Act Threatened Species"}

# categories (from NSW?) to generalise
generalisation_categories = {"Category 3": "1km",
                             "Category 2": "10km",
                             "Category 1": "WITHHOLD"}

# other variables from NSW 
codeMap = {'C': 'LC', 'CR': 'CR', 'E': 'EN',
        'NT': 'NT','PE': 'EW', 'SL': 'SL',
        'V': 'VU'}
kingdomMap = {'animals':'Animalia','plants':'Plantae','fungi':'Fungi'}
classMap = {'AMPHIBIAN': 'Amphibia', 
            'MAMMAL': 'Mammalia', 
            'INVERTEBRATE': '', 
            'FISH': '', 
            'BIRD': 'Aves', 
            'REPTILE': 'Reptilia'}

# columns to rename for both sensitive and conservation lists
conservation_columns_rename = {"Queensland": {'Scientific_name':'scientificName',
                                              'Common_name': 'vernacularName',
                                              'Taxon_author':'scientificNameAuthorship',
                                              'Family': 'family',
                                            #   'NCA_status':'status',
                                            #   'Code_description':'status',
                                              'Taxon_Id':'WildNetTaxonID'},
                               "Northern Territory": {'TERRITORY PARKS AND WILDLIFE ACT CLASSIFICATION': 'status',
                                                      'COMMON NAME': 'vernacularName',
                                                      'FAMILY': 'family', 
                                                      'GENUS': 'genus', 
                                                      'SPECIES': 'species'},
                               "New South Wales": {},
                               "Western Australia": {},
                               "Australian Capital Territory": {'scientificname': 'scientificName',
                                                                'vernacularname': 'vernacularName',
                                                                'sourcestatus': 'sourceStatus',
                                                                'taxonrank': 'taxonRank'},
                               "Tasmania": {'Scientific name': 'scientificName', 
                                            'Common name': 'vernacularName',
                                            'Current TSPA schedule classification': 'status',
                                            'Category': 'sourceStatus',
                                            'Family': 'family'},
                               "Victoria": {'FFG_ACT_STATUS': 'status',
                                            'SCIENTIFIC_NAME': 'scientificName', 
                                            'COMMON_NAME': 'vernacularName'},
                               "EPBC": {'Scientific Name': 'scientificName',
                                        'Common Name': 'vernacularName',
                                        'Threatened status': 'sourceStatus',
                                        'Family': 'family',
                                        'Genus': 'genus',
                                        'Species': 'species'}}

sensitive_columns_rename = {"New South Wales": {},
                            "Queensland": {'Scientific name':'scientificName',
                                           'Common name': 'vernacularName',
                                           'NCA status': 'category', 
                                           'Taxon Id':'WildNetTaxonID',
                                           'Code_description':'status',
                                           'Kingdom':'kingdom',
                                           'Family':'family'},
                            "Victoria": {'VIC_ADVISORY_STATUS': 'category',
                                         'SCIENTIFIC_NAME': 'scientificName', 
                                         'COMMON_NAME': 'vernacularName'},
                            "Western Australia": {}}

# key word to get values out if list is coming from API
api_values = {"New South Wales": "value"}

conservation_species_corrections = {
    "Tasmania": {
        "Prasophyllum sp. Arthurs Lake": "Prasophyllum sp. Arthurs Lake (R.Smith DLJ11363) Tas. Herbarium"
        },
    "Victoria": {
        "Rytidosperma aff. caespitosum (South-west swamps)": "Rytidosperma sp. South-west Swamps (A.C.Beauglehole 22255) Vic. Herbarium",
        "Epacris microphylla/rhombifolia spp. agg.": "Epacris rhombifolia (L.R.Fraser & Vickery) Menadue",
        "Dianella sp. aff. longifolia (Riverina)": "Epacris rhombifolia (L.R.Fraser & Vickery) Menadue",
        "Prasophyllum aff. pyriforme (Inglewood)": "Prasophyllum maccannii D.L.Jones & D.T.Rouse",
        "Prasophyllum aff. odoratum E": "Prasophyllum odoratum R.S.Rogers",
        "Prasophyllum aff. pyriforme B": "Prasophyllum maccannii D.L.Jones & D.T.Rouse",
        "Prasophyllum aff. sphacelatum (Cobberas)": "Prasophyllum sphacelatum D.L.Jones",
        "Hestiochora rufiventris": "Myrtartona rufiventris (Walker, 1854)",
        "Prasophyllum aff. odoratum I": "Prasophyllum odoratum R.S.Rogers",
        "Podocarpus aff. lawrencei (Goonmirk Rocks)": "Podocarpus lawrencei Hook.f.",
        "Dianella sp. aff. revoluta (Minjah)": "Dianella revoluta R.Br. var. revoluta",
        "Prasophyllum aff. odoratum H": "Prasophyllum odoratum R.S.Rogers",
        "Pterostylis sp. aff. boormanii (Beechworth)": "Pterostylis sp. Beechworth (J.Galbraith s.n., MEL 2117497) Vic. Herbarium",
        "Porzana pusilla": "Zapornia pusilla (Pallas, 1776)",
        "Prasophyllum aff. parviflorum (SW Victoria)": "Prasophyllum sp. Limestone heath (A.C.Beauglehole 18714) Vic. Herbarium",
        "Prasophyllum aff. odoratum L": "Prasophyllum odoratum R.S.Rogers",
        "Pittosporum bicolor x undulatum": "Pittosporum bicolor Hook. x Pittosporum undulatum Vent.", ## start here
        "Prasophyllum aff. occidentale A": "Prasophyllum odoratum R.S.Rogers",
        "Diuris aff. pardina (Western Goldfields)": "Diuris calcicola R.J.Bates",
        "Eucalyptus aff. phenax (Jeparit)": "Eucalyptus dumosa A.Cunn. ex J.Oxley",
        "Calochilus sp. aff. campestris (Moondarra)": "Calochilus sp. 'Moondarra'",
        "Gemmabryum aff. clavatum (Mornington Peninsula)": "Bryum clavatum (Schimp.) Müll.Hal.",
        "Sida aff. corrugata (grey-leaf Boort form)": "Sida spodochroma F.Muell. ",
        "Prasophyllum aff. odoratum F": "Prasophyllum odoratum R.S.Rogers",
        "Thelymitra aff. ixioides (Western Victoria)": "Thelymitra J.R.Forst. & G.Forst.",
        "Cyanicula caerulea x Glossodia major hybrid": "Cyanicula Hopper & A.P.Br.",
        "Geranium aff. sp. 3": "Geranium sp. Narrow lobes (G.S.Lorimer 1771) Vic. Herbarium",
        "Arthropodium sp. 2 (greenish flowers)": "Arthropodium sp. South-east Highlands (N.G.Walsh 811) Vic. Herbarium",
        "Prasophyllum aff. diversiflorum (North-east)": "Prasophyllum sp. Balmattum (D.T.Rouse 223) Vic. Herbarium",
        "Caladenia aff. venusta (Tallageira)": "Caladenia venusta G.W.Carr",
        "Eucalyptus sp. aff. dumosa (Nhill)": "Eucalyptus dumosa A.Cunn. ex J.Oxley",
        "Poa sp. (Lake Omeo)": "Poa orba N.G.Walsh",
        "Candalides absimilis": "Eirmocides absimilis edwardsi (Braby, 2008)",
        "Pterostylis sp. aff. striata (Silurian)": "Pterostylis striata Fitzg.",
        "Chiloglottis aff. valida (Alpine)": "Chiloglottis valida D.L.Jones",
        "Prasophyllum aff. odoratum (Chewton)": "Prasophyllum odoratum R.S.Rogers",
        "Pterostylis aff. alpina (Wilsons Promontory)": "Pterostylis sp. 'Wilsons Promontory'",
        "Prostanthera lasianthos x spinosa": "Prostanthera lasianthos Labill. x Prostanthera spinosa F.Muell.",
        "Eucalyptus aff. ignorabilis (Lerderderg)": "Eucalyptus ignorabilis L.A.S.Johnson & K.D.Hill",
        "Campylopus robillardei": "Campylopus perauriculatus Broth.",
        "Corybas sp. aff. diemenicus (Wilsons Promontory)": "Corybas sp. Wilsons Promontory Vic. Herbarium",
        "Carex aff. tereticaulis (Lake Omeo)": "Carex tereticaulis F.Muell.",
        "Leucoloma leichardtii": "Dicranoloma leichhardtii (Hampe) Watts & Whitel.",
        "Alternanthera sp. 1 (Plains)": "Alternanthera sp. A Flora of New South Wales (M.Gray 5187) J.Palmer",
        "Eucalyptus sp. aff. odorata (Tarranginnie)": "Eucalyptus microcarpa (Maiden) Maiden",
        "Prasophyllum aff. frenchii (Wilsons Promontory)": "Prasophyllum frenchii F.Muell.",
        "Eucalyptus aff. cyanophylla (Antwerp)": "Eucalyptus dumosa A.Cunn. ex J.Oxley",
    },
    "New South Wales": {
        "Diuris sp. (Oaklands, D.L. Jones 5380)": "Diuris sp. Oaklands (Jones 5380) NSW Herbarium",
        "Bertya sp. (Chambigne NR, M. Fatemi 24)": "Bertya sp. Chambigne NR (M.Fatemi 24) NE Herbarium",
        "Bertya sp. (Clouds Creek, M. Fatemi 4)": "Bertya sp. Clouds Creek (M.Fatemi 4) NE Herbarium"
    },
    "Northern Territory": {
        "Heliotropium discorde": "Heliotropium discors Craven",
        "Synostemon sp. mann river": "Sauropus sp. Mann River (I.D.Cowie 8724) NT Herbarium", 
        "Varanus indicus": "Varanus chlorostigma (Gray, 1831)",
        "Cantharellus affin. lateritius": "Cantharellus Adans. ex Fr.",
        "Ogyris doddi": "Ogyris iphis doddi Waterhouse & Lyell, 1914",
        "Oldenlandia sp. central ranges": "Oldenlandia sp. Central ranges (P.K.Latz 8076) NT Herbarium",
        "Corynotheca sp. ridged seeds": "Corynotheca micrantha var. divaricata R.J.F.Hend.", 
        "Phyllanthus sp. broad smooth seeds": "Phyllanthus sp. Broad smooth seeds (M.D.Kimbel 52) Albr. & Cowie",
        "Haemodorum sp. red flowers": "Haemodorum sp. Red flowers (N.B.Byrnes 34) WA Herbarium", ### start here
        "Dasycercus hillieri": "Dasycercus cristicauda (Krefft, 1867)",
        "Actinoschoenus sp. deaf adder gorge": "Fimbristylis sp. Deaf Adder Gorge (C.R.Dunlop 4403) NT Herbarium",
        "Phyllanthus sp. narrow tuberculate seeds": "Phyllanthus sp. Narrow tuberculate seeds (D.E.Albrecht 7456) Albr. & Cowie",
        "Galactia sp. short inflorescence": "Galactia sp. Short inflorescence (R.A.Kerrigan 595) NT Herbarium",
        "Cyperus sp. red base": "Cyperus sp. Red base (C.R.Michell 3073) NT Herbarium",
        "Antechinomys longicaudatus": "Sminthopsis longicaudata Spencer, 1909",
        "Porzana tabuensis": "Zapornia tabuensis"
    },
    "Queensland": {
        "Lenwebbia sp. (Blackall Range P.R.Sharpe 5387)": "Lenwebbia sp. Blackall Range (P.R.Sharpe 5387) Qld Herbarium",
        "Phyllanthus sp. (Bulburin P.I.Forster+ PIF16034)": "Phyllanthus sp. Bulburin (P.I.Forster+ PIF16034) Qld Herbarium",
        "Lenwebbia sp. (Main Range P.R.Sharpe+ 4877)": "Lenwebbia sp. Main Range (P.R.Sharpe+ 4877) Qld Herbarium",
        "Gaudium venustum": "Leptospermum venustum A.R.Bean"
    },
    "Western Australia": {
        "Crendactylus tuberculatus": "Crenadactylus tuberculatus Doughty, Ellis & Oliver, 2016",
        "Microcorys sp. Mt Holland broad-leaf (G. Barrett s.n. PERTH 04104927)": "Microcorys sp. Mt Holland broad-leaf (G.Barrett s.n. PERTH 04104927) WA Herbarium",
        "Thryptomene sp. Wandana (M.E. Trudgen MET 22016)": "Thryptomene sp. Wandana (M.E.Trudgen 22016) WA Herbarium",
        "Thomasia purpurea x solanacea": "Thomasia purpurea (W.T.Aiton) J.Gay x Thomasia solanacea (Sims) J.Gay",
        "Eucalyptus dielsii x platypus": "Eucalyptus dielsii C.A.Gardner x Eucalyptus platypus Hook.",
        "Tephrosia sp. Kununurra (T. Handasyde TH00 250)": "Tephrosia sp. Kununurra (T.Handesyde TH00 250) Cowie & R.Butcher",
        "Pterostylis argillacea": "Pterostylis sp. 'Murchison'",
        "Hibiscus calcareus": "Hibiscus krichauffianus F.Muell.",
        "Solanum sp. Longini (C.T. Martine et al. CTM 805)": "Solanum sp. Longini (C.T.Martin 807 et al.)",
        "Eucalyptus buprestium x ligulata": "Eucalyptus buprestium x Eucalyptus ligulata",
        "Eucalyptus macrocarpa x pyriformis": "Eucalyptus macrocarpa x Eucalyptus pyriformis",
        "Eucalyptus absita x loxophleba": "Eucalyptus absita Grayling & Brooker x Eucalyptus loxophleba Benth.",
        "Acacia monticola x tumida var. kulparn": "Acacia monticola J.M.Black x Acacia tumida var. kulparn M.W.McDonald",
        "Calandrinia sp. Hamelin Station (F. Obbens FO 02/20) PN": "Calandrinia sp. Hamelin Station (F.Obbens FO 02/20) WA Herbarium",
        "Gaudium confertum": "Leptospermum confertum Joy Thomps.",
        "Chamelaucium sp. Coolcalalaya (A.H. Burbidge 4233)": "Chamelaucium sp. Coolcalalya (A.H.Burbidge 4233) WA Herbarium",
        "Eucalyptus marginata x megacarpa": "Eucalyptus marginata x Eucalyptus megacarpa",
        "Tribulopis sp. Koolan Island (K.F. Kenneally 8278)": "Tribulopis sp. Koolan Island (K.F.Kenneally 8728) R.M.Barker",
        "Pterostylis arida": "Pterostylis sp. scooped sepals (G.Brockman GBB386)",
        "Apectospermum macgillivrayi": "Leptospermum macgillivrayi Joy Thomps.",
        "Eucalyptus buprestium x staeri": "Eucalyptus buprestium x Eucalyptus staeri",
        "Eucalyptus buprestium x erectifolia": "Eucalyptus buprestium x Eucalyptus erectifolia",
        "Goodenia sp. South Coast (A.R. Annels ARA 1846)": "Goodenia sp. South Coast (A.R.Annels 1846) WA Herbarium",
        "Erpodium coronatum var. australiense": "Venturiella coronata subsp. australiensis (I.G.Stone) Pursell",
        "Styphelia howatharra": "Leucopogon sp. Howatharra (D. & N.McFarland 1046) WA Herbarium",
        "Helicteres sp. Beverley Springs (R.L. Barrett RLB 750)": "Helicteres sp. Beverley Springs (R.L.Barrett 750) WA Herbarium",
        "Isopogon elatus": "Isopogon sp. Ravensthorpe (D.B.Foreman 1207) WA Herbarium",
        "Eutaxia sp. North Ironcap (P. Armstrong PA 06/898)": "Eutaxia sp. North Ironcap (P.Armstrong et al. 06/898) WA Herbarium",
        "Styphelia microcardia": "Leucopogon sp. Bremer Bay (K.R.Newbey 4667) WA Herbarium",
        "Hibbertia arenicola": "Hibbertia Andrews",
        "Hibbertia lanulipes": "Hibbertia Andrews",
        "Glycine sp. Yampi (J.P. Bull & D. Brearley ONS-4790) PN": "Glycine Willd.",
        "Hemiandra sp. Windy Harbour (B.J. Conn & J.A. Scott BJC 3344)": "Hemiandra sp. Windy Harbour (B.J.Conn 3344 & J.A.Scott) WA Herbarium",
        "Geleznowia narcissoides": "Geleznowia sp. Binnu (K.A.Shepherd & J.Wege KS 1301) WA Herbarium",
        "Exocarpos acerbus": "Omphacomeria acerba (R.Br.) A.DC.",
        "Styphelia brachygyna": "Leucopogon sp. Murchison (R.J.Cranfield 9224) WA Herbarium",
        "Conostylis seorsiflora subsp. Nyabing (A. Coates s.n. 2/10/1988)": "Conostylis seorsiflora subsp. Nyabing (A.Coates s.n. 2/10/1998) WA Herbarium",
        "Grevillea wickhamii subsp. Prince Regent (R.L. Barrett & M.D. Barrett RLB 3952) PN": "Grevillea wickhamii Meisn.",
        "Abutilon sp. Onslow (F. Smith s.n. 10/9/61)": "Abutilon sp. Onslow (F.Smith s.n. 10/09/1961) WA Herbarium",
        "Lindernia sp. Minute-flowered (A.S. George 12433)": "Lindernia sp. Minute-flowered (A.S.George 12433) WA Herbarium",
        "Apectospermum exsertum": "Leptospermum exsertum Joy Thomps.",
        "Eucalyptus loxophleba x wandoo": "Eucalyptus loxophleba x Eucalyptus wandoo",
        "Eucalyptus buprestium x marginata": "Eucalyptus buprestium F.Muell. x Eucalyptus marginata Donn ex Sm.",
        "Hibiscus sp. Gurinbiddy Range (M.E. Trudgen MET 15708)": "Hibiscus sp. Gurinbiddy Range (M.E.Trudgen 15708) WA Herbarium",
        "Andersonia sp. Mitchell River (B.G. Hammersley 925)": "Andersonia sp. Mitchell River (B.G.Hammersley 925) WA Herbarium",
        "Eucalyptus preissiana x staeri": "Eucalyptus preissiana x Eucalyptus staeri",
        "Mirbelia sp. Ternata (M.D. Crisp & L.G. Cook MDC 9267)": "Mirbelia sp. Ternata (M.D.Crisp & L.G.Cook MDC 9267) WA Herbarium"
    },
    "EPBC": {
        "Hypseleotris gymnocephala": "Hypseleotris Gill, 1863",
        "Pityrodia sp. Marble Bar (G.Woodman & D.Coultas GWDC Opp 4)": "Pityrodia sp. Marble Bar (G.Woodman & D.Coultas GWDS Opp 4) WA Herbarium"
    },
    "Australian Capital Territory": {}
}

sensitive_species_corrections = {
    "Queensland": {
        "Dendrobium kingianum x D.speciosum": "Dendrobium kingianum Bidwill ex Lindl. x Dendrobium speciosum Sm.",
        "Macrozamia lomandroides x M.pauli-guilielmi": "Macrozamia lomandroides - Macrozamia pauli-guilielmi",
        "Dendrobium discolor x D.nindii": "Dendrobium discolor x D.nindii"
    },
    "New South Wales": {
        "Diuris sp. (Oaklands, D.L. Jones 5380)": "Diuris sp. Oaklands (Jones 5380) NSW Herbarium"
    },
    "Victoria": {},
    "Western Australia": {
        "Crendactylus tuberculatus": "Crenadactylus tuberculatus Doughty, Ellis & Oliver, 2016",
        "Microcorys sp. Mt Holland broad-leaf (G. Barrett s.n. PERTH 04104927)": "Microcorys sp. Mt Holland broad-leaf (G.Barrett s.n. PERTH 04104927) WA Herbarium",
        "Thryptomene sp. Wandana (M.E. Trudgen MET 22016)": "Thryptomene sp. Wandana (M.E.Trudgen 22016) WA Herbarium",
        "Thomasia purpurea x solanacea": "Thomasia purpurea (W.T.Aiton) J.Gay x Thomasia solanacea (Sims) J.Gay",
        "Eucalyptus dielsii x platypus": "Eucalyptus dielsii C.A.Gardner x Eucalyptus platypus Hook.",
        "Tephrosia sp. Kununurra (T. Handasyde TH00 250)": "Tephrosia sp. Kununurra (T.Handesyde TH00 250) Cowie & R.Butcher",
        "Pterostylis argillacea": "Pterostylis sp. 'Murchison'",
        "Hibiscus calcareus": "Hibiscus krichauffianus F.Muell.",
        "Solanum sp. Longini (C.T. Martine et al. CTM 805)": "Solanum sp. Longini (C.T.Martin 807 et al.)",
        "Eucalyptus buprestium x ligulata": "Eucalyptus buprestium x Eucalyptus ligulata",
        "Eucalyptus macrocarpa x pyriformis": "Eucalyptus macrocarpa x Eucalyptus pyriformis",
        "Eucalyptus absita x loxophleba": "Eucalyptus absita Grayling & Brooker x Eucalyptus loxophleba Benth.",
        "Acacia monticola x tumida var. kulparn": "Acacia monticola J.M.Black x Acacia tumida var. kulparn M.W.McDonald",
        "Calandrinia sp. Hamelin Station (F. Obbens FO 02/20) PN": "Calandrinia sp. Hamelin Station (F.Obbens FO 02/20) WA Herbarium",
        "Gaudium confertum": "Leptospermum confertum Joy Thomps.",
        "Chamelaucium sp. Coolcalalaya (A.H. Burbidge 4233)": "Chamelaucium sp. Coolcalalya (A.H.Burbidge 4233) WA Herbarium",
        "Eucalyptus marginata x megacarpa": "Eucalyptus marginata x Eucalyptus megacarpa",
        "Tribulopis sp. Koolan Island (K.F. Kenneally 8278)": "Tribulopis sp. Koolan Island (K.F.Kenneally 8728) R.M.Barker",
        "Pterostylis arida": "Pterostylis sp. Paynes Find (G.Brockman GBB 526)",
        "Pterostylis arida": "Pterostylis sp. scooped sepals (G.Brockman GBB386)",
        "Apectospermum macgillivrayi": "Leptospermum macgillivrayi Joy Thomps.",
        "Eucalyptus buprestium x staeri": "Eucalyptus buprestium x Eucalyptus staeri",
        "Eucalyptus buprestium x erectifolia": "Eucalyptus buprestium x Eucalyptus erectifolia",
        "Goodenia sp. South Coast (A.R. Annels ARA 1846)": "Goodenia sp. South Coast (A.R.Annels 1846) WA Herbarium",
        "Erpodium coronatum var. australiense": "Venturiella coronata subsp. australiensis (I.G.Stone) Pursell",
        "Styphelia howatharra": "Leucopogon sp. Howatharra (D. & N.McFarland 1046) WA Herbarium",
        "Helicteres sp. Beverley Springs (R.L. Barrett RLB 750)": "Helicteres sp. Beverley Springs (R.L.Barrett 750) WA Herbarium",
        "Isopogon elatus": "Isopogon sp. Ravensthorpe (D.B.Foreman 1207) WA Herbarium",
        "Eutaxia sp. North Ironcap (P. Armstrong PA 06/898)": "Eutaxia sp. North Ironcap (P.Armstrong et al. 06/898) WA Herbarium",
        "Styphelia microcardia": "Leucopogon sp. Bremer Bay (K.R.Newbey 4667) WA Herbarium",
        "Hibbertia arenicola": "Hibbertia Andrews",
        "Hibbertia lanulipes": "Hibbertia Andrews",
        "Glycine sp. Yampi (J.P. Bull & D. Brearley ONS-4790) PN": "Glycine Willd.",
        "Hemiandra sp. Windy Harbour (B.J. Conn & J.A. Scott BJC 3344)": "Hemiandra sp. Windy Harbour (B.J.Conn 3344 & J.A.Scott) WA Herbarium",
        "Geleznowia narcissoides": "Geleznowia sp. Binnu (K.A.Shepherd & J.Wege KS 1301) WA Herbarium",
        "Exocarpos acerbus": "Omphacomeria acerba (R.Br.) A.DC.",
        "Styphelia brachygyna": "Leucopogon sp. Murchison (R.J.Cranfield 9224) WA Herbarium",
        "Conostylis seorsiflora subsp. Nyabing (A. Coates s.n. 2/10/1988)": "Conostylis seorsiflora subsp. Nyabing (A.Coates s.n. 2/10/1998) WA Herbarium",
        "Grevillea wickhamii subsp. Prince Regent (R.L. Barrett & M.D. Barrett RLB 3952) PN": "Grevillea wickhamii Meisn.",
        "Abutilon sp. Onslow (F. Smith s.n. 10/9/61)": "Abutilon sp. Onslow (F.Smith s.n. 10/09/1961) WA Herbarium",
        "Lindernia sp. Minute-flowered (A.S. George 12433)": "Lindernia sp. Minute-flowered (A.S.George 12433) WA Herbarium",
        "Apectospermum exsertum": "Leptospermum exsertum Joy Thomps.",
        "Eucalyptus loxophleba x wandoo": "Eucalyptus loxophleba x Eucalyptus wandoo",
        "Eucalyptus buprestium x marginata": "Eucalyptus buprestium F.Muell. x Eucalyptus marginata Donn ex Sm.",
        "Hibiscus sp. Gurinbiddy Range (M.E. Trudgen MET 15708)": "Hibiscus sp. Gurinbiddy Range (M.E.Trudgen 15708) WA Herbarium",
        "Andersonia sp. Mitchell River (B.G. Hammersley 925)": "Andersonia sp. Mitchell River (B.G.Hammersley 925) WA Herbarium",
        "Eucalyptus preissiana x staeri": "Eucalyptus preissiana x Eucalyptus staeri",
        "Mirbelia sp. Ternata (M.D. Crisp & L.G. Cook MDC 9267)": "Mirbelia sp. Ternata (M.D.Crisp & L.G.Cook MDC 9267) WA Herbarium"
    }
}

statuses_rename = {
    "Australian Capital Territory": {
        "Extinct": "Extinct",
        "Extinct in the Wild": "Extinct in the Wild",
        "Critically Endangered ": "Critically Endangered",
        "Endangered": "Endangered",
        "Vulnerable": "Vulnerable",
        "Regionally Conservation Dependent": "Conservation Dependent"
    },
    "EPBC Act": {
        "Extinct": "Extinct",
        "Extinct in wild": "Extinct in the Wild",
        "Extinct in the wild": "Extinct in the Wild",
        "Critically Endangered": "Critically Endangered",
        "Endangered": "Endangered",
        "Vulnerable": "Vulnerable",
        "Conservation dependent": "Conservation Dependent",
        "JAMBA CAMBA KAMBA": "Migratory",
        "CITES": "CITES"
    },
    "New South Wales": {
        "Extinct": "Extinct",
        "Critically Endangered": "Critically Endangered",
        "Endangered": "Endangered",
        "Vulnerable": "Vulnerable"
    },
    "Northern Territory": {
        "EX": "Extinct",
        "EW": "Critically Endangered",
        "CE": "Critically Endangered",
        "CR": "Critically Endangered",
        "EN": "Endangered",
        "VU": "Vulnerable",
        "NT": "Near Threatened",
        "LC": "Least concern",
        "DD": "Data Deficient",
        "NE": "Not Evaluated"
    },
    "Queensland": {
        "Extinct wildlife": "Extinct",
        "Extinct in the wild wildlife": "Extinct in the Wild",
        "Extinct in the wild": "Extinct in the Wild",
        "Critically endangered wildlife": "Critically Endangered",
        "Endangered wildlife": "Endangered",
        "Vulnerable wildlife": "Vulnerable",
        "Near threatened wildlife": "Near Threatened",
        "Special least concern wildlife": "Least concern",
        "Least concern wildlife": "Least concern",
        "International wildlife": "CITES"
    },
    "South Australia": {
        "Endangered": "Endangered",
        "Vulnerable": "Vulnerable",
        "Rare": "Near Threatened"
    },
    "Tasmania": {
        "Extinct": "Extinct",
        "Endangered": "Endangered",
        "Vulnerable": "Vulnerable",
        "Rare": "Near Threatened",
        "x": "Extinct",
        "e": "Endangered",
        "v": "Vulnerable",
        "r": "Near Threatened"
    },
    "Victoria": {
        "Extinct": "Extinct",
        "Extinct in the Wild": "Extinct in the Wild",
        "Endangered (Extinct in Victoria)": "Extinct in the Wild",
        "Critically Endangered": "Critically Endangered",
        "Endangered": "Endangered",
        "Endangered": "Vulnerable",
        "Conservation Dependent": "Conservation Dependent",
        "Restricted": "Restricted"
    },
    "Western Australia": {
        'CR':'Critically Endangered',
        'EN':'Endangered',
        'VU':'Vulnerable',
        'EX':'Extinct',
        'EW':'Extinct in the Wild',
        'SP':'Specially Protected',
        'MI':'Migratory',
        'CD':'Conservation Dependent',
        'CD & MI':'Conservation Dependent',
        'OS':'Other Specially Protected',
        'P1':'Priority 1: Poorly-known species',
        'P2':'Priority 2: Poorly-known species',
        'P3':'Priority 3: Poorly-known species',
        'P4':'Priority 4: Rare, Near Threatened',
        'MI & P1':'Priority 1: Poorly-known species',
        'MI & P3':'Priority 2: Poorly-known species',
        'MI & P4':'Priority 4: Rare, Near Threatened'
    },
    "EPBC": {
        "EX": "Extinct",
        "EW": "Extinct in the Wild",    
        "CR": "Critically Endangered",
        "EN": "Endangered",
        "VU": "Vulnerable",
        "CD": "Conservation dependent",
    }
}