## Step 1: Create the API Gateway

1. Go to API Gateway in the AWS console.

2. Choose Create API → HTTP API (lighter weight, good for Lambda triggers).

3. Give it a name like StockPricesAPI.

4. Under Integrations, choose Lambda → select your stock Lambda function.

4. Click Next, leave defaults for routes/stages, and create the API.

## Step 2: Add a Route

In the new API, go to Routes.

1. Create a route like:

2. Method: GET
 - Path: /stocks

3. Attach the route to your Lambda integration.

## Step 3: Deploy the API

- API Gateway will create a default stage (usually called $default).

- Copy the Invoke URL from the stage (it looks like https://xxxxxx.execute-api.us-east-1.amazonaws.com).

## Test

curl https://xxxxxx.execute-api.us-east-1.amazonaws.com/stocks
