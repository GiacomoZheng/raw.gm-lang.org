#! python3
# coding:utf-8
# gmraw=/home/giacomo/docs/raw

# static=/mnt/c/Users/giaco/Documents/GitHub/doc.gm-lang.org/static gmraw=/mnt/c/Users/giaco/Documents/GitHub gmsrc=/mnt/c/Users/giaco/Documents/GitHub/doc.gm-lang.org/src

from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application

import os

def transparent(s):
	return s.startswith("_") and s.endswith("_")

class Unimplement(Exception): pass
class NoSuchFile(Exception): pass

def analyze(full_name : str, directory = ".", root = ".", file = ".gm", ext = ".gm") -> str:
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
			with open(analyze(str(title), str(os.environ.get("gmraw"))), "r") as handle:
				self.write(handle.read())
		except Exception as e:
			self.write(str(e))

def make_app():
	return Application(handlers=[
		(r"/raw/([\w-][\.\w-]*)", RawHandler),
	])

if __name__ == "__main__":
	app = make_app()
	app.listen(8888)
	IOLoop.current().start()
