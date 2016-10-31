import string

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

	def __del__(self):
		del self.packages
	
	"""
	Index a new package
	Update Dependency of a package
	"""
        def index(self, name, deps=""):
		depsIs = []
		if deps:
			for dep in deps.split(","):
				#Check if the dep package is indexed
				for i in range(len(self.packages)):
					if self.packages[i].name == dep:
						depsIs.append(i)

			#Make sure all deps are indexed
			if len(deps.split(",")) != len(depsIs):
				print depsIs 
				print "All deps are not indexed"
				return False

		#Take a blank position remobved earlier
		newP = False
		newPI = False
		for i in range(len(self.packages)):
			if self.packages[i].name == "" and not self.packages[i].depsOn and not self.packages[i].reqdBy:
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
		
		return True
						

	"""
	Query a package
	"""
        def query(self, name):
		for i in range(len(self.packages)):
			if self.packages[i].name == name:
				return True
		return False

	"""
	Removes a package
	"""
        def remove(self, name):
		for i in range(len(self.packages)):
			if self.packages[i].name == name:
				#If it is required by other packages
				if self.packages[i].reqdBy:
					return False

				#Remove itself from all required by list
				for sp in self.packages[i].depsOn:
					#print i, sp, self.packages[sp].name, self.packages[sp].depsOn, self.packages[sp].reqdBy
					self.packages[sp].reqdBy.remove(i)

		#Blank the Package entry
		self.packages[i].name = ""
		self.packages[i].depsOn= []
		self.packages[i].reqdBy= []
			
		return True

	"""
	Debugging: Print the packages
	"""
	def printPackage(self):
		for i in range(len(self.packages)):
			print self.packages[i].name, self.packages[i].depsOn, self.packages[i].reqdBy
		

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
