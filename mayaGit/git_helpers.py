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
		self.commits = list(self.repo.iter_commits(branch, max_count=limit))
		return self.commits

	def getCommitChanged(self, num):
		changed_files = list()

		if self.commits:
			for x in self.commits[num].diff(self.commits[num-1]):
			    if x.a_blob:
				    if x.a_blob.path not in changed_files:
				        changed_files.append(x.a_blob.path)

	        	if x.b_blob:
					if x.b_blob is not None and x.b_blob.path not in changed_files:
						changed_files.append(x.b_blob.path)

		return changed_files      

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
		