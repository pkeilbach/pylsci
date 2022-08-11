import setuptools


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


setuptools.setup(
    name="pylsci",
    version="1.0.4",
    author="Pascal Keilbach",
    author_email="dev@pk17.org",
    description="Python Package for Laser Speckle Contrast Imaging",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pkeilbach/pylsci",
    packages=["pylsci"],
    package_dir={"": "src"},
    install_requires=["numpy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
