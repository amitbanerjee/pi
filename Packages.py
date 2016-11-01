import string
import threading

class Package:
	def __init__(self, name):
		self.name = name
		#All the package needed to index it
		self.depsOn = []	
		#All the other packages require this package
		self.reqdBy = []	

	def __del__(self):
		del self.name
		del self.depsOn
		del self.reqdBy

class PackageList:
	def __init__(self):
		self.packages = []
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
			depsIs = []
			if deps:
				for dep in deps.split(","):
					#Check if the dep package is indexed
					for i in range(len(self.packages)):
						if self.packages[i].name == dep.strip():
							depsIs.append(i)
	
				#Make sure all deps are indexed
				if len(deps.split(",")) != len(depsIs):
					#This is python, it will execute "finally" even if it return from here.
					return "FAIL\n"
	
			newP = False
			newPI = False
	
			#If the package exists already
			#Note: There is some abiguity over the requirement that if the package exists and indexed again with new dependencies.
			#What happens when one/more new dependencies don't exist. I've assumed it to fail in the earlier part of the code.
			for i in range(len(self.packages)):
				if self.packages[i].name == name:
					newP = self.packages[i]
					newPI = i
					newP.depsOn = []
	
			#Take a blank position removed earlier if the package doesn't exist.
			if not newP:
				for i in range(len(self.packages)):
					if (self.packages[i].name == "" and not self.packages[i].depsOn and not self.packages[i].reqdBy):
						newP = self.packages[i]
						newPI = i
						newP.name = name
	
			#No blank position, so create a fresh one
			if not newP:
				newP = Package(name)
				self.packages.append(newP)
				newPI = len(self.packages)-1
	
			#Add the dependencies
			for sDI in depsIs:
				newP.depsOn.append(sDI)
			
			#Add the required by field
			for sDI in depsIs:
				self.packages[sDI].reqdBy.append(newPI)

		except:
			#Something unexpected happened!
			return False
			
		finally:
			self.lock.release()

		return "OK\n"
					

	"""
	Query a package
	"""
        def query(self, name):
		try:
			self.lock.acquire()
			for i in range(len(self.packages)):
				if self.packages[i].name == name:
					return True
			return False
		except:
			#Something unexpected happened!
			return False
		finally:
			self.lock.release()

	"""
	Removes a package
	"""
        def remove(self, name):
		try:
			self.lock.acquire()
			exists = False
			for i in range(len(self.packages)):
				if self.packages[i].name == name:
					exists = True
					#If it is required by other packages
					if self.packages[i].reqdBy:
						return "FAIL\n"

					#Remove itself from all required by list
					for sp in self.packages[i].depsOn:
						#print i, sp, self.packages[sp].name, self.packages[sp].depsOn, self.packages[sp].reqdBy
						self.packages[sp].reqdBy.remove(i)

			#Blank the Package entry
			if exists:
				self.packages[i].name = ""
				self.packages[i].depsOn= []
				self.packages[i].reqdBy= []
			
		except:
			#Something unexpected happened!
			return False
		finally:
			self.lock.release()
		return "OK\n"

	"""
	Debugging: Print the packages
	"""
	def printPackage(self):
		s = ""
		for i in range(len(self.packages)):
			s = self.packages[i].name + " depsOn = [" 
			for j in  self.packages[i].depsOn:
				s +=  self.packages[j].name + ","
			s += "] reqdBy = [" 
			for j in  self.packages[i].reqdBy:
				s +=  self.packages[j].name + ","
			s += "]\n" 
		print s			
		return s
		
		

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
