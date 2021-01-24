import setuptools

# build
# python setup.py sdist bdist_wheel
# twine upload --repository testpypi dist/* or twine upload dist/*

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name='pylsci',
    version='1.0.0',
    author='Pascal Keilbach',
    author_email='python@pk17.org',
    description='Python Package for Laser Speckle Contrast Imaging',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/pkeilbach/pylsci',
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
