# gccArcMapPyAddins
Python addins to support CEdit application

1.Polaris Block Update
  The tool allow to create a source to regenerate Polaris Block boundaries. The source is cadastral parcels. The process based on dissolve geoprocessing operation and requeres attribute NAME of parcels set to include polaris block ID as 5 characters starting from left end of string
  The result of the tool the new feature class in local geodatabase created from selected cadastral parcelels with TYPE = 2 (municipal parcels). The selection method is spatial selection where the source layer is Polaris Block seleted features (to be updated)
