# Imports
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
car_sales = pd.read_csv('./static/vehicles_us.csv')


# Some helper functions
def replace_missing(col, how="mean"):
    """This function takes a column and fills in the missing values with a metric of choice, default is mean.
    In case of the metric is not existing returns the column with missing values untouched.
    """
    try:
        value = col.__getattribute__(how)()
        return col.fillna(value=value)
    except AttributeError:
        return col


# Add a a title and a description for the project
st.title('Research on car sales ads')
st.write("""
We're an analysts at Crankshaft List. Hundreds of free advertisements for vehicles are published on our site every day.
We need to study data collected over the last few years and determine which factors influence the price of a vehicle.
""")
col1, col2, col3 = st.columns(3)
with col2:
    st.image('car_sales.png')
# Show some info about the data: sample, description, information
# Random sample
st.write('## Open the data file and study the general information.')
st.write('A random sample of the data')
st.write(car_sales.sample(10))
# Description
st.write('Statistical description of the numeric features')
st.write(car_sales.describe())
# Information
df_info = pd.DataFrame(car_sales.dtypes.astype('str'), columns=['dtypes'])
df_info['Missing'] = car_sales.isnull().sum()
df_info['Uniques'] = car_sales.nunique()
df_info['Total'] = car_sales.count()

st.write(df_info)

# Write a conclusion for this step
st.write('## Conclusion')
st.write("""
We start by loading the data. All the entries are saved as a CSV file, meaning we have to use the "pandas" library to 
read the data and save them as a pandas DataFrame.

Reading the data was easy and now it's time to use one of the helper functions we wrote earlier and print some useful 
information about the dataset. 

 - To gain a better understanding of how the data are, we take a look at a sample of 10 random rows from the dataset. 
 At a glance, we see the column names and different data types. We start getting a feeling of what we have to work with.
 - Seeing only a small sample helps not, that's why we continue seeing a  table with all kinds of useful information of 
 each column as the data type if it has missing values, the number of features, and entries. For our example, we have to
  do with 13 features, 51525 entries, different data types, missing values, and a size of 5 Mb.
 - Knowing that some of the values are numeric, we decide to go further by checking some summary statistics for each 
 numeric feature. Some important metrics are: 
    - `mean:` shows the average value for each feature
    - `min/max:` check the min and max values of each feature and control if it makes sense with the nature of the 
    feature. We can have for example a negative value to represent years (unless is given to us this information).
    - `median/50%:` is one of the most important metrics here. If this value is close to the mean, we have not outliers
     or values that represent extreme cases.


Finally, we control the missing values using a heatmap. It's a nice way to see quantitative information visually as we 
now have a real feeling of the values that are missing.

**Quick take away:**
`Price` is the metric we want to understand the most
- no missing values
- it has definitely outliers
- min makes no sense

*`is_4wd` has the most of the missing values*

*`days_listed` has a min values that makes no sense* 

*`odometer`* has also outliers and min value that need further study.
""")

st.write("""
Explanation of some of the features:
 - fuel — gas, diesel, etc.
 - odometer — the vehicle's mileage when the ad was published
 - is_4wd — whether the vehicle has 4-wheel drive (Boolean type)
 - date_posted — the date the ad was published
 - days_listed — from publication to removal
 - days_listed — from publication to removal
""")

# Start some data preprocessing
st.write('## Data preprocessing')
st.write('### Identify and study missing values')
st.write("""
In the last step, we identify some missing values is a good tactic to tackle this problem now as it will help for our 
analysis later. A basic step we have to do before we go further is to understand the nature of the missing values, 
are they missing values or the absence of them is meaning something else. For example, we saw that the feature `is_4wd`
 has a lot of missing values but what this feature explains is the ability of a car to drive on four wheels. 
 So the absence of values is meaning that this car has not this feature. Ok now let's dive in 🤿!
""")

# How many missing values are there?
missing = pd.DataFrame(
    {
        "total_missing_values": car_sales.isnull().sum(),
        "pct%_missing_values": car_sales.isnull().sum() / len(car_sales) * 100,
    }
)
missing = missing[missing["total_missing_values"] > 0].dropna()
st.write(missing)

# Replace missing values with 0
car_sales["is_4wd"].fillna(value=0, inplace=True)

# Create a pivot table where we group by model and calculate the median of cylinders and model year for each model
pivot_model = car_sales.pivot_table(index=['model'], values=['cylinders', 'model_year'], aggfunc='median')
# Create a pivot table where we group by condition and calculate the median of odometer for each model
pivot_condition = car_sales.pivot_table(index=['condition'], values=['odometer'], aggfunc='median')


def replace_cylinders_grouped(row):
    """Take a row of the dataset and replace the cylinders with a value from the pivot table"""
    model = row['model']
    cylinders = row['cylinders']
    return pivot_model.loc[model]['cylinders']


def replace_model_year_grouped(row):
    """Take a row of the dataset and replace the model_year with a value from the pivot table"""
    model = row['model']
    cylinders = row['model_year']
    return pivot_model.loc[model]['model_year']


def replace_odometer_grouped(row):
    """Take a row of the dataset and replace the odometer with a value from the pivot table"""
    condition = row['condition']
    odometer = row['odometer']
    return pivot_condition.loc[condition]['odometer']


# Replace the values for cylinders
car_sales.loc[car_sales['cylinders'].isnull(), ['cylinders']] = (car_sales
                                                                 .query('cylinders.isnull()')
                                                                 .loc[:, ['model', 'cylinders']]
                                                                 .apply(replace_cylinders_grouped, axis=1))
# Replace the values for model_year
car_sales.loc[car_sales['model_year'].isnull(), ['model_year']] = (car_sales
                                                                   .query('model_year.isnull()')
                                                                   .loc[:, ['model', 'model_year']]
                                                                   .apply(replace_model_year_grouped, axis=1))

# Replace the values for odometer
car_sales.loc[car_sales['odometer'].isnull(), ['odometer']] = (car_sales
                                                               .query('odometer.isnull()')
                                                               .loc[:, ['condition', 'odometer']]
                                                               .apply(replace_odometer_grouped, axis=1))

car_sales["paint_color"].fillna(value="unknown", inplace=True)

# Columns to turn into integers
cols_to_int = ["model_year", "cylinders", "days_listed"]
# Columns to turn into categories
cols_to_cat = ["fuel", "condition", "transmission", "is_4wd"]
# Dictionary with data types for each column name
types = {"int16": cols_to_int, "category": cols_to_cat}

for each in types.items():
    for col in each[1]:
        car_sales[col] = car_sales[col].astype(each[0])

# Date conversion
car_sales["date_posted"] = pd.to_datetime(car_sales["date_posted"])

st.write("""
After some preprocessing we fill the missing values and also took care of some wrong data types. Now, let's see how the
 data look like.
""")
df_info = pd.DataFrame(car_sales.dtypes.astype('str'), columns=['dtypes'])
df_info['Missing'] = car_sales.isnull().sum()
df_info['Uniques'] = car_sales.nunique()
df_info['Total'] = car_sales.count()
st.write(df_info)

# Finish this step with a conclusion
st.write('## Conclusion')
st.write("""
Our goal here was to tide a bit up our data frame. We started from the missing values as it is important for our 
analysis.
First, we checked which features have missing values and plotted them as a data frame which shows apart from the count 
the percentage of the values that are missing. 

- `is_4wd` has a massive absence of values, but after understanding what this feature describes was easy to fill them 
up.

- Numeric values were filled up using the median as we have outliers, and the median is the metric to go in this case. 

- For `model_year` we decided to drop the missing values as saw that the lack of these values changes not the 
distribution of the price. So no vehicles missing with some importance for the price.

- `paint_color` is a feature with 20% of missing values, dropping them will cause some problems to our analysis, so we 
choose to replace these values with a new  color: **unknown**

This step is over and our data look already nicer, now it's time to check the data types. 
 - For small numeric values, we choose an integer of 16 bits and leave the big float number as they are.
 - Values that represent a category and have no quantitive meaning will be changes to category data type, as it helps
  pandas to handle them better and cost less space on the disk.
 - Finally, we parsed dates as it helps to make some quick calculations later.

The last step was to check for duplicates. Duplicates can appear in different forms, it can be a row that repeats 
itself for some reason, or it can appear in some categorical values if we have twice or more the same category name. 
Also, this helps to check the values each category has and catch mistakes early. 

Now the field is clear to go 😮‍💨
""")

# Next step, some feature engineering
st.write('### Feature engineering')
# Split date into: day_of_week, month, year
car_sales["year"] = car_sales["date_posted"].dt.year
car_sales["month"] = car_sales["date_posted"].dt.month
car_sales["day_of_week"] = car_sales["date_posted"].dt.dayofweek

# Calculate the age of the vehicle
car_sales["age"] = car_sales["year"] - car_sales["model_year"]
# Set age to 1 for those that have model year the same year as the date of post
car_sales.loc[car_sales["age"] == 0, "age"] = 1

# Calculate the vehicle's average mileage per year
car_sales["mileage"] = (car_sales["odometer"] / car_sales["age"]).astype("float32")

# In the condition column, replace string values with a numeric
# scale:new = 5, like new = 4, excellent = 3, good = 2, fair = 1, salvage = 0
car_sales["condition"] = (
    car_sales["condition"]
        .replace(
        ["new", "like new", "excellent", "good", "fair", "salvage"], [5, 4, 3, 2, 1, 0]
    )
        .astype("category")
)

# Create a new feature for the constructor of the vehicle
car_sales["constructor"] = car_sales["model"].apply(lambda x: x.split(" ")[0])

st.write(car_sales.sample(10))

st.write('## Conclusion')
st.write("""
This step is more like feature engineering. We use some of the fields to create new calculations.

- We parsed dates earlier so now we have the advantage to split dates into smaller chunks like *years, months, 
days, etc.*

- We can easily calculate the age of a posted vehicle, as it is more informative instead of looking at the year of 
construction and calculate the age ourselves.  **Warning**: *Some vehicles are rather new and as we calculate the 
age considering only the year we end up with zeroes. We decide to change this with 1.*
- An important feature will be the `mileage`. It will be representing the average mileage (odometer) a vehicle has, 
to calculate it we just divide the odometer by age.
- We extract the name of the factory or the manufacturer of each vehicle. 
""")

st.write('###  Carry out exploratory data analysis')

# Set the names of the columns we want to plot
col = ["price", "mileage", "cylinders", "condition"]
fig, axes = plt.subplots(nrows=4)
fig.set_size_inches(10, 20)
for ax, name in zip(axes.flatten(), col):
    ax.hist(car_sales[name])
    ax.set_title(name, fontdict={'fontsize': 12})

plt.tight_layout()
st.pyplot(fig)

st.write("""
Earlier we took a look at some summary statistics for some values and draw some conclusions. To check if we were right we made some plots. 

Histograms are plots that show the distribution of a value. It is a stacked representation of frequencies so it is better used for understanding numeric features. Categorical values have bar plots, something similar to histograms but it measures the frequency of a category rather than a number.

`price` and `mileage` are skewed to the right. This confirms the presence of outliers and the existence of extremes in both directions.  

`cylinders` is a district numeric feature and this explains the fact why it looks like a categorical feature. 

`condition` is a category so we see the frequency each category appears, with 0 and 5 being completely outnumbered from the other categories.
""")

# Plotbox the original price
fig, ax = plt.subplots()
ax.boxplot(car_sales["price"])
ax.set_title("Boxplot of Price")
st.pyplot(fig)

# Zoom at a specific range of price
fig, ax = plt.subplots()
ax.hist(car_sales['price'], range=(0, 1000), bins=30)
# car_sales["price"].plot(kind="hist", range=(0, 1000), bins=30)
ax.set_title("Histplot of Price in range 0-1000")
st.pyplot(fig)

# Print the values in range of 3rd - 97th quantile
st.write("3% of the data have price under: {}".format(car_sales["price"].quantile(0.03)))
st.write("98% of the data have price under: {}".format(car_sales["price"].quantile(0.97)))

# Plotbox the original mileage
fig, ax = plt.subplots()
ax.boxplot(car_sales["mileage"])
ax.set_title("Boxplot of mileage")
st.pyplot(fig)

# Zoom in a specific range of mileage
fig, ax = plt.subplots()
ax.hist(car_sales['mileage'], range=(0, 2500))
ax.set_title("Histplot of mileage in range 0-2000")
st.pyplot(fig)

# Print the values in range of 3rd - 97th quantile
st.write(
    "3% of the data have mileage under: {}".format(car_sales["mileage"].quantile(0.03))
)
st.write(
    "98% of the data have mileage under: {}".format(car_sales["mileage"].quantile(0.97))
)

# Filter the data with price in range 1000 - 35000
filtered_data = car_sales[(car_sales["price"] > 1000) & (car_sales["price"] < 35000)]
# Make a sample of high prices, 2% of the data
high_price = car_sales[car_sales["price"] > 35000]

# Filter the data withe mileage in range 2500 - 57000
filtered_data = filtered_data[
    (filtered_data["mileage"] > 2500) & (filtered_data["mileage"] < 57000)
    ]

st.write(
    "We lost {:.2%} of the data after filtering out the outliers".format(
        (len(car_sales) - len(filtered_data)) / len(car_sales)
    )
)

st.write("""
Boxplots show us very clearly the effect of the outliers, also help us define some boundaries where most of the data lie into. 

We decide to keep data that have a value bigger than the third quantile and smaller than the ninety-seventh, this means we left out 3% of both edges of the data.

Ranges:
- **Price**: `1000 - 35000`
- **Mileage**: `2500 - 57000` 

This translates to a loss of 10% of the data. 
""")

# Set the names of the columns we want to plot
col = ["price", "mileage"]

# Make the figures to plot on
fig, axes = plt.subplots(ncols=2, nrows=2)
fig.set_size_inches(20, 10)

# Plot the price of the original and filtered data
axes[0][1].hist(filtered_data["price"], bins=50)
axes[0][1].set_title("Filtered price", fontdict={"fontsize": 12})
axes[0][0].hist(car_sales["price"])
axes[0][0].set_title("orignal price", fontdict={"fontsize": 12})

# Plot the mileage of the original and filtered data
axes[1][1].hist(filtered_data["mileage"], bins=50)
axes[1][1].set_title("Filtered mileage", fontdict={"fontsize": 12})
axes[1][0].hist(car_sales["mileage"])
axes[1][0].set_title("orignal mileage", fontdict={"fontsize": 12})

fig.suptitle(
    "Comparison of features between original and filtered data",
    fontdict={"fontsize": 20},
)
plt.tight_layout()
st.pyplot(fig)

st.write("""
Plotting both features now shows the effect of the previous step. Looking at the filtered data we can understand better the ranges and the behavior of each feature. We keep having a right tail but it's much better and informative than the original one. The loss of the data was a sacrifice we had to make.
""")

pivot_price_type = filtered_data.pivot_table(
    index="type", values=["price"], aggfunc=["mean", "count"]
)

pivot_price_type.columns = [
    "average_price",
    "count",
]

pivot_price_type.sort_values(by="count", inplace=True, ascending=False)

st.write("""
 Analyze the number of ads and the average price for each type of vehicle. 
 Plot a graph showing the dependence of the number of ads on the vehicle type. 
 Select the two types with the greatest number of ads.
""")
st.write(pivot_price_type)

fig, ax = plt.subplots()

ax.bar(pivot_price_type.index, pivot_price_type["count"])
ax.set_xlabel("Vehicle type")
ax.set_ylabel("Count of ads for each type")
ax.tick_params(axis="y", colors="C0")
ax.tick_params(axis="x", rotation=90)

ax2 = ax.twinx()
ax2.plot(
    pivot_price_type.index, pivot_price_type["average_price"], color="C1", marker="D"
)
ax2.set_ylabel("Average price of vehicles")
ax2.tick_params(axis="y", colors="C1")
ax2.grid(0)

plt.tight_layout()
st.pyplot(fig)

st.write("""
On the graph above we have combined a bar chart showing the number of vehicles' types, with a lineplot showing 
the average price for each type. As we see the three dominant categories are SUVs, sedans, and trucks. 
Although sedans are in the top three the average price for this kind of vehicle is quite low in comparison with the 
other two. So if we have to choose two dominant categories from our site, it will be the SUV and trucks, as they seem 
to be listed most of the time and also, have the higher price.💯💰
""")

st.write('## Detailed analyses of SUV type')

# We filter out the three most common vehicle types to make our analysis.
data_sample = filtered_data.loc[filtered_data["type"].isin(["SUV"])]

# Features to plot
cat_values = ["paint_color", "condition", "transmission", "constructor"]
num_values = ["age", "mileage", "price"]

# Check numeric values
fig, ax = plt.subplots()
pd.plotting.scatter_matrix(car_sales[num_values], figsize=(20, 15), diagonal="kde", ax=ax)
plt.tight_layout()
st.pyplot(fig)

# Relation of color with price and odometer
pivot_price_odometer_color = data_sample.pivot_table(
    index="paint_color",
    values=["price", "odometer", "constructor"],
    aggfunc={"price": "median", "odometer": "mean", "constructor": "count"},
)

# Relation of condition with price and odometer
pivot_price_odometer_condition = data_sample.pivot_table(
    index="condition",
    values=["price", "odometer", "constructor"],
    aggfunc={"price": "median", "odometer": "mean", "constructor": "count"},
)

# Relation of transmission with price and odometer
pivot_price_odometer_trans = data_sample.pivot_table(
    index="transmission",
    values=["price", "odometer", "constructor"],
    aggfunc={"price": "median", "odometer": "mean", "constructor": "count"},
)

# Relation of constructor with price and odometer
pivot_price_odometer_const = data_sample.pivot_table(
    index="constructor",
    values=["price", "odometer", "type"],
    aggfunc={"price": "median", "odometer": "mean", "type": "count"},
)

# Plot all scatterplots
#######################################################################################################################
# COLOR
#######################################################################################################################
fig, ax = plt.subplots()
sns.scatterplot(
    x="price",
    y="odometer",
    data=pivot_price_odometer_color,
    size="constructor",
    sizes=(50, 500),
    ax=ax
)

for name in pivot_price_odometer_color.index:
    coordinates = (
        pivot_price_odometer_color.loc[name][2],
        pivot_price_odometer_color.loc[name][1],
    )
    plt.annotate(
        s=name,
        xy=coordinates,
        textcoords="offset points",
        xytext=(10, -30),
        ha="right",
        arrowprops={"color": "red", "arrowstyle": "simple"},
        fontsize=12,
        bbox=dict(facecolor="red", alpha=0.5),
        color="w",
    )
plt.xlabel("median price")
plt.ylabel("average odometer")
plt.title(
    "Correlation between median of Price and average of Odometer for all records grouped by color."
)

st.pyplot(fig)

#######################################################################################################################
# CONDITION
#######################################################################################################################
fig, ax = plt.subplots()
sns.scatterplot(
    x="price",
    y="odometer",
    data=pivot_price_odometer_condition,
    size="constructor",
    sizes=(50, 500),
    ax=ax
)

for name in pivot_price_odometer_condition.index:
    coordinates = (
        pivot_price_odometer_condition.iloc[name][2],
        pivot_price_odometer_condition.iloc[name][1],
    )
    plt.annotate(
        s=name,
        xy=coordinates,
        textcoords="offset points",
        xytext=(-10, 20),
        ha="right",
        arrowprops={"color": "red", "arrowstyle": "simple"},
        fontsize=12,
        bbox=dict(facecolor="red", alpha=0.5),
        color="w",
    )
plt.xlabel("median price")
plt.ylabel("average odometer")
plt.title(
    "Correlation between median of Price and average of Odometer for all records grouped by condition."
)

st.pyplot(fig)

#######################################################################################################################
# TRANSMISSION
#######################################################################################################################
fig, ax = plt.subplots()
sns.scatterplot(
    x="price",
    y="odometer",
    data=pivot_price_odometer_trans,
    size="constructor",
    sizes=(50, 500),
    ax=ax
)

for name in pivot_price_odometer_trans.index:
    coordinates = (
        pivot_price_odometer_trans.loc[name][2],
        pivot_price_odometer_trans.loc[name][1],
    )
    plt.annotate(
        s=name,
        xy=coordinates,
        textcoords="offset points",
        xytext=(20, -20),
        ha="left",
        arrowprops={"color": "red", "arrowstyle": "simple"},
        fontsize=12,
        bbox=dict(facecolor="red", alpha=0.5),
        color="w",
    )
plt.xlabel("median price")
plt.ylabel("average odometer")
plt.title(
    "Correlation between median of Price and average of Odometer for all records grouped by transmission."
)

st.pyplot(fig)

#######################################################################################################################
# CONSTRUCTOR
#######################################################################################################################
fig, ax = plt.subplots()
sns.scatterplot(
    x="price",
    y="odometer",
    data=pivot_price_odometer_const,
    size="type",
    sizes=(50, 500),
    ax=ax
)

for name in pivot_price_odometer_const.index:
    coordinates = (
        pivot_price_odometer_const.loc[name][1],
        pivot_price_odometer_const.loc[name][0],
    )
    plt.annotate(
        s=name,
        xy=coordinates,
        textcoords="offset points",
        xytext=(-10, -20),
        arrowprops={"color": "red", "arrowstyle": "simple"},
        fontsize=12,
        bbox=dict(facecolor="red", alpha=0.5),
        color="w",
    )
plt.xlabel("median price")
plt.ylabel("average odometer")
plt.title(
    "Correlation between median of Price and average of Odometer for all records grouped by Constructor."
)

st.pyplot(fig)

st.write("## Final Conclusion")
st.write("""
With the step above, our analysis has concluded. The steps we took to come here make us learn a lot about our data. 

We saw from an early point that we have outliers, now we know that these outliers are because of vehicles that are unique cases in comparison with the norm.

We managed to find out ranges to filter our values safe without the influence of any outliers.

We discovered the most popular vehicle types on our site were:
- SUV
- Sedan
- Trucks

Despite that, these types except trucks have a low median price in comparison with other types such as *pickup* and *coupe*. Also, we spot some expensive types with only a few post, this has to do with the fact that these types are more for professionals or people with specific interests, like a bus driver or an offroad enthusiast.

After sampling only the most popular categories we decided to find out what configures the price of each vehicle. Here come the correlations into the play, a powerful metric that shows how each feature is correlated, in our case, with the price. We calculate the Spearman rank correlation as it not so sensitive with outliers and extreme values. The features that influence the price the most are the `model_year`, the `mileage`, and the cylinders of the vehicle. We came up with the assumption that this finding follows common sense and nothing surprising there.

To have the correlations metric as a number is not enough, we plot scatterplots for the price, mileage, and age to see if the correlation is clear visually. Age has a negative strong correlation and mileage a weak positive, both are visible on the plots.

The final and most informative part was the grouping and plotting of some categorical features in comparison with the price and odometer. We could have used boxplots but it wouldn't have captured the details we have now.

**Findings:**

*Color vs Price vs Odometer*
 - SUVs: For the SUVs, color separates the data into two big categories the ones with low median price and big mileage and the others with average median price and mileage. There is also one color that stands out, orange.
 
 - Sedans: For sedans, the orange is again the color that stands out with the highest median price and lower mileage. Also, we can see again that most of the colors are gathered at the middle of the plot showing an average in both features -price and mileage.

*Condition vs Price vs Odometer*
The most common condition is the 2 --> good and 3 --> excellent, where you find vehicles with a fair median price and average mileage.
Interesting enough is that vehicles in the "new" category (5) tend to be sold with more mileage than the vehicles in the like-new (4) category

*Transmission vs Price vs Odometer*
Automatic is the dominant category with an average price and mileage. The other two categories are not so popular. For SUVs automatic shows a tendency to low priced and big odometer while in sedans we have vehicles with high prices and lower odometer.

*Manufacturer vs Price vs Odometer*
For the SUVs, the odometer seems not to be influenced by the manufacturer although the price changes for different brands with Chrysler to stand out with the highest median price.
For the sedans is quite the opposite, the price seems to stay steady for different manufacturers but the odometer changes. Ram and Cadillac are the two domina categories here.

So if you are looking for a car have that in mind:

If you want an SUV and don't want to spend much, then it has to be automatic, green, or blue and for a manufacturer, Acura seems a fine choice.

Now if you want a sedan, try to avoid automatic vehicles, for the color search for a green one and the manufacturer is not so important as long as is not Cadillac or ram.

""")

col1, col2, col3 = st.columns(3)
with col1:
    st.image('./static/accura.png')
with col2:
    st.image('./static/ford.png')
with col3:
    st.image('./static/ram.png')
