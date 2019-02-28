# -*- coding utf-8 -*-

import os
a = os.path.dirname(__file__)

iconpath = os.path.join(os.path.dirname(a), "icons")
iconpath.replace("\\", "/")
print iconpath