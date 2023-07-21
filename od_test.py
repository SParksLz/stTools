import sys
import os
from xml.etree.ElementTree import parse

dir = os.path.dirname(hou.hipFile.path())
sys.path.append(dir)
from readXodr import ODRoad


node = hou.pwd()
geo = node.geometry()

od_object = None

od_file = "gicc.xodr"
od_file = os.path.join(dir, od_file)

with open(od_file, encoding="utf-8") as f :
    od_object = parse(f)

roads = od_object.findall("road")
for road in roads :
    road_object = ODRoad.Road(road)
    road_level_pt = geo.createPoint()
    road_level_pt.setAttribValue("road_id", int(road_object.id))
    road_level_pt.setAttribValue("road_length", float(road_object.length))
    road_level_pt.setAttribValue("road_junction", int(road_object.junction))
    road_level_pt.setAttribValue("road_name", road_object.name)
    road_level_pt.setAttribValue("level", "road")

    road_geometry = road_object.planView.geometry
    for geometry in road_geometry :
        new_pt = geo.createPoint()
        new_pt.setPosition((float(geometry.x), 0, float(geometry.y)))
        new_pt.setAttribValue("level", "road_geometry")
        new_pt.setAttribValue("road_id", int(road_object.id))
        new_pt.setAttribValue("road_geo_type", geometry.desc.name)
        new_pt.setAttribValue("road_geometry_s", float(geometry.s))
        new_pt.setAttribValue("road_geometry_x", float(geometry.x))
        new_pt.setAttribValue("road_geometry_y", float(geometry.y))
        new_pt.setAttribValue("road_geometry_hdg", float(geometry.hdg))
        new_pt.setAttribValue("road_geometry_length", float(geometry.length))
        new_pt.setAttribValue("road_length", float(road_object.length))
        if geometry.desc.name == "paramPoly3" :
            new_pt.setAttribValue("road_paramPoly_aU", float(geometry.desc.desc.aU))
            new_pt.setAttribValue("road_paramPoly_aV", float(geometry.desc.desc.aV))
            new_pt.setAttribValue("road_paramPoly_bU", float(geometry.desc.desc.bU))
            new_pt.setAttribValue("road_paramPoly_bV", float(geometry.desc.desc.bV))
            new_pt.setAttribValue("road_paramPoly_cU", float(geometry.desc.desc.cU))
            new_pt.setAttribValue("road_paramPoly_cV", float(geometry.desc.desc.cV))
            new_pt.setAttribValue("road_paramPoly_dU", float(geometry.desc.desc.dU))
            new_pt.setAttribValue("road_paramPoly_dV", float(geometry.desc.desc.dV))


    lane_sections = road_object.lanes.laneSection
    for index in range(len(lane_sections)) :
        current_section = road_object.lanes.laneSection[index]
        current_offset = road_object.lanes.laneOffset[index]

        center = current_section.center
        center_pt = geo.createPoint()
        center_pt.setAttribValue("level", "lane_section")
        center_pt.setAttribValue("road_id", int(road_object.id))
        center_pt.setAttribValue("road_lane_section_center_ptr_to_road_geometry", int(road_object.id))
        center_pt.setAttribValue("road_lane_section_lane_type", "center")
        center_pt.setAttribValue("road_lane_section_s", float(current_section.s))
        center_pt.setAttribValue("road_lane_offset_s", float(current_offset.s))
        center_pt.setAttribValue("road_lane_offset_a", float(current_offset.a))
        center_pt.setAttribValue("road_lane_offset_b", float(current_offset.b))
        center_pt.setAttribValue("road_lane_offset_c", float(current_offset.c))
        center_pt.setAttribValue("road_lane_offset_d", float(current_offset.d))

        if float(current_offset.a) != 0 and float(current_offset.b) != 0 and float(current_offset.c) != 0 and float(current_offset.d) != 0 :
            print("{}  {}  {}  {}".format(current_offset.a, current_offset.b, current_offset.c, current_offset.d))

        # left = current_section.left
        # right = current_section.right
        #
        # if left :
        #     left_lanes = left.lane
        #     for left_lane in left_lanes :
        #         left_pt = geo.createPoint()
        #
        #         left_pt.setAttribValue("road_lane_section_rl_ptr_to_center", center_pt.number())
        #         left_pt.setAttribValue("road_lane_section_rl_lane_id", left_lane.id)
        #         left_pt.setAttribValue("road_lane_section_rl_lane_level", left_lane.level)
        #         left_pt.setAttribValue("road_lane_section_rl_lane_type", left_lane.type)
        #         left_pt.setAttribValue("level", "lane_section_left")
        #
        #         border = left_lane.border
        #         height = left_lane.height
        #         width  = left_lane.width
                # left_pt.setAttribValue("road_lane_section_rl_lane_border", float(left_lane.border))
                # left_pt.setAttribValue("road_lane_section_rl_lane_height", float(left_lane.height))
                # left_pt.setAttribValue("road_lane_section_rl_lane_width", float(left_lane.width))











# Add code to modify contents of geo.
# Use drop down menu to select examples.
