from setuptools import setup
import pyhive

setup(
    name="pyhive",
    version=pyhive.__version__,
    description=open("README.md", 'r').read(),
    url="https://github.com/MPBAUnofficial/hive",
    author="Roberto Bampi",
    author_email="robampi@fbk.eu",
    packages=["pyhive", "pyhive.extra", "pyhive.extra.django"],
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: GPL License',
        'Operating System :: OS Indipendent',
    ],
)

