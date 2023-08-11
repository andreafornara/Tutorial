wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
if [ "$(uname)" == "Darwin" ]; then
    # Do something under Mac OS X platform
    if [ "$(uname -m)" == "x86_64" ]; then
        curl -O Miniconda3-latest.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
    elif [ "$(uname -m)" == "arm64" ]; then
        curl -O Miniconda3-latest.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh
    fi
elif [ "$(uname)" == "Linux" ]; then
    # Do something under Linux platform
    wget -O Miniconda3-latest.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
fi

bash Miniconda3-latest.sh -b  -p ./miniforge -f
source miniforge/bin/activate                                                    
python -m pip install -r requirements.txt