import xml.etree.cElementTree as etree
from cStringIO import StringIO
from apertium_quality.core import whereis
from collections import defaultdict
from subprocess import *
from tempfile import NamedTemporaryFile
import urllib

class RegressionTest(object):
	ns = "{http://www.mediawiki.org/xml/export-0.3/}"
	program = "apertium"
	
	def __init__(self, url, mode, directory="."):
		if not whereis(self.program):
			raise IOError("Cannot find `%s`. Check $PATH." % self.program)	
		if not "Special:Export" in url:
			raise AttributeError("URL did not contain Special:Export.")
		self.mode = mode
		self.directory = directory
		self.tree = etree.parse(urllib.urlopen(url))
		self.passes = 0
		self.total = 0
		for e in self.tree.getroot().getiterator():
			if e.tag == self.ns + "title":
				self.title = e.text
			if e.tag == self.ns + "revision":
				self.revision = e[0].text # should be <id>
			if e.tag == self.ns + "text":
				self.text = e.text
		if not self.text:
			raise AttributeError("No text element?")
		self.tests = defaultdict(defaultdict)
		for i in self.text.split('\n'):
			if i[:4] == "* {{":
				x = i.strip("{}* ").split('|')
				y = x[2].strip()
				self.tests[x[1]][y if y[-1] == '.' else y+'[_].'] = x[3].strip()
		self.out = StringIO()
	
	def run(self):
		for side in self.tests:
			self.out.write("Now testing: %s\n" % side)
			args = '\n'.join(self.tests[side].keys()).encode('utf-8')
			app = Popen([self.program, '-d', self.directory, self.mode], stdin=PIPE, stdout=PIPE, stderr=PIPE)
			app.stdin.write(args)
			self.results = app.communicate()[0].decode('utf-8').split('\n')
			
			for n, test in enumerate(self.tests[side].items()):
				res = self.results[n].split("[_]")[0].strip().encode('utf-8')
				tes = test[1].strip().encode('utf-8')
				self.out.write("%s\t  %s\n" % (self.mode, tes))
				if res == tes:
					self.out.write("WORKS\t  %s\n" % res)
					self.passes += 1
				else:
					self.out.write("\t- %s\n" % tes)
					self.out.write("\t+ %s\n" % res)
				self.total += 1
				self.out.write('\n')

	def start(self):
		self.run()

	def get_output(self):
		print self.out.getvalue()
		if self.passes > 0 and self.total > 0: 
			print "Passes: %d/%d, Success rate: %.2f%%" % (self.passes, self.total, (float(self.passes) / float(self.total) * 100))
