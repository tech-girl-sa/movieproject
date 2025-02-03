# My Awesome Movie App

This project is your mini library of movies. You can add, update, delete or list your favorite movies,
allowing automatically storage of year and rating of the film as well. you can check statistics about 
your stored films search or filter them and even generate histograms based on the ratings. 
If you don't know what to watch tonight just use the random film option. Great isn't it !! but that's not all: 
You can even generate your own website based on your favorite Films. Enjoy!! 

## Installation

To install this project, simply clone the repository and install the dependencies in requirements.txt using `pip`
You need to add env file and specify  OMDbAPI_KEY variable using your api key from The OMDb API following 
 [This Link](https://www.omdbapi.com/apikey.aspx)

## Usage

To use this project, run the following command - `python main.py` if you want to use your own storage file instead
of the default one you can add the file name as argument in your command like: `python main.py my_custom_file.json` 
or  `python main.py my_custom_file.csv` we support two ways of storage using csv or json files. if you choose your file
name without any extension your file will be by default a json file.
