from setuptools import setup, find_packages

with open("readme.md", "r") as fh:
    long_description = fh.read()

setup(
    name='aec6s',
    version='0.0.1',
    author='Yulun Wu',
    author_email='yulunwu8@gmail.com',
    description='Adjacency-effect correction following the Vermote et al. 1997 approach',
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3'
    ],
    python_requires='>=3.8',
    install_requires=['scipy','pandas','numpy','netCDF4']
)











