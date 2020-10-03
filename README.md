# func-statcast
An [Azure Function](https://docs.microsoft.com/en-us/azure/azure-functions/) that runs daily, using [Baseball Savant](https://baseballsavant.mlb.com/statcast_search) to fill a MySQL database with Statcast data.

In production, this Azure Function updates the database used by [app-statcast](https://github.com/isaacrlee/app-statcast).

## Features
This project has two function.

`TimerTrigger1` is a function that queries yesterday's Statcast data from Baseball Savant and adds it to a MySQL database.

`HttpTrigger1` is a function that queries and adds Statcast data to a MySQL database but the start and end dates for the query are passed in parameters. This function allows users to recover days of data when TimerTrigger1 fails.

## Getting Started

## Setting up MySQL Database
Set up a MySQL database.

Set the MYSQL_STATCAST environment variable with the connection string of the MySQL database.

$ export MYSQL_STATCAST="mysql+pymysql://<user>:<password>@<host>[:<port>]/<dbname>"

### Installing Requirements and running the Azure Function locally
First, clone the repository.
```
$ git clone https://github.com/isaacrlee/func-statcast.git
```

Follow the Azure Functions [docs](https://docs.microsoft.com/en-us/azure/azure-functions/functions-develop-vs-code?tabs=csharp) to setup Visual Studio Code to run Azure Functions locally.

## Update requirements.txt
When you add dependencies with poetry, you have to make sure to update the requirements.txt file because that it used by Azure to install dependencies before deploying the API to production.
```
$ poetry export -f requirements.txt > requirements.txt
```