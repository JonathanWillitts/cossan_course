# COSSAN Course
Useful scripts for the Uncertainty Quantification on HPC with COSSAN Software course. 

## Install COSSAN-X (install_cossan.py)

To install, first download the installer script:
```sh
wget https://raw.githubusercontent.com/JonathanWillitts/cossan_course/master/install_cossan.py
```

Next update the line specifying the SMARX dongle license server (and any other required config parameters) in `install_cossan.py`:
```python
SMARX_SERVER = 'hostname.or.ip.to.smarx.server'
```
 
Then run the install script, noting:
* It may take 10+ mins to fully run.
* There is no successful message, though the script should exit early with an error if it encounters a problem.
```sh
python install_cossan.py
````

Finally change to the COSSAN-X install directory and launch, e.g.
```sh
cd ~/cossanx/COSSANX_Linux_R2014a
./start_cossan.sh
``` 
The GUI should load up (though can take a minute to initialise on first run).
