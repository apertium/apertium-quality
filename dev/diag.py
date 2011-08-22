#!/usr/bin/env python3
from __future__ import print_function
import sys
print(sys.version)
print()
print(sys.path)
print()
try:
	import lxml
	print("lxml: yes")
except:
	print("lxml: no")

try:
	import nltk
	print("nltk: yes")
except:
	print("nltk: no")

try:
	import yaml
	print("yaml: yes")
except:
	print("yaml: no")

