import streamlit as st
import requests
from flask import Flask, redirect, request, render_template, session, jsonify 
import pandas as pd
import logging


app = Flask(__name__)

@app.route("/")
def home():
    return render_template('')

def getall():
    url = "https://webapi.bps.go.id/v1/api/domain/type/all/key/04672fed2c8645d7564d60891ddc98c4/"  

    try:
        response = requests.get(url)
        response.raise_for_status()  

        data = response.json()  # Mengurai respons JSON
        return data
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        return None

# Contoh penggunaan
getallData = getall()
if getallData:
    print(getallData)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run()