# vsphere-api-test
Testing vSphere API.

Instructions.
1. Install Poetry project management tool
1. `poetry install` to install dependencies from poetry.lock
1. `eval $(poetry env activate)` to activate the virtual environment
1. Create a `.env` file with:
```
VSPHERE_URI=
VSPHERE_USERNAME=
VSPHERE_PASSWORD=
```
1. `python vsphere_test.py` to execute the script
