from setuptools import setup, find_packages

setup(
    name='AS_SQL',
    version='1.0.0',
    author='Akihiro-Shiotani',
    packages=find_packages(),
    install_requires=['requests'],
    include_package_data=True,
)