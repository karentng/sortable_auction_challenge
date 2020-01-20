# Auction Coding Challenge

Inside of the auction folder are all files part of the implemented solution.
main.py file contains the main function to run the prototype.
    
    - Load config file
    - get input file
    - call the process function to run the input auctions
    - prints the output in json format indented
    
models.py includes two classes implemented to model the input data and configs:

    - Bid: model class with all attributes that belong to it (bidder, bid, unit)
    - Site: model a site and all its attributes (name, bidders, floor)

run_auctions.py contains all methods to validate, get the winners and process auctions' results. 
All functions are commented with docstring and single line comments.

There is a log option in case of desired following up the process. This is located in the main.py file
line 14.

# Running Auctions

The program works with Docker as required. Therefore you will be able to run it as following:

```bash
$ docker build -t challenge .
$ docker run -i -v /path/to/challenge/config.json:/auction/config.json challenge < /path/to/challenge/input.json
```
