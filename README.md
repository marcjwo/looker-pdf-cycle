# 🚲 Looker PDF Cycle 🚲

👋🏼 Welcome to the Looker PDF Cycle! <br> Ever wanted to generate a multi-page PDF that cycles through the different filter values? Look no further!

## Introductions

The guide facilitates the ecommerce dataset of the looker-private-demo dataset available in BigQuery. This guide will demonstrate a way to solve a commonly received request of generate multi-page PDF reports that are build by cycling through the filters available on a dashboard; to achieve this, Lookers API Version 4.0 is facilitated.

## Requirements

It requires a few things for this too work.

### Looker instance requirements

- Create a dashboard that contains the view that you want to output as PDF
- The dashboard needs to have a filter thats being applied --> this is whats being cycled through

### Development environment requirements (facilitate requirements.txt)

- Looker SDK >= 22.10.0
- Python3 (tested with Python 3.10.4)
- PyPDF2 >= 2.7.0

## How-to
### Create the dashboard you want to 🚲 through
Create the dashboard you will be using, give it the filter you want to cycle through and maybe test out how it looks like when you generate it as a PDF - done! Suggestion for testing: Orders per month with a filter to select between the different shipping statusses.

### Create a configuration file
To facilitate the Looker API, we need to tell the script we are about to create how to authenticate into our instance. The preferred way of doing this is creating an `.ini` file containing all the relevant information.

```
[Looker]
base_url=YOUR_INSTANCE_URL
client_id=YOUR_CLIENT_ID
client_secret=YOUR_CLIENT_SECRET


[LookML]
model = MODEL_TO_BE_USED
view = EXPLORE_TO_BE_USED
field = FIELD_TO_BE_USED (in the format: view_name.field_name) # status in our case
dashboard_id="DASHBOARD_ID_FROM_URL"
dashboard_filters="filter part of the url"

[OutputSettings]
result_format=pdf
width=1000
height=1000
pdf_paper_size="a4"
```
The first section [Looker] contains the relevant instance information; in the [LookML] you can define additional parameters for the python script- this is helpful as you only have to edit the ini file without bothering to change lines of the code. Finally, the [OutputSettings] section lets you define a few options for the API leveraged. These are just examples of course and can be adjusted accordingly.

### Run the script!

