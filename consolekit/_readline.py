# pragma: no cover

# stdlib
import sys

if not bool(getattr(sys, "ps1", sys.flags.interactive)):

	try:
		# stdlib
		import readline

		# typeshed thinks the module but not these functions are available on Windows.
		# In reality the whole module is unavailable.
		readline.set_history_length(0)
		readline.set_auto_history(False)
	except (ImportError, AttributeError):
		# Attribute error on PyPy, ImportError on Windows etc.
		pass
