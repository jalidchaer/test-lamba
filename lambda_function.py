import json
import os
import pymysql
import time
import urllib.request 
from dotenv import load_dotenv


load_dotenv()

# Parámetros de la conexión a la base de datos
db_endpoint = os.getenv('DB_HOST')
db_user = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')


def lambda_handler(event, context):
    
    # Configuración de la API de CoinMarketCap
    api_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=BTC'
    headers = {'X-CMC_PRO_API_KEY': os.getenv('CMC_API_KEY')}
    # Extracción del precio de Bitcoin
    req = urllib.request.Request(api_url, headers=headers)
    response = urllib.request.urlopen(req)
    if response.status == 200:
        data = json.loads(response.read().decode('utf-8'))
        price = data['data']['BTC']['quote']['USD']['price']
        timestamp = time.time()
       # Conectar a la base de datos
   
        conn = pymysql.connect(
           host=db_endpoint, 
           user=db_user,
           password=db_password, 
           db=db_name,
           )

        with conn.cursor() as cursor:
           cursor.execute("INSERT INTO bitcoin_prices (timestamp, price) VALUES (NOW(), %s)", (price,))
           conn.commit()

        conn.close()

        return {
        'statusCode': 200,
        'body': json.dumps({'price': price})
       }
   
