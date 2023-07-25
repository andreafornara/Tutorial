wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
bash Miniforge3-Linux-x86_64.sh -b  -p ./miniforge -f
source miniforge/bin/activate                                                    
python -m pip install ipython jupyterlab numpy scipy pandas awkward matplotlib               
python -m pip install pyarrow pyyaml pytest cpymad  xsuite pyabel                                          
# python -m pip install sixtracktools                                                
python -m pip install NAFFlib   
