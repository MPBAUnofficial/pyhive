from setuptools import setup
import hive

setup(
    name="hive",
    version=hive.__version__,
    description=open("README.md", 'r').read(),
    url="https://github.com/gigaroby/hive",
    author="Roberto Bampi",
    author_email="robampi@fbk.eu",
    packages=["hive"],
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: GPL License',
        'Operating System :: OS Indipendent',
        'Framework :: Django',
    ]
)

