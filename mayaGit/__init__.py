try:
	import git
except ImportError:
	raise ImportError("'git' could not be found in your PYTHONPATH")