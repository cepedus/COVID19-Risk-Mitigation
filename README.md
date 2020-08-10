# COVID19 Risk Mitigation

Internship @ TAU team, INRIA Saclay
*Author: Martín Cepeda*

This repository holds the code for my internship subject "A mixed EPI-ECO environment for pandemic policy design". 

The main file `EPI_fitter.ipynb` defines a SEIR-inspired model and gets publicly available data from [Our World in Data](https://ourworldindata.org/coronavirus-source-data) and [Santé Publique France](https://www.data.gouv.fr/fr/datasets/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/). The model is then fitted using the [lmfit](https://lmfit-py.readthedocs.io/en/latest/index.html) library.

In order to make the model run, an initial guess of parameters must be given in `params.csv` at the root directory with the following columns: name, init_value, min, max