# ERCOT_windfarm

### Description
I worked on this project back in early 2016. The premise is that there is a wind farm in Texas trying to sell 
energy into the regional wholesale market (ERCOT, see https://en.wikipedia.org/wiki/Electric_Reliability_Council_of_Texas).
The owner of the wind farm tries to forecast the wind farm's 
energy production, however the actual production deviates due to forecasting errors. The objective for the project
is to find an ideal battery size (or what combination of batteries) that a battery manufacturer could sell to the wind farm owner to help improve their
interaction with the wholesale market.

### Project Organization
I approached the problem from two different angles. I first took a 'statistical' approach by trying to size the battery 
in a way that would cover the majority of daily deviations. Second, I approached the problem by looking at wholesale market
prices available from ERCOT to combine ancillary services - then simulate battery operation for a year for a variety of battery sizes.
* The 'part_1_stats' folder contains the python scipts, original data, and images generated for the 'statistical' approach
* The 'part_2_market' folder contains the python scripts, data, and images generated for the 'pricing' approach
* The 'final' folder contains the final write-up for both approaches in PDF format and a summary powerpoint<br>

The PDFs are viewable in GitHub. 

### Requirements

* Code is in Python 2.7.10
* Pandas >= 0.19.1
* Numpy >= 1.8.0rc1
* Seaborn >= 0.8.1
