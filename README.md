# QuickPunch
Get summaries of your daily Nigerian news in Deedax style!

![https://quick-punch.vercel.app/](images/quickpunch.png)

## Introduction
QuickPunch is a simple news aggreagator that uses the PunchNG to summarize Nigerian news. Subscribers can choose to receive daily summaries of the top headlines in Nigerian news based on their interests.

For the front-end, check [here](https://github.com/Daheer/QuickPunch_Front_End)

## Demo
Live hosted version of QuickPunch can be found [here](https://quick-punch.vercel.app/)

## How does it work?

QuickPunch 
 - Fetches live Nigerian news from [PunchNG's RSS Feed](https://rss.punchng.com/)
 - Scrapes the actual news articles from links provided by the RSS feed
 - Stores the news articles in a Supabase database
 - Uses a [BART model finetuned on CNN Daily Mail](https://huggingface.co/facebook/bart-large-cnn) to summarize the news articles
 - Uses a [News Topic Classification model](https://huggingface.co/kartashoffv/news_topic_classification) to categorize the news articles
 - Sends the summaries to subscribers via email

## Installation

```bash
# Clone the repo
git clone https://github.com/Daheer/QuickPunch.git

# Install dependencies  
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Project Structure

```bash
📦QuickPunch
├── Dockerfile
├── LICENSE
├── QuickPunch
│   ├── __init__.py
│   ├── components
│   │   ├── __init__.py
│   │   ├── categorization.py
│   │   ├── distribution.py
│   │   ├── init.py
│   │   ├── initialization.py
│   │   └── summarization.py
│   ├── config
│   │   ├── __init__.py
│   │   └── configuration.py
│   ├── constants
│   │   └── __init__.py
│   ├── entity
│   │   └── __init__.py
│   ├── logging
│   │   └── __init__.py
│   ├── pipeline
│   │   ├── __init__.py
│   │   └── daily_digest.py
│   └── utils
│       └── __init__.py
├── README.md
├── app.py
├── config
│   └── config.yaml
├── main.py
├── params.yaml
├── requirements.txt
├── research
│   └── trials.ipynb
├── setup.py
└── template.py
```

## Usage

#### Setting up the environment variables

```bash
touch .env
```

Add the following to the .env file

```
SUPABASE_URL: XXX  
SUPABASE_KEY: XXX
APP_PASSWORD: XXX # Google App Password
```

#### Running the daily digest

```bash
python QuickPunch/pipeline/daily_digest.py 
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please reach out to me @ suhayrid6@gmail.com, I'd be happy to walk you through the project, including the Supabase database configuration




