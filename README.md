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
    "day": "<day string>",
    "time": "<time range>"
    "items": [
      {
        "name": "<name of item>",
        "options": { "<option name>": "<option choice>" },
        "quantity": <number>
      },
      ...repeated for as many items as needed
    ]
}
```

Day string and time range are based on Grub Hub's UI, which results in some odd choices. You can generally only order out about 4 days from the current day, and it uses abbreviations. For example, tomorrow is listed as `TMR`. Times also depend on the options and must include the full string, so one needs too use `8:30 - 8:50 AM` rather than just `8:30 AM`

For example, this is an `order.json` (see the example file in this directory as well) that orders several bagels and some cream cheeses from Breuggers tomorrow at `8:30 - 8:50 AM`
```
[{
    "site": "https://www.doordash.com/store/bruegger's-bagels-durham-250810",
    "address": "123 Pavement St, Durham, NC 27707",
    "day": "TMR",
    "time": "8:30 - 8:50 AM",
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

## Troubleshooting

### Pausing mid process

If the program pauses mid process it may be because a string is incorrect. Check for spelling, and if it is spelled correctly use the inspect tool in the browser to check for extra spaces after the end of an option name. Names must be exact matches

### Refusing to Start

The Chrome instance launched by this tool must be closed before a new instance of the script is run, or it will fail. If the script fails to start double check that the Selenium Chrome instance is closed

### Installation Failed

Selenium depends on a cryptography package that only functions with a newer version of pip. This should be auto installed by the run script, but may be a source of problems
