from setuptools import setup, find_packages

setup(
    name='data_pipeline',
    version='0.1.0',
    packages=find_packages(include=['pipeline*']),
    install_requires=[
        # List any dependencies here
    ],
)