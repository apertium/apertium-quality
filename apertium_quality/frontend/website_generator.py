import sys, re, os.path
try:
	import argparse	
except:
	raise ImportError("Please install argparse module.")

from apertium_quality import Webpage, Statistics

#TODO add piping for great interfacing

class UI(object):
	def __init__(self):
		ap = argparse.ArgumentParser(description="Generate webpage and related files.")
		ap.add_argument("statistics", nargs=1, help="Statistics file")
		ap.add_argument("outdir", nargs=1, help="Output directory")
		self.args = args = ap.parse_args()
		self.stats = Statistics(args.statistics[0])
		self.web = Webpage(self.stats, args.outdir[0])
	
	def start(self):
		self.web.generate()

def main():
	try:
		ui = UI()
		ui.start()
	except KeyboardInterrupt:
		pass

if __name__ == "__main__":
	main()


