import string
import threading

class PackageList:
	def __init__(self):
		self.packages = {}
		self.lock = threading.Lock()

	def __del__(self):
		del self.packages
		del self.lock
	
	"""
	Index a new package
	Update Dependency of a package
	"""
        def index(self, name, deps=""):
		try:
			self.lock.acquire()
			if deps:
				for dep in deps.split(","):
					#Check if the dep package is indexed
					#Note: There is some abiguity over the requirement that if the package exists and indexed again with new dependencies.
					#What happens when one/more new dependencies don't exist. I've assumed it to fail in the earlier part of the code.
					if not dep in self.packages:
						return "FAIL\n"

			#If the package exists already
			if name in self.packages:
				del self.packages[name]
			self.packages[name] = {}
			for dep in deps.split(","):
				if dep:
					self.packages[name][dep] = 1
		except:
			#Something unexpected happened!
			return "ERROR\n"

		finally:
			self.lock.release()

		return "OK\n"
					

	"""
	Query a package
	"""
        def query(self, name):
		try:
			self.lock.acquire()
			if name in self.packages:
				return "OK\n"
			return "FAIL\n"
		except:
			#Something unexpected happened!
			return "ERROR\n"
		finally:
			self.lock.release()

	"""
	Removes a package
	"""
        def remove(self, name):
		try:
			self.lock.acquire()
			if not name in self.packages:
				return "OK\n"
			else:
				for sp in self.packages.keys():
					if name in self.packages[sp]:
						return "FALSE\n"
		except:
			#Something unexpected happened!
			return "ERROR\n"
		finally:
			self.lock.release()
		return "OK\n"

	"""
	Debugging: Print the packages
	"""
	def printPackage(self):
		print self.packages

if __name__=='__main__':

	#Code for unit testing
	myPacks = PackageList()
	'''
	print myPacks.query("abc")	
	print myPacks.index("abc")	
	print myPacks.query("abc")	
	print myPacks.remove("abc")	
	print myPacks.query("abc")	

	print myPacks.index("c")	
	print myPacks.index("b")	
	print myPacks.index("a","b,c")
	myPacks.printPackage()
	print myPacks.remove("a")	
	#print myPacks.remove("b")	
	print myPacks.index("d","b")
	myPacks.printPackage()
	'''

	myPacks.index("k")
	myPacks.index("i")
	myPacks.index("h")
	myPacks.index("j", "k")
	myPacks.index("g", "i,h")
	myPacks.index("f", "i,j")
	myPacks.index("b", "g")
	myPacks.index("c", "f")
	myPacks.index("e", "f")
	myPacks.index("a", "b,c")
	myPacks.index("d", "c,e")
	myPacks.printPackage()
	myPacks.index("c", "g,Z")
	myPacks.printPackage()
