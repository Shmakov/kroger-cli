Kroger CLI
==========

![Display Purchases Summary](images/Purchases-Summary.gif)

I got tired of manually applying the digital coupons while grocery shopping and decided to automate the process. While doing so I've added extra features, currently this python's cli can:

* Display basic information from your account (name, address, rewards card number, etc)
* [Complete the Kroger’s Survey on your behalf](images/Kroger-Survey.gif) (to earn 50 points and enter the sweepstake)
* [Clip Digital Coupons](#clip-digital-coupons) (first 150 coupons only, sorted by relevance)
* [Display Purchases Summary](#purchases-summary) (number of store visits and dollars spent)
* [Retrieve Points Balance](#fuel-points-balance)

The script works on kroger.com and other Kroger-owned grocery stores (Ralphs, Fry's, Fred Meyer, Dillons, Food 4 Less, [etc](https://en.wikipedia.org/wiki/Kroger#Chains)).

Install/Download
----------------

### Windows

You can download the latest version from the GitHub's [releases tab](https://github.com/Shmakov/kroger-cli/releases).

### Linux

* Clone the repository: `git clone git@github.com:Shmakov/kroger-cli.git && cd ./kroger-cli`
* Creating virtual environment: `python3.8 -m venv ./venv` (you might need to install `sudo apt-get install python3.8-venv`)
* And activate it: `source venv/bin/activate`
* Install the requirements: `pip install -r requirements.txt`
* And you should be able to launch the project: `python -m kroger_cli`

CLI Commands
------------

The application support non-interactive mode by passing a name of a command. An example on how to complete Kroger's Survey: `kroger-cli survey`.

Please use `kroger-cli --help` to see list of all available commands. Alternatively you can run the application without any command to launch the interactive mode (you can see the screenshot of it below).

Screenshots
-----------

### Main Interface

![Kroger CLI Screenshot](images/Home-Screen-Screenshot.png)

### Clip Digital Coupons

![Clip all Kroger's Digital Coupons](images/Clip-Digital-Coupons.png)

### Purchases Summary

![Display Purchases Summary](images/Purchases-Summary.gif)

### Fuel Points Balance

![Fuel Points Balance](images/Fuel-Points-Balance.png)

### Complete Kroger's Feedback Form

[Watch](images/Kroger-Survey.gif)

Side Notes
----------

The initial plan was to use plain HTTP (and `requests` package), however I couldn't sign in to the Kroger's website using it. Possibly had to do with csrf token validation and/or JavaScript-based protection. Because of that I had to use `pyppeteer`, which is a python's port of `Puppeteer` (Headless Chrome).

### TODO

* Purchased items (receipt data) Excel export, which could be useful for budgeting/categorization/filtering
* Notification on when certain items go on sale