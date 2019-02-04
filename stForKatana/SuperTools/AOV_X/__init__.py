import logging
log = logging.getLogger('AOV_X')

try:
	import v1 as AOV_X
except Exception as exception:
    log.exception('Error importing Super Tool Python package: %s' % str(exception))
else:
	 PluginRegistry = [("SuperTool", 2, "AOV_X",
                      (AOV_X.AOV_XNode,
                       AOV_X.GetEditor)),
	 ]