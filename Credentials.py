#### Header file that contains Student's usernames and passwords

class User:

	global_count = 0 # keeps track of a global count of how many Keys have been used 

	def __init__(self, username, key):
		self.username = username
		self.key = key
		User.global_count += 1

	def showGlobalCount(self):
		print "Number of Keys: %d" % global_count

	def showKeys(self):
		print "username: " + self.username
		print "key: " + self.key + '\n'


