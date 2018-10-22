from setuptools import setup, find_packages

setup(
    name="flexcalc",
    package_dir={'flexcalc': 'flexcalc'},
    packages=find_packages(),

    install_requires=[
    "numpy",
    "tqdm",
    "simpleitk",
    "scipy",
    "numpy-stl",
    "scikit-image",
    "transforms3d",
    "flexdata",
    "flextomo"],

    version='0.0.1',
)
