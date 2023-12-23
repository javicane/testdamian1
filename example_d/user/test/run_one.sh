#export PATH=python binary:$PATH
#export PYTHONPATH=$PYTHONPATH:----/lib

which coverage
coverage run -m  unittest $1
#coverage report -m
