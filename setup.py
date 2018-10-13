from setuptools import setup, find_packages

setup(
    name="flexdata",
    package_dir={'flexdata': 'flexdata'},
    packages=find_packages(),

    install_requires=[
    "numpy",
    "tqdm",
    "scipy",
    "transforms3d",
    "flexdata",
    "flextomo"],

    version='0.0.1',
)