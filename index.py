#! python3
# coding:utf-8

# gmraw=/home/giacomo/raw.gm-lang.org/raw
# gmraw=/mnt/c/Users/giacomo/Documents/GitHub

from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application

import os

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments_gm.gm import GMLexer

pwd = os.getcwd()
if os.environ.get("gmraw") is None:
	GMRAW = os.path.join(pwd, "raw/")
else:
	GMRAW = os.environ.get("gmraw")

def transparent(s):
	return s.startswith("_") and s.endswith("_")

class Unimplement(Exception): pass
class NoSuchFile(Exception): pass

def analyze(full_name : str, directory = pwd, root = pwd, file = ".gm", ext = ".gm") -> str:
	"""
	"gm.h.group" ⇒ "./gm/h/_/group/.gm" \n
	"gm.Prolog" ⇒ "./gm/_/_interest_/Prolog"
	"""

	path = directory
	locations = full_name.split(".")
	location = locations[0]
	# print("location", location)

	if os.path.isfile(os.path.join(path, location + ext)):
		if len(locations) > 1:
			raise Unimplement("unimplement!")
		return os.path.join(path, location + ext)

	if os.path.isdir(os.path.join(path, location)):
		return analyze(".".join(locations[1:]), os.path.join(path, location), root)

	for item in filter(transparent, [filepath for filepath in os.listdir(directory)]):
		# print("transpart item: ", item)
		try:
			return analyze(full_name, os.path.join(path, item), root)
		except Unimplement as e:
			raise Unimplement(e)
		except NoSuchFile:
			pass
		except Exception as e:
			raise Exception(e)

	raise NoSuchFile("no such file")

class RawHandler(RequestHandler):
	def get(self, title : str):
		try:
			with open(analyze(str(title), GMRAW), "r") as handle:
				self.write(handle.read())
		except Exception as e:
			# raise e
			self.write(str(e))

class TimeHandler(RequestHandler):
	def get(self, title : str):
		try:
			self.write(
				str(os.path.getmtime(analyze(str(title), GMRAW)))
			)
		except Exception as e:
			# raise e
			self.write(str(e))

# for html, I may remove it
class HtmlHandler(RequestHandler):
	def get(self, title : str):
		try:
			with open(analyze(str(title), GMRAW), "r") as handle:
				raw = handle.read()
			self.write(highlight(raw, GMLexer(), HtmlFormatter()))
		except Exception as e:
			# raise e
			self.write(str(e))


def make_app():
	return Application(handlers=[
		(r"/([\w-][\.\w-]*)", RawHandler),
		(r"/([\w-][\.\w-]*)/time", TimeHandler),
		(r"/([\w-][\.\w-]*)/html", HtmlHandler),
	])

if __name__ == "__main__":
	app = make_app()
	app.listen(8888)
	IOLoop.current().start()
