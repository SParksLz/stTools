# Called when this node should generate new work items from upstream items.
#
# self             -   A reference to the current pdg.Node instance
# item_holder      -   A pdg.WorkItemHolder for constructing and adding work items
# upstream_items   -   The list of work items in the node above, or empty list if there are no inputs
# generation_type  -   The type of generation, e.g. pdg.generationType.Static, Dynamic, or Regenerate

for upstream_item in upstream_items:
    new_item = item_holder.addWorkItem(parent=upstream_item)
    new_item.addAttrib("partition_id", pdg.attribType.String)
    road_info = new_item.attrib("road_info")
    road_info_expanded = road_info.value()
    col_id = road_info_expanded["partColId"]
    row_id = road_info_expanded["partRowId"]
    new_item.setStringAttrib("partition_id", "{0}_{1}".format(col_id, row_id))


# ----------------------------------

# Called when this node should generate new work items from upstream items.
#
# self             -   A reference to the current pdg.Node instance
# item_holder      -   A pdg.WorkItemHolder for constructing and adding work items
# upstream_items   -   The list of work items in the node above, or empty list if there are no inputs
# generation_type  -   The type of generation, e.g. pdg.generationType.Static, Dynamic, or Regenerate

def sortInfoByColRow(item):
    new_dir = {}
    info = item.attrib("road_info")
    info = info.value()
    col_id = info["partColId"]
    row_id = info["partRowId"]

    return (col_id, row_id)


col_id_array = [sortInfoByColRow(i)[0] for i in upstream_items]
row_id_array = [sortInfoByColRow(i)[1] for i in upstream_items]

col_max = max(col_id_array)
row_max = max(row_id_array)

new_item = item_holder.addWorkItem()
new_item.addAttrib("col_count", pdg.attribType.Int)
new_item.addAttrib("row_count", pdg.attribType.Int)

new_item.setIntAttrib("col_count", col_max + 1)
new_item.setIntAttrib("row_count", row_max + 1)
