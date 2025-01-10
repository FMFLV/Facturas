from fastapi import FastAPI;
import urllib3
import requests
from pydantic import BaseModel
from datetime import datetime

app = FastAPI() 

@app.get("/")
def index():
    return {"message": "Hello World"}

@app.get("/Facturas/{Rut}")
def get_data(Rut : str):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    API_ENDPOINT = "https://23.88.83.123:50047/b1s/v1/Login"

    data = {
        'CompanyDB': 'ZZ_VINOTECA_11122024',
        'UserName': 'integradorDW',
        'Password': 'X.Lv3Ee.2B'
    }


    r = requests.post(url=API_ENDPOINT, json=data, verify=False)

    b1session_cookie = r.cookies.get('B1SESSION')
    b1session_ROUTEID = r.cookies.get('ROUTEID')

    r = requests.post(url=API_ENDPOINT, json=data, verify=False)

    b1session_cookie = r.cookies.get('B1SESSION')
    

    b1session_ROUTEID = r.cookies.get('ROUTEID')

    url = f"https://23.88.83.123:50047/b1s/v1/SQLQueries('Sql02')/List?rut='{Rut}'"
    headers = {
        "Cookie": "B1SESSION=" + b1session_cookie + "; ROUTEID=" + b1session_ROUTEID,
        "Content-Type": "application/json",
        "prefer": "odata.maxpagesize=10000"
    }
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    data = response.json()

    all_results = []
    while url:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        data = response.json()
        results = data.get("value", [])
        all_results.extend(results)
        url = data.get("@odata.nextLink")

    if not all_results:
        return {"message": "No records found."}
    processed_data = [
            {
                "numfactura": item.get("numfactura"),
                "fechadocto": item.get("fechadocto"),
                "fechavecto": item.get("fechavecto"),
                "mtobruto": item.get("mtobruto"),
                "saldo": item.get("mtobruto", 0) - item.get("PaidSum", 0),  # Cálculo de la diferencia
                "estado": item.get("estado"),
                "concepto": item.get("concepto"),
            
            }
            for item in results
        ]
    return processed_data
    #return response


