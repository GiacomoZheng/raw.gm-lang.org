#! python3
# coding:utf-8

# gmraw=/home/giacomo/raw.gm-lang.org/raw

from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application

import os
import sys

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments_gm import GMLexer

if len(sys.argv) > 1:
	ROOT = sys.argv[1]
else:
	ROOT = "./"

if os.environ.get("gmraw") is None:
	GMRAW = os.path.join(ROOT, "raw/")
else:
	GMRAW = os.environ.get("gmraw")

def transparent(s):
	return s.startswith("_") and s.endswith("_")

class Unimplement(Exception):
	def __str__(self):
		return f"functionality unimplement yet"

class NoSuchFile(Exception):
	def __init__(self, name):
		self.name = name
		super().__init__("no file named " + str(self.name))

# !!!! full name is not full name
def analyze(full_name : str, directory : str, root = ROOT, file = ".gm", ext = ".gm") -> str:
	"""
	"gm.h.group" ⇒ "./gm/h/_/group/.gm"
	"""

	path = directory
	locations = full_name.split(".")
	location = locations[0]
	# print("location", location)

	if os.path.isfile(os.path.join(path, location + ext)):
		# + I guess this functionality is wrong, only work for theorem
		if len(locations) > 1:
			raise Unimplement()
		return os.path.join(path, location + ext)

	if os.path.isdir(os.path.join(path, location)):
		return analyze(".".join(locations[1:]), os.path.join(path, location), root)

	for item in filter(transparent, [filepath for filepath in os.listdir(directory)]):
		try:
			return analyze(full_name, os.path.join(path, item), root)
		except Unimplement:
			eprint("Unimplement")
			raise Unimplement()
		except NoSuchFile:
			pass
		except Exception as e:
			raise Exception(e)

	raise NoSuchFile(full_name)

class RawHandler(RequestHandler):
	def get(self, title : str):
		try:
			with open(analyze(str(title), GMRAW), "r") as handle:
				self.write(handle.read().replace("\t", "    ")) # TODO)
		except Exception as e:
			self.write(str(e))

# for html, I may remove it
class HtmlHandler(RequestHandler):
	def get(self, title : str):
		try:
			path_raw = analyze(str(title), GMRAW)
			path_src = ROOT + "src_cache/" + str(title) + ".html"
			if (not os.path.isfile(path_src)) or (os.path.getmtime(path_src) < os.path.getmtime(path_raw)):
				with open(path_raw, "r") as handle:
					raw = handle.read().replace("\t", "    ") # TODO
				with open(path_src, "w") as handle:
					handle.write(highlight(raw, GMLexer(), HtmlFormatter(linenos="table")))
			with open(path_src, "r") as handle:
				self.write(handle.read())
		except Exception as e:
			# raise e
			self.write(str(e))

def make_app():
	return Application(handlers=[
		(r"/([\w-][\.\w-]*)", RawHandler),
		(r"/([\w-][\.\w-]*)/html", HtmlHandler),
	])

if __name__ == "__main__":
	app = make_app()
	app.listen(8888)
	IOLoop.current().start()
