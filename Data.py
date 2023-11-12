import requests
from datetime import datetime
import json
import os

MONTH = datetime.now().strftime("%m")


class Data:
    # Gestiona los datos de la hoja de cálculo en la que se alojan.

    def __init__(self):
        # selecciona la url del mes en curso
        self.token = os.environ.get("BEARER_SHEETDB")
        self.header_sheety = {"Authorization": f"Bearer {self.token}"}
        # print(self.header_sheety)
        self.endpoint = f"https://sheetdb.io/api/v1/ykev452pamc3m"
        self.response = requests.get(url=self.endpoint,
                                     headers=self.header_sheety)  # obtiene los datos de la hoja de este mes.
        # print(self.response.text)
        self.data = json.loads(self.response.text)
        self.now = datetime.now().strftime("%d/%m/%y")
        self.gasto_qq = 0
        self.gasto_esti = 0

    def write(self, gasto, pagador, sheet):
        self.dataToWrite = [{
            "Fecha": self.now,
            "Gasto": gasto,
            "Quien paga": pagador,
        }
        ]
        self.sheet = {"sheet": sheet}
        self.response = requests.post(url=self.endpoint, headers=self.header_sheety, json=self.dataToWrite,
                                      params=self.sheet)
        print(self.response.text)
        if self.response.status_code == 201:
            print("Gasto añadido")
        else:
            print("algo ha fallado, mira a ver qué pasa.")

    def get_data(self):
        self.response = requests.get(url=self.endpoint,
                                     headers=self.header_sheety)
        self.data = json.loads(self.response.text)
        # print(self.data)
        self.gasto_qq = 0
        self.gasto_esti = 0
        for i in self.data:
            if i['Quien paga'] == 'Quique':
                self.gasto_qq += float(i['Gasto'].replace(",", "."))
            elif i['Quien paga'] == 'Estibaliz':
                self.gasto_esti += float(i['Gasto'].replace(",", "."))
        # print(f'Gasto Esti: {self.gasto_esti}\nGasto Quique: {self.gasto_qq}')

    def hacer_cuentas(self):
        self.get_data()
        self.gasto_total = self.gasto_qq + self.gasto_esti
        self.mitad = self.gasto_total / 2
        print(f'Gasto Esti: {self.gasto_esti}\nGasto Quique: {self.gasto_qq}')
        if self.gasto_qq < self.mitad:
            print(f"Quique debe {self.mitad - self.gasto_qq}€ a Esti")
        elif self.gasto_qq == self.mitad:
            print(f"Está todo apañado")
        else:
            print(f"Esti debe {self.mitad - self.gasto_esti}€ a Quique")

    def apañar_cuentas(self):
        self.hacer_cuentas()
        if self.gasto_qq < self.mitad:
            self.quiqueApana = [
                {"Fecha": self.now,
                 "Gasto": f"{self.mitad - self.gasto_qq}",
                 "Concepto": "apañar cuentas",
                 "Quien paga": "Quique"
                 }

            ]
            self.estiresta = [
                {"Fecha": self.now,
                 "Gasto": f"{-((self.mitad - self.gasto_qq))}",
                 "Concepto": "apañar cuentas",
                 "Quien paga": "Esti"
                 }

            ]
            self.response = requests.post(url=self.endpoint, headers=self.header_sheety, json=self.quiqueApana)
            self.response = requests.post(url=self.endpoint, headers=self.header_sheety, json=self.estiresta)
        elif self.gasto_esti < self.mitad:
            self.estiApana = [
                {"Fecha": self.now,
                 "Gasto": f"{(self.mitad - self.gasto_esti)}",
                 "Concepto": "apañar cuentas",
                 "Quien paga": "Esti"
                 }

            ]
            self.quiqueresta = [
                {"Fecha": self.now,
                 "Gasto": f"{-((self.mitad - self.gasto_esti))}",
                 "Concepto": "apañar cuentas",
                 "Quien paga": "Quique"
                 }

            ]
            self.response = requests.post(url=self.endpoint, headers=self.header_sheety, json=self.estiApana)
            self.response = requests.post(url=self.endpoint, headers=self.header_sheety, json=self.quiqueresta)
