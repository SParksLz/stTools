import logging
log = logging.getLogger('Light_AOV_X')

try:
	import v1 as Light_AOV_X
except Exception as exception:
    log.exception('Error importing Super Tool Python package: %s' % str(exception))
else:
	 PluginRegistry = [("SuperTool", 2, "Light_AOV_X",
                      (Light_AOV_X.Light_AOV_XNode,
                       Light_AOV_X.GetEditor)),
	 ]