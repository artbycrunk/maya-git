import git
import console

def isValidRepo(path):
	try:
		repo = git.Repo(path)
		console.log('Valid Repo!', 'info')
		return True
	except:
		console.log('is Not Valid Repo!', 'error')
		return False

class mayaGit:

	def __init__(self, path):
		self.path = path
		# self.repo = git.Repo(path)
		if self.isValid(self.path):
			self.index = self.repo.index
			console.log('Repo Init', 'info')

	def isValid(self, path):
		try:
			self.repo = git.Repo(path)
			# console.log('Valid Repo!', 'info')
			return True
		except:
			# console.log('is Not Valid Repo!', 'error')
			return False
		
	def isDirty(self):
		return self.repo.is_dirty()

	def addSelected(self, files):
		self.index.add(files)

	def removeSelected(self, files):
		self.index.remove(files)

	def resetSelected(self, files):
		self.index.reset(files)

	def getChanged(self):
		return self.index.add([diff.a_blob.path for diff in self.index.diff(None)])

	def getCommits(self, branch, limit):
		return self.repo.iter_commits(branch, max_count=limit)

	def getStaged(self):
		hcommit = self.repo.head.commit
		if hcommit:
			return hcommit.diff()

	def getAllFiles(self):
		blobs = list()
		for stage, blob in self.index.iter_blobs():
			blobs.append(blob)
		if blobs:
			return blobs

	def commit(self, message):
		new_commit = self.index.commit(message)
		