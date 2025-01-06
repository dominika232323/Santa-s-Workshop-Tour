# Santa's Workshop Tour

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

## Competition description

Kaggle 2019 competition: [Santa's Workshop Tour](https://www.kaggle.com/c/santa-workshop-tour-2019)

Santa has exciting news! For 100 days before Christmas, he opened up tours to his workshop. Because demand was so strong, and because Santa wanted to make things as fair as possible, he let each of the 5,000 families that will visit the workshop choose a list of dates they'd like to attend the workshop.

Now that all the families have sent Santa their preferences, he's realized it's impossible for everyone to get their top picks, so he's decided to provide extra perks for families that don't get their preferences. In addition, Santa's accounting department has told him that, depending on how families are scheduled, there may be some unexpected and hefty costs incurred.

Santa needs the help of the Kaggle community to optimize which day each family is assigned to attend the workshop in order to minimize any extra expenses that would cut into next years toy budget! Can you help Santa out?

## Available Commands

- `make create_environment` - sets up Python interpreter environment
- `make requirements` - installs Python dependencies
- `make freeze` - overwrites requirements.txt with your installed Python dependencies
- `make clean` - deletes all compiled Python files
- `make lint` - lints using flake8 and black
- `make format` - formats source code with black
- `make tests` - runs tests from *santas_workshop_tour/tests/*
- `make santas` - runs *santas_workshop_tour/main.py* script

## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
│
├── data               <- Dataset with families choices from competition page on Kaggle
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         santas_workshop_tour and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── results            <- Results of running the algorithm
│   └── examples       <- Example result from competition page on Kaggle
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── santas_workshop_tour   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes santas_workshop_tour a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

## Authors

- Dominika Boguszewska
- Aleksander Szymczyk

