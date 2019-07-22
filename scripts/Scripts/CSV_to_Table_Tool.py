# setting the environment
import arcpy
arcpy.env.overwriteOutput = True


#---------------------------------------------------------------------------
# creating a table from the csv file to be saved in a geodatabase
#---------------------------------------------------------------------------
# input CSV table
in_csv = arcpy.GetParameterAsText(0)


# output Geodatabase location ( the output must be a geodatabase *.gdb* type )
out_location = arcpy.GetParameterAsText(1)


# the name of the new table created in the geodatabase
table_name = arcpy.GetParameterAsText(2)


# Executing the tool
UsersT = arcpy.TableToTable_conversion(in_csv,out_location,table_name)

#---------------------------------------------------------------------------
# Sorting the created table based on time field to get the oldest to newest
# picture posted and adding new text field to the created table to be used for
# concatenation in the Concatenate Tool step.
#---------------------------------------------------------------------------

# the input table ( it's set to the previous step output )
in_table = out_location + "\\" + table_name

# the output location and name
out_sort = out_location + "\\" + table_name + "_Sorted"


# the field selected for sorting ( the sorting is Ascending )
sort_fields = [[arcpy.GetParameterAsText(3),"ASCENDING"]]


# Executing the sort tool
sorted_table = arcpy.Sort_management(in_table,out_sort,sort_fields)

#---------------------------------------------------------------------------
# Add new text field for concatenation process
#---------------------------------------------------------------------------

# input table
inTable = sorted_table

# name of the field
field_Name = arcpy.GetParameterAsText(4)

# the type of the field
field_Type = "TEXT"

# field length

#field_Length = 1000000
field_Length = arcpy.GetParameterAsText(5)

# Executing Add field tool
arcpy.AddField_management(inTable, field_Name, field_Type,"", "", int(field_Length))


#---------------------------------------------------------------------------

# END OF THE TOOL

#---------------------------------------------------------------------------
