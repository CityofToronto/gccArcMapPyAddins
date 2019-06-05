__revision__ = "$Id$"

__all__ = ['DoExport']

import time
import arcpy
import pythonaddins

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
