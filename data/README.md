# Data presentation

## Sources

Data was collected from the following sources:

| #    | Name                                                         | Description                                                  | Link                                                         |
| ---- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| *1*  | Mobilités scolaires des individus : déplacements commune de résidence / commune de scolarisation en 2016 | From 2016 Census, shows origin-destination movements per household (with corrective factor computed by INSEE) for schooling | https://www.insee.fr/fr/statistiques/4171517?sommaire=4171558 |
| *2*  | Mobilités professionnelles des individus : déplacements commune de résidence / commune de travail en 2016 | From 2016 Census, shows origin-destination movements per household (with corrective factor computed by INSEE) for working | https://www.insee.fr/fr/statistiques/4171531?sommaire=4171558#consulter |
| *3*  | Régularité mensuelle TGV par liaisons                        | Number of planned/circulating trains per day in the 'TGV 'network | https://data.sncf.com/explore/dataset/regularite-mensuelle-tgv-aqst/table/?sort=periode |
| *4*  | Régularité mensuelle Intercités                              | Number of planned/circulating trains per day in the 'Intercités' network | https://data.sncf.com/explore/dataset/regularite-mensuelle-intercites/table/?sort=nombre_de_trains_a_l_heure_pour_un_train_en_retard |
| *5*  | Données hospitalières relatives à l'épidémie de COVID-19     | Daily indicators per department of hospitalized, in reanimation, sent to home and dead individuals registered in France hospitals | https://www.data.gouv.fr/fr/datasets/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/ |
| *6*  | Données relatives aux résultats des tests virologiques COVID-19 SI-DEP | Daily indicators per department of taken tests and positive tests | https://www.data.gouv.fr/fr/datasets/donnees-relatives-aux-resultats-des-tests-virologiques-covid-19/ |
| *7*  | Données relatives aux tests de dépistage de COVID-19 réalisés en laboratoire de ville | Daily indicators per department of taken tests and positive tests (old mechanism) | https://www.data.gouv.fr/fr/datasets/donnees-relatives-aux-tests-de-depistage-de-covid-19-realises-en-laboratoire-de-ville/ |
| *8*  | France: Coronavirus Pandemic                                 | Official data from France indicators of deaths, infected, estimated stringency factor of government policies among other indicators | https://ourworldindata.org/coronavirus/country/france?country=~FRA |
| *9*  | CAC 40                                                       | Price and volume of CAC 40 benchmark French stock market index | https://live.euronext.com/fr/product/indices/FR0003500008-XPAR |
| *10* | Consommation mensuelle des ménages en biens - Biens - Volumes aux prix de l'année précédente, chaînés depuis 2014 - Série CVS-CJO | French national consumption per sector and variations        | https://www.insee.fr/fr/statistiques/serie/010565753         |
| *11* | Tableaux de l'économie française Édition 2020 - Emploi par activité | French work distribution per sector                          | https://www.insee.fr/fr/statistiques/4277675?sommaire=4318291 |
| *12* | Comptes nationaux trimestriels - résultats détaillés (PIB) - premier trimestre 2020 | French PIB indicators                                        | https://www.insee.fr/fr/statistiques/4500941                 |
| *13* | Conditions de vie des ménages en période de confinement      | French confinement demographics                              | https://www.insee.fr/fr/statistiques/4476914                 |

## Available data

In `./clean/`, all in `.csv` format

| File name                                  | Source #     | Description                                                  |
| ------------------------------------------ | ------------ | ------------------------------------------------------------ |
| `ECO/CAC 40_quote_chart`                   | *9*          | CAC40 index and volume from 1987-12-03 to 2020-06-05, directly from *9* |
| `ECO/PIB_VA_variation_prixAnneePrecedente` | *12*         | Manually taken. Quarterly data on PIB decomposition (imports, spending, exports, demand, etc.) and variations per work sector w.r.t previous year's prices |
| `ECO/school_mobility`                      | *1*          | Computed by summing all pair-wise department movements and normalizing to 0-1 |
| `ECO/work_mobility`                        | *2*          | Computed by summing all pair-wise department movements and normalizing to 0-1 |
| `ECO/secteurs_age_sexe_2018`               | *11*         | Manually taken. Gives percentages per age group/gender and quantity of workers per work sector |
| `ECO/valeurs_mensuelles`                   | *10*         | Monthly cumulated household consumption from 2019-01 to 2020-04 |
| `EPI/france_departments`                   | *5, 6, 7, 8* | Time series from 2019-12-31 to 2020-06-08 of national/per department EPI indicators |

## TODO:

* Parse 3, 4
* Common timeline for EPI and ECO (daily & monthly/quarterly)