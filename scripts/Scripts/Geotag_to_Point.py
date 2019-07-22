
import arcpy
arcpy.env.overwriteOutput = True

#-------------------------------------------------------------------------------
#Setting the variables for creating the Event Layer and the final Feature Class
#-------------------------------------------------------------------------------

inTable = arcpy.GetParameterAsText(0)

inLong = arcpy.GetParameterAsText(1)
inLat = arcpy.GetParameterAsText(2)

outLyr = "XYlyr"
CordSys = arcpy.GetParameterAsText(3)


outFeature = arcpy.GetParameterAsText(4)
outLocation = arcpy.GetParameterAsText(5)

#-------------------------------------------------------------------------------
# Creating the Event Layer from the table
#-------------------------------------------------------------------------------


arcpy.MakeXYEventLayer_management(inTable,inLong,inLat,outLyr,CordSys)

#-------------------------------------------------------------------------------
# Converting the Event Layer to Feature Class
#-------------------------------------------------------------------------------

arcpy.FeatureClassToFeatureClass_conversion(outLyr,outLocation,outFeature)


#-------------------------------------------------------------------------------

# END OF TOOL

#-------------------------------------------------------------------------------
