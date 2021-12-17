# A simple Weather App

<p align=center>
    <img alt="img_2.png" height="150" src="images\img_2.png" width="150"/>
</p>

## Technologies and Tools

![](https://img.shields.io/badge/OS-Windows-informational?style=flat&logo=windows&logoColor=white&color=2bbc8a)
![](https://img.shields.io/badge/Editor-PyCharm-informational?style=flat&logo=pycharm&logoColor=white&color=2bbc8a)
![](https://img.shields.io/badge/Code-Python-informational?style=flat&logo=python&logoColor=white&color=2bbc8a)
![](https://img.shields.io/badge/Database-PostgreSQL-informational?style=flat&logo=PostgreSQL&logoColor=white&color=2bbc8a)
![](https://img.shields.io/badge/Tools-API-informational?style=flat&logo=freeCodeCamp&logoColor=white&color=2bbc8a)

## Introduction

This is a simple application that combines databases, APIs and Python programming. The result of this application is a
simple python script that after execution makes a connection to the database and transfers some weather information of a
city we choose.

## The API

<p align=center>
    <img src="D:\GitHub\Data-Analysis\WeatherApp\images\img_1.png" width="150" height="150" title="an api icon" align="center">
</p>

This app uses weather data acquired from the [OpenWeatherMap](https://openweathermap.org/current). The site demands that
the user makes an account and generates a key unique for their account. After getting the key we can explore the
different ways we can use the API and which information we want to retrieve. For this app the current weather data will
be enough, all the documentation can be found [here](https://openweathermap.org/current). We choose to make requests
using a city name using this call:

`api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}`

where `city name` is the city we want to retrieve the weather data for and the `appid` is our personal API key.

### A small example

To understand better how this works we gonna put the following url to our browser and see what returns.

`api.openweathermap.org/data/2.5/weather?q=Berlin&appid={API key}`

where city name = Berlin and for obvious reasons my API key is omitted. The browser will return something like this:

```json
{
  "coord": {
    "lon": 13.4105,
    "lat": 52.5244
  },
  "weather": [
    {
      "id": 701,
      "main": "Mist",
      "description": "mist",
      "icon": "50n"
    }
  ],
  "base": "
  stations
  ","
  main
  ":{"
  temp
  ":280.91,"
  feels_like
  ":278.62,"
  temp_min
  ":279.13,"
  temp_max
  ":282.04,"
  pressure
  ":1025,"
  humidity
  ":97},"
  visibility
  ":3100,"
  wind
  ":{"
  speed
  ":3.58,"
  deg
  ":213,"
  gust
  ":4.47},"
  clouds
  ":{"
  all
  ":75},"
  dt
  ":1639426447,"
  sys
  ":{"
  type
  ":2,"
  id
  ":
  2011538,
  "country": "DE",
  "sunrise": 1639379354,
  "sunset": 1639407126
},"timezone": 3600, "id": 2950159, "name":"Berlin", "cod": 200
}
```

This is what the API call returns when we ask the browser to `GET` the requested url. It is a json object with all the
information for the current weather in Berlin.

Now in our code later we have to find a way to extract what we need from this response and put it into a dataframe or
database

## The Database

<p align=center>
    <img alt="img.png" height="150" src="D:\GitHub\Data-Analysis\WeatherApp\images\img.png" width="150"/>
</p>

For this project we're going to use [PostgreSQL](https://www.postgresql.org/download/) RDMS. It will allow us to run
powerful SQL queries alongside with extra functionality. After installation, we have to search into our system for
the `pgAdmin`.

**Notice:** During installation it will be necessary to give some credentials like username and password. This is good
to keep in mind as we are going to need them later in the process.

### Simple as 1,2,3

Now we have access to the admin page of our management system we can see on the right side all the servers we currently
have on our computer.Expanding the server list we see the following:

**1. Activating/Creating the server**

<p align=center>
    <img src="D:\GitHub\Data-Analysis\WeatherApp\images\servers.PNG"/>
</p>

**Notice:** This probably is going to be different for each user. I have installed two versions of the PostgreSQL and
one custom server. We can create any amount of servers with custom configurations. I choose to activate the PostgreSQL
13 server.

**2. Creating the Database**

<p align=center>
    <img src="D:\GitHub\Data-Analysis\WeatherApp\images\db_create.PNG"/>
</p>

Under the databases we can see all the existing databases we have on this particular server. With righ click we can
create and configure a new one. For this project I created a new one with name `weather-app`

**3. Creating the table**

<p align=center>
    <img src="D:\GitHub\Data-Analysis\WeatherApp\images\schemas.PNG"/>
</p>

Final step is to create a new table tha will hold all the data for our app. A table is an object that belongs to the
database, so as all the objects we find tables under `Schemas` which is a collection of database objects. Now here is
the tricky part we can create a new table either by right click and manually typing every parameters susch as column
names and types or running SQL commands which give us more control.

#### The code

```SQL
CREATE TABLE IF NOT EXISTS data (
    id SERIAL PRIMARY KEY,
    city_name VARCHAR(255) NOT NULL,
    wind_speed FLOAT NOT NULL,
    clouds FLOAT NOT NULL,
    temperature FLOAT NOT NULL,
    pressure FLOAT NOT NULL,
    humidity FLOAT NOT NULL,
    temp_min FLOAT NOT NULL,
    temp_max FLOAT NOT NULL,
    description VARCHAR(255) NOT NULL,
    registered_on TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

With right click on tables we choose the Query Tool. This will open for us a text editor where we can write and execute
SQL queries. Pasting the code above will result into creating a table with name data and 11 columns of different
attributes.

For more explanation on the code look the documentation of postgresql.

The names of the columns are determined by what we need to extract though the API call.

**Final Step**
Now we have a database running on our local server and a table to hold all the data. This step will show us how to find
some information about the server that we will need to connect to.

Right-click on the server and click on properties will prompt the following window.

Navigate to connection and take a look of the Host name, Port that the server is running and username

<p align=center>
    <img src="D:\GitHub\Data-Analysis\WeatherApp\images\connection.PNG"/>
</p>

## Putting all together

Time to get our hands dirty and write some code. We will create two python scripts. One will make the request and will
retrieve the data and the other will connect to the database and will insert the data into our table. Also we create a
config file that will hold the following configurations:

```python
api_key = ""
DB_NAME = ""
DB_HOST = ""
DB_PORT = ""
DB_USER = ""
DB_PASSWORD = ""
````

all the above parameters are private and is good practice not to share. Also don't commit the changes for this file and
keep it to your ignore list.

After having my files ready I create a final python script that will use the functionality of the previous files and
will put all together. Executing this script will generate an output confirming the connection to the database. To see
the results we go back to our admin pages and view the entries of our table. Again to view the data is possible either
through some clicks or running SQL commands.

Below are the results. The table has successfully been populated with the data from the API call

<p align=center>
    <img src="D:\GitHub\Data-Analysis\WeatherApp\images\results.PNG"/>
</p>

## Conclusion and final thoughts

This simple app shows the functionality of a data pipeline. From a simple request to a successful connection to a
Database and a transfer of data. This application lucks thought from automation. To get results we have manually to
execute the script each time, this is time-consuming and slows the process if we want to collect data for a longer
period. So an extension for this app could be the automation of all the tasks, so it will be independent of any user
input.
