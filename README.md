<img src="https://github.com/matchms/matchmsextras/blob/main/images/matchmsextras_logo.png" width="600">

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/matchms/matchmsextras/CI_build.yml?branch=main)
![GitHub](https://img.shields.io/github/license/matchms/matchmsextras)
[![PyPI](https://img.shields.io/pypi/v/matchmsextras?color=blue)](https://pypi.org/project/matchmsextras/)

# matchmsextras

Additional functionalities to be used with [matchms](https://github.com/matchms/matchms).

Usually this is stuff which either in scope and/or in code quality and/or in degree of unit testing does not match the criteria we have for matchms.
For producing the results shown in our [Spec2Vec article, PLoS Computational Biology, 2021](https://doi.org/10.1371/journal.pcbi.1008724) we used code from `matchmsextras 0.1.0`. To fully reproduce those results you can install this via `pip install matchmsextras==0.1.0`. For all other purposes we recommend using the latest release.

## Installation

```
pip install matchmsextras
```

## Citing us
If you use **matchmsextras** for your research, please cite the following references:

Huber F, Ridder L, Verhoeven S, Spaaks JH, Diblen F, Rogers S, van der Hooft JJJ, (2021) "Spec2Vec: Improved mass spectral similarity scoring through learning of structural relationships". PLoS Comput Biol 17(2): e1008724. https://doi.org/10.1371/journal.pcbi.1008724

F. Huber, S. Verhoeven, C. Meijer, H. Spreeuw, E. M. Villanueva Castilla, C. Geng, J.J.J. van der Hooft, S. Rogers, A. Belloum, F. Diblen, J.H. Spaaks, (2020). "matchms - processing and similarity evaluation of mass spectrometry data". Journal of Open Source Software, 5(52), 2411, https://doi.org/10.21105/joss.02411

Many extra thanks!

## Tutorial on matchms and Spec2Vec
Possibly the easiest way to learn how to run matchmsextras is to follow our tutorial on `matchms`.

+ [Part I - Import and process MS/MS data using matchms](https://blog.esciencecenter.nl/build-your-own-mass-spectrometry-analysis-pipeline-in-python-using-matchms-part-i-d96c718c68ee)
+ [Part II - Compute spectral similarity using Spec2Vec](https://blog.esciencecenter.nl/build-a-mass-spectrometry-analysis-pipeline-in-python-using-matchms-part-ii-spec2vec-8aa639571018)
+ [Part III - Create molecular networks from Spec2Vec similarities](https://blog.esciencecenter.nl/build-a-mass-spectrometry-analysis-pipeline-in-python-using-matchms-part-iii-molecular-91891248ee34)
