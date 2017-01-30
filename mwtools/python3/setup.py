try: 
	import distribute_setup
	distribute_setup.use_setuptools()
except: pass

from setuptools import setup, find_packages
from os import listdir

setup(
	name = "mwtools",
	version = "0.7",
	url = "https://github.com/bbqsrc/mwtools",
	download_url='https://github.com/bbqsrc/mwtools/archives/master',
	packages = ["mwtools"],
	provides = ["mwtools"],
	author = "Brendan Molloy",
	author_email = "brendan@bbqsrc.net",
	description = """Parses Mediawiki syntax into readable plain-text suitable
	for linguistic purposes.""",
	license = "CC0",
	keywords = ["mwtools", "mediawiki", "wikipedia", "parser"],
	classifiers=[
    "Development Status :: 4 - Beta",
    "Operating System :: OS Independent",
	"License :: Public Domain",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.1",
    "Programming Language :: Python :: 3.2",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries :: Python Modules",
	"Topic :: Text Processing :: Linguistic",
    ]
	
)
