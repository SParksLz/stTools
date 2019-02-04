# -*- coding: utf-8 -*-
# @Author: liuzhen
# @Date:   2018-07-27 11:01:41
# @Last Modified by:   liuzhen
# @Last Modified time: 2018-07-27 11:13:03
import logging
log = logging.getLogger('Solver_X')

try:
	import v1 as Solver_X
except Exception as exception:
    log.exception('Error importing Super Tool Python package: %s' % str(exception))
else:
	 PluginRegistry = [("SuperTool", 2, "Solver_X",
                      (Solver_X.Solver_XNode,
                       Solver_X.GetEditor)),
	 ]