# eGauge 2015
## Description
The goal is to extract individual device power consumption from eGauge data sets to eventually make them available to the research community.
## Building
Using conda for package management. [Here](http://conda.pydata.org/docs/using/envs.html) is a basic tutorial.
### Create environment from file
`conda env create -f environment.yml`
### Update environment from file
`conda env update -f environment.yml`
### Activate the environment
Linux, OS X: `source activate egauge-data-env`

Windows: `activate egauge-data-env`
### Deactivate the environment
Linux, OS X: `source deactivate egauge-data-env` or `source deactivate`

Windows: `deactivate egauge-data-env`
### Install a new package
Make sure egauge-data-env is the active environment.

`conda install package_name`
### Export the environment to a file
Make sure egauge-data-env is the active environment.

`conda env export > environment.yml`
