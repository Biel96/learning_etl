# Importando biblioteca para requisitar API
import requests

# Importando esse breguete pra conversar com o Postgres (+ uma caralhada de DBs)
import sqlalchemy as db
from sqlalchemy import create_engine, URL, text
from sqlalchemy import *
import pymysql

api_url = 'https://restcountries.com/v3.1/all'
response = requests.get(api_url)

# Cláusula de verificação da conexão com API
# if response.status_code == 200:
data = response.json()

# URL.create - string de conexão apenas
url_object = URL.create(
    'postgresql',
    username='postgres',
    password='Lecotchezin2023',
    host='localhost',
    database='postgres',
)

engine = create_engine(url_object)

connection = engine.connect()

# Arthur ####################
def check_apostrophe(s):
    if("'" in s):
        s = s.replace("'", "\\'")
        return f"E'{s}'"
    return f"'{s}'"
#############################

# Query para limpar os dados na tabela
connection.execute(text('Truncate table tb_countries'))

for country in data:
    # Gabriel
    continente = country['region']
    
    try:
        pais = country['subregion']
        
        # Resolvendo problema
        if "'" in country['capital'][0]: 
            capital = "E'" + country['capital'][0].replace("'","\\'") + "'"
        else:
            capital = "'" + country['capital'][0] + "'"
    
    except KeyError:
        pais = 'N/A' 
        capital = "'N/A'"
        
    bandeira = country['flags']['png']
    populacao = country['population']
    statement = text(f"INSERT INTO tb_countries(continente, pais, capital, bandeira, populacao) VALUES('{continente}','{pais}',{capital},'{bandeira}',{populacao})")
    
    # Arthur    
    """ continente = country.get('region', 'n/a')
    pais = country.get('subregion', 'n/a')
    populacao = country.get('population', 'n/a')
    bandeira = country.get("flags", {}).get("png", "n/a")
    capital = country.get('capital', ["n/a"])[0] if 'capital' in country else "n/a"

    columns = [continente, pais, capital, bandeira, populacao]

    row = ",".join([ check_apostrophe(valor) if type(valor) == str else str(valor) for valor in columns ])
    statement = text(f"INSERT INTO tb_countries(continente, pais, capital, bandeira, populacao) VALUES({row})") """
            
    connection.execute(statement)


connection.commit()
connection.close()