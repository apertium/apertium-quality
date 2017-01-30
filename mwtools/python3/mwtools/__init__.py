#import xml.etree.ElementTree as etree
from io import StringIO
from collections import deque, defaultdict
import re

symbols = {
	'&diams;': '\u2666',
	'&Ecirc;': '\xca',
	'&Theta;': '\u0398',
	'&Lambda;': '\u039b',
	'&raquo;': '\xbb',
	'&sum;': '\u2211',
	'&oacute;': '\xf3',
	'&iota;': '\u03b9',
	'&Sigma;': '\u03a3',
	'&atilde;': '\xe3',
	'&agrave;': '\xe0',
	'&nbsp;': ' ',
	'&Gamma;': '\u0393',
	'&Auml;': '\xc4',
	'&Ouml;': '\xd6',
	'&Egrave;': '\xc8',
	'&acute;': '\xb4',
	'&supe;': '\u2287',
	'&lsquo;': '\u2018',
	'&deg;': '\xb0',
	'&middot;': '\xb7',
	'&upsilon;': '\u03c5',
	'&ocirc;': '\xf4',
	'&Ugrave;': '\xd9',
	'&ndash;': '\u2013',
	'&psi;': '\u03c8',
	'&gt;': '>',
	'&notin;': '\u2209',
	'&lambda;': '\u03bb',
	'&hearts;': '\u2665',
	'&sigmaf;': '\u03c2',
	'&ge;': '\u2265',
	'&uml;': '\xa8',
	'&aring;': '\xe5',
	'&sub;': '\u2282',
	'&iexcl;': '\xa1',
	'&Aacute;': '\xc1',
	'&zeta;': '\u03b6',
	'&ne;': '\u2260',
	'&trade;': '\u2122',
	'&igrave;': '\xec',
	'&aelig;': '\xe6',
	'&there4;': '\u2234',
	'&asymp;': '\u2248',
	'&uarr;': '\u2191',
	'&gamma;': '\u03b3',
	'&yen;': '\xa5',
	'&times;': '\xd7',
	'&ouml;': '\xf6',
	'&epsilon;': '\u03b5',
	'&Prime;': '\u2033',
	'&egrave;': '\xe8',
	'&prime;': '\u2032',
	'&kappa;': '\u03ba',
	'&divide;': '\xf7',
	'&Igrave;': '\xcc',
	'&hArr;': '\u21d4',
	'&omega;': '\u03c9',
	'&ucirc;': '\xfb',
	'&Icirc;': '\xce',
	'&sigma;': '\u03c3',
	'&micro;': '\xb5',
	'&Ccedil;': '\xc7',
	'&Xi;': '\u039e',
	'&Omega;': '\u03a9',
	'&sup;': '\u2283',
	'&larr;': '\u2190',
	'&prod;': '\u220f',
	'&rsaquo;': '\u203a',
	'&Ucirc;': '\xdb',
	'&lsaquo;': '\u2039',
	'&amp;': '&',
	'&uuml;': '\xfc',
	'&yuml;': '',
	'&uacute;': '\xfa',
	'&ecirc;': '\xea',
	'&theta;': '\u03b8',
	'&laquo;': '\xab',
	'&infin;': '\u221e',
	'&dagger;': '\u2020',
	'&not;': '\xac',
	'&Ograve;': '\xd2',
	'&oslash;': '\xf8',
	'&Uuml;': '\xdc',
	'&permil;': '\u2030',
	'&cedil;': '\xb8',
	'&plusmn;': '\xb1',
	'&AElig;': '\xc6',
	'&loz;': '\u25ca',
	'&icirc;': '\xee',
	'&alpha;': '\u03b1',
	'&auml;': '\xe4',
	'&xi;': '\u03be',
	'&szlig;': '\xdf',
	'&spades;': '\u2660',
	'&euml;': '\xeb',
	'&pi;': '\u03c0',
	'&bull;': '\u2022',
	'&phi;': '\u03c6',
	'&isin;': '\u2208',
	'&iquest;': '\xbf',
	'&equiv;': '\u2261',
	'&lt;': '<',
	'&eacute;': '\xe9',
	'&ntilde;': '\xf1',
	'&le;': '\u2264',
	'&clubs;': '\u2663',
	'&pound;': '\xa3',
	'&Phi;': '\u03a6',
	'&sbquo;': '\u201a',
	'&Iuml;': '\xcf',
	'&and;': '\u2227',
	'&rArr;': '\u21d2',
	'&Eacute;': '\xc9',
	'&Ntilde;': '\xd1',
	'&rsquo;': '\u2019',
	'&euro;': '\u20ac',
	'&rdquo;': '\u201d',
	'&delta;': '\u03b4',
	'&cap;': '\u2229',
	'&quot;': '"',
	'&sect;': '\xa7',
	'&radic;': '\u221a',
	'&tau;': '\u03c4',
	'&rho;': '\u03c1',
	'&Acirc;': '\xc2',
	'&ccedil;': '\xe7',
	'&prop;': '\u221d',
	'&mu;': '\u03bc',
	'&Delta;': '\u0394',
	'&nabla;': '\u2207',
	'&forall;': '\u2200',
	'&Iacute;': '\xcd',
	'&Dagger;': '\u2021',
	'&cup;': '\u222a',
	'&sube;': '\u2286',
	'&Aring;': '\xc5',
	'&darr;': '\u2193',
	'&macr;': '\xaf',
	'&ordm;': '\xba',
	'&Oslash;': '\xd8',
	'&Otilde;': '\xd5',
	'&alefsym;': '\u2135',
	'&part;': '\u2202',
	'&Uacute;': '\xda',
	'&reg;': '\xae',
	'&ordf;': '\xaa',
	'&omicron;': '\u03bf',
	'&nu;': '\u03bd',
	'&iuml;': '\xef',
	'&ugrave;': '\xf9',
	'&curren;': '\xa4',
	'&copy;': '\xa9',
	'&ldquo;': '\u201c',
	'&Atilde;': '\xc3',
	'&para;': '\xb6',
	'&Euml;': '\xcb',
	'&harr;': '\u2194',
	'&Pi;': '\u03a0',
	'&chi;': '\u03c7',
	'&ograve;': '\xf2',
	'&acirc;': '\xe2',
	'&int;': '\u222b',
	'&or;': '\u2228',
	'&aacute;': '\xe1',
	'&Agrave;': '\xc0',
	'&Oacute;': '\xd3',
	'&exist;': '\u2203',
	'&eta;': '\u03b7',
	'&Psi;': '\u03a8',
	'&oelig;': '\u0153',
	'&iacute;': '\xed',
	'&cent;': '\xa2',
	'&Ocirc;': '\xd4',
	'&mdash;': '\u2014',
	'&minus;': '\u2212',
	'&bdquo;': '\u201e',
	'&otilde;': '\xf5',
	'&beta;': '\u03b2',
	'&rarr;': '\u2192'
}

class MediawikiHandler(object):
	def __init__(self, data):
		self.data = data
		self.done = False
	
	def _first_pass(self):
		"""Whole page scan"""
		def unescape(d):
			regex = re.compile("(%s)" % "|".join(symbols.keys()))
			out = re.sub("&amp;", "&", d)
			while True:
				m = regex.search(out)
				if m is None:
					break
				out = re.sub(m.group(0), symbols[m.group(0)], out)
			return out

		def strip(d):
			regex = []
			# strip comments
			regex.append(r"\<\!\-\-.*\-\-\>")
			# strip refs
			regex.append(r"\<ref.*?\>(.*?)\<\/ref\>")
			# strip tables
			regex.append("\{\|.*\|\}")
			# strip font
			regex = re.compile(r"\'{2,5}")
			return regex.sub('', d)

		def mask_titles(d):
			# mark titles
			regex = re.compile(r"^(?<!=)(={1,6})([^=]+)\1(?!=)")
			return regex.sub(lambda x: "[%s]" % x.group(0), d)

		self.data = unescape(self.data)
		self.data = strip_comments(self.data)
		self.data = strip_refs(self.data)
		# STRIP OTHER
		self.data = strip_tables(self.data)
		self.data = strip_font(self.data)
		self.data = mask_titles(self.data)

	def _second_pass(self):
		"""Line by line scan"""
		## convert titles (=)
		## convert lists (*)
		## convert indents (:)
		## wrap paragraph blocks (\n\n)
		pass

	def _third_pass(self):
		class ElementHandler(object):
			STATE_SIZE = 2
			def __init__(self, document, tags):
				self.document = StringIO(document)
				self.start_tags = tags
				self.end_tags = {}
				for k, v in tags.items():
					self.end_tags[v] = k
				
				self.tags = defaultdict(list)
				self.out = StringIO()

			def parse(self):
				state = State(self.STATE_SIZE)
				#for ch in self.document.read():
				while True:
					ch = self.document.read(1)
					if ch == '':
						break
					state.set(ch)
					
					tag = state.get()
					if tag in self.start_tags.keys():
						begin = self.document.tell()
						self.tags[tag].append(begin)
						#print("BEG(%s): %s %s" % (tag, begin, self.tags[tag]))

					elif tag in self.end_tags.keys():
						tag = self.end_tags[tag]
						depth = len(self.tags[tag])
						end = self.document.tell()
						#print("END(%s): %s %s" % (self.start_tags[tag], end, self.tags[tag]))
						try:
							begin = self.tags[tag].pop()
						except:
							#print("ERR: no pop at %s" % end)
							continue

						p = -(state.maxlen)

						buf = []
						# first chunk
						self.document.seek(0)
						buf.append(self.document.read(begin - self.STATE_SIZE))

						# open tag
						buf.append(self.document.read(self.STATE_SIZE))

						# cur chunk
						self.document.seek(begin)
						buf.append(self.document.read(
							end-begin-self.STATE_SIZE))

						# close tag
						buf.append(self.document.read(self.STATE_SIZE))

						# end chunk
						buf.append(self.document.read())
						#print(buf)
						out = self.parse_element(tag, buf[2])
						
						self.document = StringIO(buf[0] + out + buf[4])
						self.document.seek(begin + p)
				return self.document

			def parse_element(self, tag, chars):
				if tag == "[[":
					return chars.split('|')[-1]

				if tag == "{{":
					return ''


		class State(object):
			def __init__(self, maxlen):
				self.maxlen = maxlen
				self.value = ""

			def set(self, data):
				if len(data) > 1 or len(data) < 1:
					raise ValueError("input must be one byte")
				if len(self.value) >= self.maxlen:
					self.value = self.value[1:]
				self.value += data

			def get(self):
				return self.value

			def depth(self):
				return len(self)

		eh = ElementHandler(self.data, {"[[":"]]", "{{":"}}"})
		self.data = eh.parse().getvalue()

	def _final_pass(self):
		def strip_newlines(d):
			regex = re.compile(r"\n\n+")
			return regex.sub('\n\n', d)

		def strip_brackets(d): 
			# this is required because some people hurt the wiki
			regex = re.compile(r"[\[\]\{\}]")
			return regex.sub('', d)

		self.data = strip_newlines(self.data)
		self.data = strip_brackets(self.data)

	def parse(self):
		if not self.done:
			self.done = True
			self._first_pass()
			self._second_pass()
			self._third_pass()
			self._final_pass()
		return self.data

