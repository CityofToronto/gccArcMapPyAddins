class overwriteError(Exception):
    pass

import arcpy
import time
import pythonaddins

_tool_title = 'Building final result'

EDIT_Block_ToolBoxLocation = r'C:\GCC\GpTools'
EDIT_Block_ToolBox = 'Polaris Block.tbx'
EDIT_BLOCK_CompileBlock_Tool = 'PreapareLineWorkNewBlocks'
EDIT_BLOCK_NewUpdateBlock_Tool = 'CreateNewPolarisBlocks'
EDIT_BLOCK_LINES_fc = 'pblock_new_lines'
UPDATE_BLOCK_center_point = "change_block_center_point"
EDIT_BLOCK_fc = 'pblock_new_update'

def AddLayerToTheMap(feature_class):
	# Add to the map
	temp_workspace = arcpy.geoprocessing.env.scratchWorkspace
	new_feature_set = temp_workspace + "/" + feature_class
	if arcpy.Exists(new_feature_set):
		arcpy.MakeFeatureLayer_management(new_feature_set, feature_class)
		# Check the status of the result object every 0.2 seconds
		#    until it has a value of 4 (succeeded) or greater
		while result.status < 4:
			time.sleep(0.2)
		
		#Make new layer Visible
		del mxd
		mxd = arcpy.mapping.MapDocument('current')
		lyr=self._get_Layer_(mxd, feature_class)
		if lyr != None:
			lyr.visible = True
			df = arcpy.mapping.ListDataFrames(mxd)[0]
			df.extent = lyr.getExtent()
			del lyr
	

class GpBuildBlockDialogClass(object):
    """Implementation for Edit Blocks_addin.ed_button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
		fs_location = EDIT_Block_ToolBoxLocation+"\\"+EDIT_Block_ToolBox
		# pythonaddins.MessageBox("Vk",fs_location,0)
		try:
			pythonaddins.GPToolDialog(fs_location, 
								 EDIT_BLOCK_CompileBlock_Tool)
		except:
			pass

class GpEditBlockFinalClass(object):
    """Implementation for Edit Blocks_addin.up_button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
		# pythonaddins.MessageBox("Vk",fs_location,0)
		try:
			cur_workspace = arcpy.env.workspace
			#TO DO: make new feature_class
			# Process: Delete
			arcpy.env.workspace = arcpy.geoprocessing.env.scratchWorkspace
			if arcpy.Exists(EDIT_BLOCK_fc):
				arcpy.Delete_management(EDIT_BLOCK_fc, "FeatureClass")
				
			pr_ready = True
			if not arcpy.Exists(EDIT_BLOCK_LINES_fc):
				pr_ready = False
			if not arcpy.Exists(UPDATE_BLOCK_center_point):
				pr_ready = False
			
			if pr_ready:
				lines = arcpy.env.workspace+ "\\" + EDIT_BLOCK_LINES_fc
				polygons =  arcpy.env.workspace+ "\\" + EDIT_BLOCK_fc
				cn_points = arcpy.env.workspace+ "\\" + UPDATE_BLOCK_center_point
				result = arcpy.FeatureToPolygon_management(lines, polygons , "0.005 Meters", "ATTRIBUTES", cn_points)
				
				# Check the status of the result object every 0.2 seconds
				#    until it has a value of 4 (succeeded) or greater
				while result.status < 4:
					time.sleep(0.2)

				#print result.GetMessages()
				pythonaddins.MessageBox("Succefull completion\n"+arcpy.GetMessages(),_tool_title,0)
				
				# Add to the map
				# AddLayerToTheMap(arcpy.geoprocessing.env.workspace, EDIT_BLOCK_fc)
			else:
				pythonaddins.MessageBox('Some of feature classes where not found in current workspace',_tool_title,0)
			
			arcpy.env.workspace = cur_workspace
			
		except:
			arcpy.AddError('Something went wrong. Tool execution fails')
			pythonaddins.MessageBox("ERRORS\n"+arcpy.GetMessages(),_tool_title,0)
	