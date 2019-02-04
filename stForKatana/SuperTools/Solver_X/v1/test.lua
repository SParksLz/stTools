-- @Author: liuzhen
-- @Date:   2018-07-27 11:01:41
-- @Last Modified by:   liuzhen
-- @Last Modified time: 2018-07-27 11:12:59
local location = Interface.GetInputLocationPath()
local geometry = Interface.GetPotentialChildren()
local path = location .. '/' .. 'geometry'
local child = Interface.GetPotentialChildren(path):getNearestSample(0.0)
for i=1, #child do
	local childpath = path .. '/' .. child[i]
	Interface.CopyLocationToChild(child[i],childpath)
end
Interface.DeleteChild('geometry')
