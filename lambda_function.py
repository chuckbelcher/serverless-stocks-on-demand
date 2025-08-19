import yaml
import json
import requests
import time
import csv
import boto3
from io import StringIO

# S3_BUCKET = "my-lambda-stock-prices"  # replace with your bucket name
S3_BUCKET = "my-lambda-stock-prices"
S3_KEY = "stocks.csv"  # path in S3


def lambda_handler(event, context):
    # Load symbols from YAML
    with open("symbols.yaml", "r") as f:
        data = yaml.safe_load(f)
        symbols = data.get("symbols") if isinstance(data, dict) else data

    results = []
    headers = {"User-Agent": "Mozilla/5.0"}

    for symbol in symbols:
        price = None
        for attempt in range(3):
            try:
                url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
                r = requests.get(url, headers=headers, timeout=5)
                r.raise_for_status()
                data = r.json()
                price = data['chart']['result'][0]['meta']['regularMarketPrice']
                break
            except Exception as e:
                if attempt < 2:
                    time.sleep(1)
                else:
                    results.append({"symbol": symbol, "error": str(e)})

        if price is not None:
            results.append({"symbol": symbol, "price": price})

    # Convert results to CSV
    csv_buffer = StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=["symbol", "price", "error"])
    writer.writeheader()
    for row in results:
        writer.writerow({
            "symbol": row.get("symbol", ""),
            "price": row.get("price", ""),
            "error": row.get("error", "")
        })

    # Upload CSV to S3
    s3 = boto3.client("s3")
    s3.put_object(Bucket=S3_BUCKET, Key=S3_KEY, Body=csv_buffer.getvalue())
    # s3.put_object(Bucket=S3_BUCKET, Key="test.txt", Body="hello world")

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(results)
    }
