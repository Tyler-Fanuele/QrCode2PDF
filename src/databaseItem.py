from src.itemDetails import ItemDetails

from fastapi import Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="./templates")

class DatabaseItem:
    def __init__(self, data, cnx):
        cursor = cnx.cursor()
        cursor.execute("DESCRIBE " + "items")
        result = cursor.fetchall()
        cursor.close()
        self.itemTableSchema = result

        if "itemId" in data:
            self.itemDetails = self.__getItemDetailsFromItemId(data["itemId"], cnx)
        else:
            self.itemDetails = self.__getItemDetails()
        
    def __getItemDetails(self):
        return ItemDetails(self.itemTableSchema)

    def __getItemDetailsFromItemId(self, item_id, cnx):
        cursor = cnx.cursor()
        query = f"SELECT * FROM items WHERE itemId = {item_id};"

        itemDetails = ItemDetails(self.itemTableSchema)
        print("Executing query:", query)
        cursor.execute(query)

        result = cursor.fetchone()
        if result:
            print("Result found")
            try:
                itemDetails.updateFromDatabaseResults(result)
            except ValueError as e:
                print(f"Error updating item details: {e}")
            print("Item details updated successfully")
        else:
            print("No result found")

        cursor.close()

        return itemDetails

    def getJsonDetails(self):
        return self.itemDetails.json()

    def getHtmlPage(self, request: Request):
        details = {"request": request}
        details.update(self.itemDetails.json())
        return templates.TemplateResponse("item_details.html", details)