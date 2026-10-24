# Udemy Course Scraper

This is a python package that scrapes Udemy for your purchases and owned courses.

## Installation

Install it with your package manager of choice such as:

```shell
uv init
uv add git+https://github.com/GreenBeanio/Udemy_Purchase_Scraper
```

Download the default `.env` file:

```shell
curl -L -o .env https://raw.githubusercontent.com/GreenBeanio/Udemy_Purchase_Scraper/refs/heads/master/dot.env
```

## Usage

1. Modify the `.env` file if you don't want to use defaults.

2. Run the script:

```python
uv run python -m udemy_purchase_scraper
```

There are the following command line arguments you can run:

`-e` or `--env`: the file name of your `.env` file (Default: `.env`)
`-ll` or `--log-level`: Logging Level: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. (Default: `INFO`)
`-lf` or `--log-file`: Path for the log file (Default: `Udemy.log`)
`-h` or `--help`: Help message

## Output

The main output is an Excel file with 2 tabs:

- Purchase: Has your Purchase information
- Course: Has your course information

## Notes

Some courses will not have an associated purchase. For some reason some free courses have corresponding purchases and some don't.

I have never had a Udemy subscription so I have no idea if those courses count as owned courses in your menu. If they do
they should show up in the Course sheet.

I currently do not have it checking the archived page since I don't have any courses in there. If there is actually any other souls
that ever use this script I will add that feature.
