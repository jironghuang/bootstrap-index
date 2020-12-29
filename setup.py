#In this directory, type pip install .
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='bootstrapindex',
      version='0.1.2',
      description='Returns block bootstrap indexes for walk-forward analysis (expanding or sliding window)',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/jironghuang/bootstrap-index",
      packages=['bootstrapindex'],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",],
      python_requires='>=3.6',      
      author = 'Jirong Huang',
      author_email = 'jironghuang88@gmail.com',
      zip_safe=False)

