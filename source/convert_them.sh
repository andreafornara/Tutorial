# convert all python files in the folder in ipynb using ipynb-py-convert
for f in *.py; do
    ipynb-py-convert $f ../examples/${f%.*}.ipynb
done


# for all ipnb in ../examples/ run them
# Path: source/convert_them.sh
for f in ../examples/*.ipynb; do
    jupyter nbconvert --to notebook --execute $f --output $f
done