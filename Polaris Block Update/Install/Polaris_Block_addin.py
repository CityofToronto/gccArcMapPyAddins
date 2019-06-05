import time
import arcpy
import pythonaddins

# from Utils import map_support as cadast

EXP_parcels_fc = 'map_parcels'
_tool_Title = 'Polaris Block update'

def DoExport(lyr, exp_fc, exp_workspace):
	_iError_ = 0
	
	exp_feature_set = exp_workspace + "/" + exp_fc
	
	# Set the current workspace
	#
	arcpy.env.workspace = exp_workspace
	# Check for existence of data before deleting
	#
	if arcpy.Exists(exp_fc) :
		arcpy.Delete_management(exp_fc)

	try :
		print "\nExporting parcels into: " + exp_feature_set + " ..."
		_fs_to_save_ = arcpy.FeatureSet(lyr)
		_fs_to_save_.save(exp_feature_set)
	except :
		_iError_ = -1

	# Wait to complete
	time.sleep(10.0)
	return _iError_

class ExportParcelsClass(object):
    # Implementation of OnClick method of Button's class
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
		cur_workspace = arcpy.geoprocessing.env.workspace
		# Get the current map document and the first data frame.
		mxd = arcpy.mapping.MapDocument('current')
		df = arcpy.mapping.ListDataFrames(mxd)[0]
		## Call the zoomToSelectedFeatures() method of the data frame class
		## df.zoomToSelectedFeatures()
		##pythonaddins.MessageBox("Vk","kV",0)
		parLyr = self._get_Parcel_(mxd)
		if parLyr == None:
		   pythonaddins.MessageBox("The map is not for cadastral data\nParcel layer is missing",_tool_Title,0)
		   exit(100)
		
		pbLyr = self._get_PolarisBlock_(mxd)
		if pbLyr == None:
		   pythonaddins.MessageBox("The map is not for cadastral data\nPolaris Block layer is missing",_tool_Title,0)
		   exit(100)
		
		#pythonaddins.MessageBox("Vk","kV",0)
		pbselList = pbLyr.getSelectionSet()
		if pbselList == None :
			pythonaddins.MessageBox("Please make a selection on Polaris Block layer",_tool_Title,0)
			#print "WARNING >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
			#print "Please make a selection on " + str(pbLyr)
			#print "WARNING >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
			## del mxd
			## exit(-100)
		else:
			sel_count = len(pbselList)
			#print ("Selected Polaris Blocks: " + str(sel_count))
			if (self._ShowPolarisBlockSelection_(pbLyr, pbselList)).upper() == "CANCEL":
			  del pbselList
			  del parLyr
			  del pbLyr
			  del mxd
			  exit(100)
			
			del pbselList
			
			result = arcpy.SelectLayerByLocation_management(parLyr,"HAVE_THEIR_CENTER_IN",pbLyr)
			### WARNING: MTB is too slow
			### Try only in QA/Prod !!!!
			### result = arcpy.SelectLayerByLocation_management(parLyr,"WITHIN_CLEMENTINI",pbLyr,0.0,"ADD_TO_SELECTION")
			
			# Check the status of the result object every 0.2 seconds
			#    until it has a value of 4 (succeeded) or greater
			while result.status < 4 :
			   time.sleep(0.2)
			# Wait little bit more
			time.sleep(3.0)
			result = arcpy.GetCount_management(parLyr)
			sel_count = result.getOutput(0)
			# Must got greater then 0
			if sel_count == 0 :
				pythonaddins.MessageBox("ERROR: no parcels were selected",_tool_Title,0)
				#print "ERROR >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
				#print "No selection found in " + str(parLyr)
				#print "ERROR >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
				#exit(-101)
			else :
				print ("\nSelected parcels: " + str(sel_count))
				#exp_parcels_fc = "map_parcels"
				temp_workspace = arcpy.geoprocessing.env.scratchWorkspace
				exp_feature_set = temp_workspace + "/" + EXP_parcels_fc

				if DoExport(parLyr, EXP_parcels_fc, temp_workspace) < 0:
				   pythonaddins.MessageBox("ERROR: Expoprt to local geodatabase was not succeeded",_tool_Title,0)
				   #print "\nExporting parcels FAiled WITH ERROR <" + arcpy.GetMessages() + ">"
				else:
				   print ("Exported parcels: " + str(sel_count))
				   # Add to the map
				   arcpy.MakeFeatureLayer_management(exp_feature_set, EXP_parcels_fc)
				   
				   # Check the status of the result object every 0.2 seconds
				   #    until it has a value of 4 (succeeded) or greater
				   while result.status < 4:
				   	  time.sleep(0.2)
					  
				   parLyr.setSelectionSet("NEW", [])
				   
				   #Make new layer Visible
				   del mxd
				   mxd = arcpy.mapping.MapDocument('current')
				   lyr=self._get_Layer_(mxd, EXP_parcels_fc)
				   if lyr != None:
					 lyr.visible = True
					 df = arcpy.mapping.ListDataFrames(mxd)[0]
					 df.extent = lyr.getExtent()
					 del lyr
				
				arcpy.env.workspace = cur_workspace
		
		## pythonaddins.MessageBox("Vk","kV",0)
		del parLyr
		del pbLyr
		del mxd
    def _get_Layer_(self, doc, la_name):
		try:
		   lyr = arcpy.mapping.ListLayers(doc, la_name)[0]
		except:
		   lyr=None
		
		if lyr == None:
		  # pythonaddins.MessageBox("The map is not for cadastral data",_tool_Title,0)
		  print "The map content does not includes the layer <{}> ".format(la_name)
		  return None
		else:
		  print "The the layer <{}> has been found in the map".format(la_name)
		  return lyr
    def _get_Parcel_(self, doc):
		# Must got: Municipal Parcel Fabric\Parcels
		lyr=self._get_Layer_(doc, "Parcels")
		if lyr != None:
		  #print ("Parcels layer: " + str(lyr))
		  return lyr
		else:
		  lyr=self._get_Layer_(doc, "CADAST.Cadastral_Parcels")
		  if lyr != None:
			#print ("Parcels layer: " + str(lyr))
			return lyr
		  else:
			return None
    def _get_PolarisBlock_(self, doc):
		# Must got: Polaris Block
		lyr=self._get_Layer_(doc, "CADAST.POLARIS_BLOCK")
		if lyr != None:
		  #print ("Polaris Block layer: " + str(lyr))
		  return lyr
		else:
		  return None
    def _ShowPolarisBlockSelection_(self, lyr, sel_set):
		fcPBlock = arcpy.FeatureSet(lyr)
		oid_field= "OBJECTID"
		
		# Create an expression with proper delimiters
		pblock_list = arcpy.AddFieldDelimiters(fcPBlock, oid_field) + ' IN ('
		# Must have selection
		for feat in sel_set:
		   pblock_list = pblock_list + "'" + str( feat ) + "',"
		   ## print str( feat )
		pblock_list = pblock_list.rstrip(',')
		pblock_list = pblock_list + ")"
		## print pblock_list
		
		# Display POLARIS_BLOCK attribute
		pb_ids = []
		for row in arcpy.da.SearchCursor(fcPBlock, ["POLARIS_BLOCK"], where_clause=pblock_list):
		   #print("POLARS_BLOCK: {}".format(row[0]))
		   pb_ids.append(str(row[0]))
		   
		return pythonaddins.MessageBox("POLARIS_BLOCK: {}".format(pb_ids),_tool_Title,1)  ## Ok/Cancel
    