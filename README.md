# Door Dash Orderer

A small selenium script that automates door dash orders

## Installation

Simply download and extract this folder somewhere on your device. Make sure Python 3 is installed and accessible as `python3` on the PATH.

## Usage

Orders are defined in the `order.json` file in the same directory as the `order.py` file. `order.json` is an array of order objects which have the following format:

```
{
    "site": "<url of doordash store>",
    "address": "<address to deliver to>",
    "items": [
      {
        "name": "<name of item>",
        "options": { "<option name>": "<option choice>" },
        "quantity": <number>
      },
      ...repeated for as many items as needed
    ]
}]
```

For example, this is an order.json that orders several bagels and some cream cheeses from Breuggers
```
[{
    "site": "https://www.doordash.com/store/bruegger's-bagels-durham-250810",
    "address": "123 Pavement St, Durham, NC 27701",
    "items": [
      {
        "name": "Baker's Dozen",
        "options": { "Sliced Choice": "Sliced" },
        "quantity": 4
      },
      {
        "name": "Cream Cheese Tubs",
        "options": { "Cream Cheese Choice": "Plain" },
        "quantity": 1
      },
      {
        "name": "Cream Cheese Tubs",
        "options": { "Cream Cheese Choice": "Onion & Chive" },
        "quantity": 1
      },
      {
        "name": "Cream Cheese Tubs",
        "options": { "Cream Cheese Choice": "Strawberry" },
        "quantity": 1
      }
    ]
}]
```

Once the order.json file is in place you can run the script with `bash run.command`.

On your first run you will not be logged into DoorDash because this runs under a special profile. The app will open up a dialog prompting you to log in. Once you are logged in press the OK button to continue the script. Assuming you ask DoorDash to remember you, this will not be necessary on every run.