import logging

log = logging.getLogger('Ass_solver_X')

try:
	import v1 as Ass_solver_X
except Exception as exception:
	log.exception('Error importing Super Tool Python package:%s' % str(exception))
else:
	PluginRegistry = [("SuperTool", 2, "Ass_solver_X",
					  (Ass_solver_X.Ass_solver_XNode,
					   Ass_solver_X.GetEditor)),

	]