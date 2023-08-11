#check if the py files have been modified with the last commit
# if yes, convert them to ipynb and move them to the examples folder
# if not, do nothing
# if the ipynb files have been modified, run them and save the output
# if not, do nothing
for f in *.py; do
    if [[ $(git diff --name-only HEAD^ HEAD $f) ]]; then
        ipynb-py-convert $f ../examples/${f%.*}.ipynb
        jupyter nbconvert --to notebook --execute ../examples/${f%.*}.ipynb --output ../examples/${f%.*}.ipynb
    fi
done