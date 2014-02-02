import maya.cmds as mc
import maya.mel as mm
import git_helpers as mg


gitMaya = ''
MainPath = ''

def preUI():
	if mc.window( 'gitMayaWin', query=True, ex=True ):
		mc.deleteUI('gitMayaWin')

def createUI():

	preUI()

	mc.window( 'gitMayaWin', title="Git Tools", iconName='', widthHeight=(200, 55) )
	mc.menuBarLayout()
	mc.menu( label='File' )
	mc.menuItem( label='Create Repo', c=lambda *args: createRepo() )
	mc.setParent( '..' )
	mc.columnLayout( adjustableColumn=True )
	mc.textFieldButtonGrp( 'repoPath', label='Repo Path', text='', buttonLabel='Browse', bc=lambda *args: getFolder() )
	mc.button( label='Refresh', c=lambda *args: initRepo() )
	mc.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
	mc.columnLayout( 'Files', adjustableColumn=True )
	mc.rowColumnLayout(nc=5)
	mc.separator(h=20, style='none')
	mc.text(l='Working Copy Changes')
	mc.separator(h=20, style='none')
	mc.separator(h=20, style='none')
	mc.text(l='Staged Changes')
	mc.columnLayout( 'workingChangesColor', adjustableColumn=True)
	mc.setParent( '..' )
	mc.textScrollList( 'workingChanges', numberOfRows=16, allowMultiSelection=True)
	mc.columnLayout( adjustableColumn=True )
	mc.button( label='>>', c=lambda *args: addChanged())
	mc.button( label='>' )
	mc.separator(h=30, style='none')
	mc.button( label='<', c=lambda *args: remSelected())
	mc.button( label='<<' )
	mc.setParent( '..' )
	mc.columnLayout( 'stagedChangesColor', adjustableColumn=True )
	mc.setParent( '..' )
	mc.textScrollList( 'stagedChanges', numberOfRows=16, allowMultiSelection=True)
	mc.setParent( '..' )
	mc.textFieldButtonGrp( 'commitMessage', label='Message', text='', buttonLabel='Commit', bc=lambda *args: doCommit() )
	mc.separator(h=20)
	mc.setParent( '..' )

	mc.columnLayout( 'History', adjustableColumn=True )
	mc.intFieldGrp( 'commitCount', numberOfFields=1, label='Number of Commits', value1=10, cc=lambda *args: getCommits())
	mc.scrollLayout(h=250, horizontalScrollBarThickness=16, verticalScrollBarThickness=16)
	mc.rowColumnLayout( 'commitsGrid', numberOfColumns=2, cw=([1,450],[2,150]) )
	mc.setParent( '..' )
	mc.setParent( '..' )
	mc.text(l='Commited Changes')
	mc.textScrollList( 'commitChanges', numberOfRows=16, allowMultiSelection=True)
	mc.showWindow( 'gitMayaWin' )

	postUI()

def postUI():
	mc.window( 'gitMayaWin', edit=True, widthHeight=[634, 585] )

def getFolder():
	global MainPath
	path = mc.fileDialog2(dialogStyle=2, fm=3, okc='Select')
	MainPath = path[0]
	if MainPath:
		mc.textFieldButtonGrp( 'repoPath', edit=True, text=MainPath)
		# mg.isValidRepo(path[0])
		initRepo()

def createRepo():
	pass

def initRepo():
	global gitMaya
	global MainPath
	# MainPath = mc.textFieldButtonGrp( 'repoPath', query=True, text=True)
	if MainPath:
		clear()
		gitMaya = mg.mayaGit(MainPath)
		getWorkingCopy()
		refreshStage()
		getCommits()

def getWorkingCopy():
	global gitMaya
	fileList = list()
	blobs = gitMaya.getAllFiles()
	for blob in blobs:
		fileList.append(blob.path)
		# mc.iconTextButton( parent='workingChangesColor', style='iconOnly', image1='', label='', bgc=[0,1,0], h=13, w=13 )
	if fileList:
		mc.textScrollList( 'workingChanges', edit=True, append=fileList)	

def commitNumLink(num):
	return lambda *args: getCommitFiles(num)

def getCommits():
	global gitMaya
	clearChildren()
	count = mc.intFieldGrp( 'commitCount', query=True, v1=True)
	# num=int(1)
	commits = gitMaya.getCommits('master', count)

	for i in range(0, len(commits)):
		mc.textField(parent='commitsGrid', ed=0, text=commits[i].message, rfc=commitNumLink(i+1) )
		mc.textField(parent='commitsGrid', ed=0, text=commits[i].author)

	# for commit in gitMaya.getCommits('master', count):
	# 	mc.textField(parent='commitsGrid', ed=0, text=commit.message, rfc=(lambda *args: getCommitFiles(int(num))) )
		
	# 	mc.textField(parent='commitsGrid', ed=0, text=commit.author)
	# 	num= num+1
		# count = count+1

def getCommitFiles(num):
	global gitMaya
	mc.textScrollList( 'commitChanges', edit=True, ra=True)
	print num
	files = gitMaya.getCommitChanged(num)
	if files:
		mc.textScrollList( 'commitChanges', edit=True, append=files)

def addChanged():
	global gitMaya
	global MainPath
	if MainPath:
		files = gitMaya.getChanged()
		refreshStage()

	# print files
	# fileList = list()
	# if files:
	# 	for file in files:
	# 		fileList.append(file[3])
	# if fileList:
	# 	mc.textScrollList( 'stagedChanges', edit=True, append=fileList)

def remSelected():
	global gitMaya
	files = mc.textScrollList( 'stagedChanges', query=True, si=True)
	if files:
		gitMaya.resetSelected(files)
		for file in files:	
			mc.textScrollList( 'stagedChanges', edit=True, ri=file)

def clear():
	mc.textScrollList( 'workingChanges', edit=True, ra=True)
	mc.textScrollList( 'stagedChanges', edit=True, ra=True)
	# mc.textScrollList( 'commits', edit=True, ra=True)
	clearChildren()

def refreshStage():
	global gitMaya
	mc.textScrollList( 'stagedChanges', edit=True, ra=True)
	files = gitMaya.getStaged()
	fileList = list()
	if files:
		for file in files:
			mc.iconTextButton( parent='stagedChangesColor', style='iconOnly', image1='', label='', bgc=[0,1,0], h=13, w=13 )
			fileList.append(file.b_blob.path)
	if fileList:
		mc.textScrollList( 'stagedChanges', edit=True, append=fileList)

def doCommit():
	global gitMaya
	message = mc.textFieldButtonGrp( 'commitMessage', query=True, text=True)
	if message:	
		gitMaya.commit(message)
		refreshStage()
		getCommits()
	else:
		print 'error no message'	

def clearChildren():
	children = mc.rowColumnLayout( 'commitsGrid', query=True, ca=True)
	if children:
		for child in children:
			mc.deleteUI(child)