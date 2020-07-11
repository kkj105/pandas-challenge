#!/usr/bin/env python
# coding: utf-8

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[1]:


# Dependencies and Setup
import pandas as pd

# File to Load (Remember to Change These)
file_to_load = "Resources/purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_data = pd.read_csv(file_to_load)
purchase_data.head(15)


# ## Player Count

# * Display the total number of players
# 

# In[2]:



# Calculate the total number of players 
player_count=len(purchase_data["SN"].unique())

# Convert a dictionary into a dataframe
players_dict=[{"Total Players": (player_count)}]
totalplayers_df=pd.DataFrame(players_dict)
totalplayers_df


# ## Purchasing Analysis (Total)

# * Run basic calculations to obtain number of unique items, average price, total number of purchases, & total revenue
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame
# 

# In[3]:


# Calculate the total number of unique items
count_uniqueitems=len(purchase_data["Item ID"].unique())

# Calculate the average item price
average_price=purchase_data["Price"].mean()

#Calculate the total number of purchases
number_purchases=len(purchase_data["Purchase ID"].unique())

# Calculate the total revenue
total_revenue=purchase_data["Price"].sum()

# Display new summary data frame using a dictionary of lists
summary_df=pd.DataFrame({"Number of Unique Items": [(count_uniqueitems)], 
                         "Average Price": [(average_price)], "Number of Purchases": [(number_purchases)], 
                         "Total Revenue": [(total_revenue)]})

# Convert "Average Price" & "Total Revenue" columns to float, format to two decimal places and include dollar sign
summary_df["Average Price"]=summary_df["Average Price"].astype(float).map("${:,.2f}".format)
summary_df["Total Revenue"]=summary_df["Total Revenue"].astype(float).map("${:,.2f}".format)
summary_df


# ## Gender Demographics

# * Percentage and Count of Male Players
# 
# 
# * Percentage and Count of Female Players
# 
# 
# * Percentage and Count of Other / Non-Disclosed
# 
# 
# 

# In[4]:


# Using GroupBy, pull by "Gender" to count the unique instances of "SN"
purchase_data.groupby("Gender")["SN"].nunique()


# In[5]:


# Convert the gender_count Series into a DataFrame
gender_count_df = pd.DataFrame(purchase_data.groupby("Gender")["SN"].nunique())
gender_count_df.head()


# In[6]:


# Convert the column name into "Total Count" & then calculate the percentage from "Total Count"
gender_count_df = gender_count_df.rename(
    columns={"SN": "Total Count"})
gender_count_df["Percentage of Players"]=gender_count_df["Total Count"]/gender_count_df["Total Count"].sum()
gender_count_df.head()


# In[7]:


# Display demographic data frame & map as %
gender_count_df["Percentage of Players"] = gender_count_df["Percentage of Players"].map("{:.2%}".format)
gender_count_df


# 
# ## Purchasing Analysis (Gender)

# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender
# 
# 
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[8]:


# Calculate the total number of purchases 
purchase_count=len(purchase_data["Purchase ID"].unique())
purchase_count


# In[9]:


# Using GroupBy, pull by "Gender" to count the unique instances of "Purchase ID"
purchase_data.groupby("Gender")["Purchase ID"].nunique()

# Convert the purchase_count Series into a DataFrame
purchase_count_df = pd.DataFrame(purchase_data.groupby("Gender")["Purchase ID"].nunique())
purchase_count_df.head()


# In[10]:


# Using GroupBy, pull by "Gender" to find the average purchase price - to be relabeled "Average Purchase Price"
purchase_data.groupby("Gender")["Price"].mean()

# Convert the avg_price Series into a DataFrame
avg_price_df = pd.DataFrame(purchase_data.groupby("Gender")["Price"].mean())
avg_price_df.head()


# In[11]:


# Using GroupBy, pull by "Gender" to sum the instances of "Price" - to be relabled "Total Purchase Value"
purchase_data.groupby("Gender")["Price"].sum()

# Convert the purchase_value Series into a DataFrame
purchase_value_df = pd.DataFrame(purchase_data.groupby("Gender")["Price"].sum())
purchase_value_df.head()


# In[12]:


# trying to create DataFrame from raw data rather than csv. Include the "Total Count" column to calculate
    # Avg total, then delete the "Total Count" column. Will also need to change index label
# Convert a single dictionary containing lists into a dataframe
purchase_analysis_df = pd.DataFrame(
    {"Purchase Count": purchase_count_df["Purchase ID"],
     "Total Count": gender_count_df["Total Count"],
     "Average Purchase Price": avg_price_df["Price"],
     "Total Purchase Value": purchase_value_df["Price"]
     }
)
purchase_analysis_df


# In[13]:


# Add new column "Avg Total Purchase per Person" & calculate that average
purchase_analysis_df["Avg Total Purchase per Person"]=purchase_analysis_df["Total Purchase Value"]/purchase_analysis_df["Total Count"]
purchase_analysis_df


# In[14]:


# Delete "Total Count" column
del purchase_analysis_df["Total Count"]


# In[15]:


# Display purchase analysis dataframe & map with $
purchase_analysis_df["Average Purchase Price"] = purchase_analysis_df["Average Purchase Price"].map("${:.2f}".format)
purchase_analysis_df["Total Purchase Value"] = purchase_analysis_df["Total Purchase Value"].map("${:,.2f}".format)
purchase_analysis_df["Avg Total Purchase per Person"] = purchase_analysis_df["Avg Total Purchase per Person"].map("${:.2f}".format)
purchase_analysis_df


# ## Age Demographics

# * Establish bins for ages
# 
# 
# * Categorize the existing players using the age bins. Hint: use pd.cut()
# 
# 
# * Calculate the numbers and percentages by age group
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: round the percentage column to two decimal points
# 
# 
# * Display Age Demographics Table
# 

# In[16]:


# Figure out the minimum and maximum ages in the data
print(purchase_data["Age"].max())
print(purchase_data["Age"].min())


# In[17]:


# Create the bins in which to place values based upon ages  
bins = [0, 9.9, 14.9, 19.9, 24.9, 29.9, 34.9, 39.9, 49.9]

# Create the names for the bins
age_groups = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]


# In[18]:


# Drop SN duplicate purchases
demographics=purchase_data.drop_duplicates("SN")
demographics.head()


# In[19]:


# Slice the data and place it into bins
pd.cut(demographics["Age"], bins, labels=age_groups).head(10)


# In[20]:


# Place the data series into a new column inside of the DataFrame
demographics["Age Summary"]=pd.cut(demographics["Age"], bins, labels=age_groups, include_lowest=True)
demographics.head()


# In[21]:


# NEED TO RECOMMENT THIS Using GroupBy, pull by "Age Summary" to count the instances of "Age"
totalcount=demographics["Age Summary"].value_counts()
totalcount


# In[22]:


# Convert the TotalCount Series into a DataFrame & sort index 
totalcount=totalcount.to_frame().sort_index()


# In[23]:


# Convert the column name into "Total Count" & then calculate the percentage from "Total Count"
totalcount=totalcount.rename(
    columns={"Age Summary": "Total Count"})
totalcount["Percentage of Players"]=totalcount["Total Count"]/totalcount["Total Count"].sum()

# Display total count data frame & map as %
totalcount["Percentage of Players"] = totalcount["Percentage of Players"].map("{:.2%}".format)
totalcount


# ## Purchasing Analysis (Age)

# * Bin the purchase_data data frame by age
# 
# 
# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[24]:


# Create the bins in which to place values based upon ages  
bins = [0, 9.9, 14.9, 19.9, 24.9, 29.9, 34.9, 39.9, 49.9]

# Create the names for the bins
age_groups = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]


# In[25]:


# Slice the data and place it into bins
pd.cut(purchase_data["Age"], bins, labels=age_groups).head()


# In[26]:


# Place the data series into a new column inside of the DataFrame
purchase_data["Age Summary"]=pd.cut(purchase_data["Age"], bins, labels=age_groups, include_lowest=True)
purchase_data.head()


# In[27]:


# Create a GroupBy object based upon "Age Summary" - this makes it the index of the dataframe
age_analysis=purchase_data.groupby("Age Summary")


# In[28]:


# Find how many rows fall into each bin
print(age_analysis["Age"].count())

# Convert age_analysis series into a DataFrame
purchase_count=pd.DataFrame(age_analysis["Age"].count())


# In[29]:


# Get the Average Price of the "Price" column within the GroupBy object
age_analysis[["Price"]].mean()

# Convert the age_analysis series into a DataFrame
average_price=pd.DataFrame(age_analysis[["Price"]].mean())
average_price


# In[30]:


# Using GroupBy, pull by "Age Summary" to sum the instances of "Price" - to be relabled "Total Purchase Value"
purchase_data.groupby("Age Summary")["Price"].sum()

# Convert the age_analysis Series into a DataFrame
purchase_value=pd.DataFrame(purchase_data.groupby("Age Summary")["Price"].sum())
purchase_value


# In[31]:


# Using GroupBy, pull by "Gender" to count the unique instances of "SN"
purchase_data.groupby("Age Summary")["SN"].nunique()

# Convert the gender_count Series into a DataFrame
age_count = pd.DataFrame(purchase_data.groupby("Age Summary")["SN"].nunique())
age_count.head()


# In[32]:


# Convert into a dataframe
purchaseanalysis=pd.DataFrame(
    {"Purchase Count": purchase_count["Age"],
    "Average Purchase Price": average_price["Price"],
    "Total Purchase Value": purchase_value["Price"],
    "Total Count": age_count["SN"]})
purchaseanalysis


# In[33]:


# Add new column "Avg Total Purchase per Person" & calculate that average
purchaseanalysis["Avg Total Purchase per Person"]=purchaseanalysis["Total Purchase Value"]/purchaseanalysis["Total Count"]
purchaseanalysis


# In[34]:


# Delete "Total Count" column
del purchaseanalysis["Total Count"]


# In[35]:


# Display purchase analysis dataframe & map with $
purchaseanalysis["Average Purchase Price"] = purchaseanalysis["Average Purchase Price"].map("${:.2f}".format)
purchaseanalysis["Total Purchase Value"] = purchaseanalysis["Total Purchase Value"].map("${:,.2f}".format)
purchaseanalysis["Avg Total Purchase per Person"] = purchaseanalysis["Avg Total Purchase per Person"].map("${:.2f}".format)
purchaseanalysis


# ## Top Spenders

# * Run basic calculations to obtain the results in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the total purchase value column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[36]:


# Delete "Age Summary" column & print DataFrame
del purchase_data["Age Summary"]
purchase_data.head()


# In[37]:


# Create a GroupBy object based upon "SN" 
namelist=purchase_data.groupby("SN")


# In[38]:


# Find how many rows fall into each bin
print(namelist["SN"].count())

# Convert namelist series into a DataFrame
screen_names=pd.DataFrame(namelist["SN"].count())


# In[39]:


# Using GroupBy, pull by "SN" to find the total number of "Purchase ID"
purchase_data.groupby("SN")["Purchase ID"].count()

# Convert the series into a DataFrame
purchase_count=pd.DataFrame(purchase_data.groupby("SN")["Purchase ID"].count())
purchase_count.head()


# In[40]:


# Using GroupBy, pull by "Price" to count the unique instances of "SN"
purchase_data.groupby("SN")["Price"].sum()

# Convert the Series into a DataFrame
purchase_total = pd.DataFrame(purchase_data.groupby("SN")["Price"].sum())
purchase_total.head()


# In[41]:


# Get the Average Price of the "Price" column within the GroupBy object
namelist[["Price"]].mean()

# Convert the age_analysis series into a DataFrame
average_price=pd.DataFrame(namelist[["Price"]].mean())
average_price.head()


# In[42]:


# Convert into a dataframe
topspenders=pd.DataFrame(
    {"Purchase Count": purchase_count["Purchase ID"],
    "Average Purchase Price": average_price["Price"],
    "Total Purchase Value": purchase_total["Price"]})
topspenders.head()


# In[43]:


# Sort the DataFrame by the values in the "SN" column to find the biggest spenders & map with $
biggest_spenders=topspenders.sort_values(by=["Total Purchase Value"],ascending=False)

biggest_spenders["Average Purchase Price"]=biggest_spenders["Average Purchase Price"].map("${:.2f}".format)
biggest_spenders["Total Purchase Value"] = biggest_spenders["Total Purchase Value"].map("${:.2f}".format)
biggest_spenders.head()


# ## Most Popular Items

# * Retrieve the Item ID, Item Name, and Item Price columns
# 
# 
# * Group by Item ID and Item Name. Perform calculations to obtain purchase count, item price, and total purchase value
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the purchase count column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[53]:


# Print original DataFrame
purchase_data.head()


# In[54]:


# Extract the following columns: Item ID, Item Name, and Price columns
item_name_df=purchase_data[["Item ID", "Item Name", "Price"]]
item_name_df.head()


# In[58]:


# Using GroupBy in order to separate the data into fields according to Item ID & Item Name
# Also calculate aggregates
grouped_item_name = item_name_df.groupby(["Item ID", "Item Name"])
grouped_item_name["Price"].mean()

mostpopular_df=pd.DataFrame({"Item Price":grouped_item_name["Price"].mean()})
mostpopular_df["Purchase Count"]=grouped_item_name["Price"].count()
mostpopular_df["Total Purchase Value"]=grouped_item_name["Price"].sum()
mostpopular_df


# In[65]:


# Sort the DataFrame by the values in the "Purchase Count" column to find the most
highest_purchasecount=mostpopular_df.sort_values(by=["Purchase Count"],ascending=False)

highest_purchasecount["Item Price"]=highest_purchasecount["Item Price"].map("${:.2f}".format)
highest_purchasecount["Total Purchase Value"] = highest_purchasecount["Total Purchase Value"].map("${:.2f}".format)
highest_purchasecount.head()


# In[66]:


# Reorder columns to match given output
reordered_highest_purchasecount=highest_purchasecount[["Purchase Count","Item Price","Total Purchase Value"]]
reordered_highest_purchasecount.head()


# ## Most Profitable Items

# * Sort the above table by total purchase value in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the data frame
# 
# 

# In[67]:


# Sort the DataFrame by the values in the "Purchase Count" column to find the most
most_profitable=mostpopular_df.sort_values(by=["Total Purchase Value"],ascending=False)

most_profitable["Item Price"]=most_profitable["Item Price"].map("${:.2f}".format)
most_profitable["Total Purchase Value"] =most_profitable["Total Purchase Value"].map("${:.2f}".format)
most_profitable.head()


# In[68]:


# Reorder columns to match given output
reordered_most_profitable=most_profitable[["Purchase Count","Item Price","Total Purchase Value"]]
reordered_most_profitable.head()


# ## Most Profitable Items

# * 1. In examining the Purchasing Analysis by Gender, I was surprised to see that while men outnumber 
#     women in the dataset, it’s women who, on average, spend more money per person.
# * 2. The dataset makes clear that the target audience to market to are: males, between the ages of 20-24. 
#     They make the most purchases and spend more money than any other age group.
# * 3. In looking at the Most Popular and Most Profitable Analyses, it was interesting to see that both have 
#     the same #1 item: “Final Critic”. Followed very closely in both analyses by the #2 item: 
#     “Oathbreaker, Last Hope of the Breaking Storm”.

# In[ ]:




