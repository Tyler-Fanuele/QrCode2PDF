# uvicorn main:app --host 10.0.0.147 --port 8001

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import mysql.connector


app = FastAPI()

cnx = None


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    itemId, itemName = getItemDetails(item_id)

    return {"itemId": item_id}

@app.get("/items/{item_id}/details", response_class=HTMLResponse)
async def read_item_details(item_id: int):
    itemId, itemName = getItemDetails(item_id)

    return f"""
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Item Id: {itemId}</h1>
            <h2>Item Name: {itemName}</h2>
        </body>
    </html>
    """
    
@app.on_event("shutdown")
def shutdown_event():
    global cnx
    cnx.close()
    print("Database connection closed.")

@app.on_event("startup")
def startup_event():
    print("Starting up...")
    # Initialize database connection
    global cnx
    cnx = mysql.connector.connect(user='root', password=input("Enter password: "),
                                host='127.0.0.1',
                                database='StorageSystem')

    print(cnx) 

def getItemDetails(item_id):
    global cnx
    cursor = cnx.cursor()
    query = f"SELECT * FROM items WHERE itemId = {item_id};"

    itemId = None
    itemName = None
    print("Executing query:", query)
    cursor.execute(query)

    result = cursor.fetchone()
    if result:
        print("Result found")
        itemId = result[0]
        itemName = result[1]
    else:
        print("No result found")

    cursor.close()

    return itemId, itemName