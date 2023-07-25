# convert all python files in the folder in ipynb using ipynb-py-convert
for f in *.py; do
    ipynb-py-convert $f ../examples/${f%.*}.ipynb
done
