# uvicorn main:app --host 10.0.0.147 --port 8001

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fastapi import Request
from fastapi.staticfiles import StaticFiles

from src.itemDetails import ItemDetails
from src.databaseItem import DatabaseItem

import mysql.connector
from mysql.connector import errorcode

import os
import signal



# Init App
app = FastAPI()

# Mount the static directory
app.mount("/static", StaticFiles(directory="./static"), name="static")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    global cnx
    databaseItem = DatabaseItem({"itemId": item_id}, cnx)
    return databaseItem.getJsonDetails(item_id)

@app.get("/items/{item_id}/details", response_class=HTMLResponse)
async def read_item_details(request: Request, item_id: int):
    global cnx
    databaseItem = DatabaseItem({"itemId": item_id}, cnx)
    return databaseItem.getHtmlPage(request)
    
@app.on_event("shutdown")
async def shutdown_event():
    global cnx
    if cnx is not None:
        cnx.close()
        print("Database connection closed.")
    else:
        print("No database connection to close.")

@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    # Initialize database connection
    try:
        global cnx
        cnx = mysql.connector.connect(user='root', password=input("Enter password: "),
                                    host='127.0.0.1',
                                    database='StorageSystem')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        os.kill(os.getpid(), signal.SIGTERM)
    else:
        print(cnx) 




