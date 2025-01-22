from celery import Celery
import yfinance as yf
from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")

celery_worker = Celery(
    "celery_worker",
    broker="redis://redis:6379/0",  # broker for tasks
    backend="redis://redis:6379/0"  # backend for results
)

# Functions
def add(numbers):
    print(f"Adding numbers: {numbers}")
    return sum(numbers)

def enrich_stock(ticker):
    # get info from yahoo first
    stock = yf.Ticker(ticker)
    info = stock.info
    yahoo_data = {
        "symbol": info.get("symbol"),
        "name": info.get("shortName"),
        "currency": info.get("currency"),
    }
    
    # then the openAI stuff
    client = OpenAI(api_key=OPENAI_TOKEN)
    keys = ['founding_year', 'country', 'founder', 'current_ceo', 'market_cap', 'url_website', 'description', 'industry']
    prompt = f"create a json dict with the following information {keys}, for this stock ticker: {ticker}"
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a wall street analyst"},
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    openai_data = json.loads(completion.choices[0].message.content)
    return {**yahoo_data, **openai_data}

    
    
# The main processor
PROCESS_MAP = {
    "add": add,
    "enrich_stock": enrich_stock
}

@celery_worker.task(name="handle_task")
def handle_task(task_data):
    process_name = task_data.get("process_name")
    data = task_data.get("data")

    if process_name not in PROCESS_MAP:
        raise ValueError(f"Unknown process_name: {process_name}")

    # Call the appropriate function and return the result
    return PROCESS_MAP[process_name](data)


