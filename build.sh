rm -rf build/ dist/ py_redis.egg-info/
python setup.py sdist bdist_wheel
twine upload dist/*
