
import arcpy,csv, os


#------------------------------------------------------------------------------------------------------------------

# Importing the table from the geodatabase to read the Concatenate field

#------------------------------------------------------------------------------------------------------------------


# the input table from the geodatabase

table = arcpy.GetParameterAsText(0)

#------------------------------------------------------------------------------------------------------------------

# Deleting identical unique items ( Example: deleting multiple user id's to unique user id for each row )

#------------------------------------------------------------------------------------------------------------------

# Field the contans the duplicated items
DuplicateField = arcpy.GetParameterAsText(1)
# Executing Delete Identical Tool
arcpy.DeleteIdentical_management(table, DuplicateField)

#------------------------------------------------------------------------------------------------------------------

# selecting the Concatenate field in the input table

#------------------------------------------------------------------------------------------------------------------

# the field to be used for the probability analysis, which contain the concatenated values ( CONCATENATED FIELD )
field = arcpy.GetParameterAsText(2)

# using SearchCursor to access the data
Con_field = arcpy.da.SearchCursor(table, field)

# A list to append the field country codes
list1 = []

# User defined country codes from the concatenated field ( Example: country A code, country B code)

ctyA_1 = arcpy.GetParameterAsText(3)
ctyB_1 = arcpy.GetParameterAsText(4)
output_folder = arcpy.GetParameterAsText(5)

# Converting the entered country codes to integers for probability analysis
ctyA = int(ctyA_1)
ctyB = int(ctyB_1)


# Sum of N1 ( if country code B is occured after country code A in each row ) ---> ( Example: A user visited Spain after visiting UK )
# and N2 ( total occurance of Item A in each row ) to be used later for the probability ---> ( Example: All the users who have been to UK )
N1 = 0
N2 = 0

# using SearchCursor to append the rows to the list
with arcpy.da.SearchCursor(table,field) as cur:

    for row in cur:
        list1.append(row[0])

#------------------------------------------------------------------------------------------------------------------

# processing the data from unicode to seperated strings

#------------------------------------------------------------------------------------------------------------------

# converting the list from Unicode to String

for items in list1:

    list1_updated = [str(i)for i in list1]


# spliting each item in the list to use it for index comparison
split_list = [i.split(',') for i in list1_updated]



for row in split_list:
    #------------------------------------------------------------------------------------------------------------------

    # converting the strings to integers for index search for each entered country code by the user

    #------------------------------------------------------------------------------------------------------------------


    items = map(int, row)



    #------------------------------------------------------------------------------------------------------------------

    # finding if both user defined country codes exist in the row then using the index value for both entered country codes to find if
    # the index of country code B is occured after country code B in each row.

    #------------------------------------------------------------------------------------------------------------------


    if ctyA in items and ctyB in items:


# If Country B index is After A ( less than ), then  add 1 to N1
        i1 = items.index(ctyA)
        i2 = items.index(ctyB)

        if i2>i1:

            N1+=1


# if it's not, then pass the row
    else:
        pass

#------------------------------------------------------------------------------------------------------------------

# If item A is in the row then, add 1 to N2. If it's not, then pass the row

#------------------------------------------------------------------------------------------------------------------

for row in split_list:
    items2 = map(int, row)
    if ctyA in items2:
        N2+=1

    else:
        pass


#------------------------------------------------------------------------------------------------------------------

# Calculating the Probability using the sum of N1 and the sum of N2

#------------------------------------------------------------------------------------------------------------------

# Defining Probability variable
Propability = float(N1)/ float(N2) * 100


#------------------------------------------------------------------------------------------------------------------

# Adding messages for the probability results and N1, N2 sums

#------------------------------------------------------------------------------------------------------------------

arcpy.AddMessage("The probability to visit " + ctyB_1 + " after visiting " + ctyA_1 + " is : " + str("{:0.2f}%".format(Propability))  + "\n")

arcpy.AddMessage("N1 = " + str(N1) + "\n")

arcpy.AddMessage("N2 = " + str(N2) + "\n")

#------------------------------------------------------------------------------------------------------------------

# Creating a text file of the output results

with open(output_folder+'/Probability_Results.csv', 'ab') as result:
            writter = csv.writer(result, delimiter=',')
            empty = os.stat(output_folder+'/Probability_Results.csv').st_size
            if empty ==0:
                writter.writerow(['Country_A','Country_B','Propability',"Probability_Interpretation"])
            #writter.writerow([str(N1), str(N2),str(Propability)])
            writter.writerow([ctyA_1, ctyB_1,str(Propability), "The probability of visiting " + ctyB_1 + " after visiting " + ctyA_1 + " is : " + str("{:0.2f}%".format(Propability))])

#------------------------------------------------------------------------------------------------------------------

# END OF THE TOOL

#------------------------------------------------------------------------------------------------------------------
