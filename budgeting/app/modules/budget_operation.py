from flask import jsonify
from datetime import datetime
from bson.objectid import ObjectId
import json

# Function to calculate the balance
def calculating_budget(collection, budget_id):
    response = collection.find_one({"_id": ObjectId(budget_id)})
    revenue, expenses = 0.0, 0.0
    
    for rev in response['revenue']: 
        revenue += float(response['revenue'][rev]['amount'])

    for exp in response['expenses']:
        expenses += float(response['expenses'][exp]['amount'])

    balance = round(revenue - expenses, 2)
    collection.update_one({"_id": ObjectId(budget_id)}, {"$set": {"balance": balance}})


# Function to handle budget_operation operations
def budget_operation(db, request, type_budget_operation):
    
    # Retrieve data from the request JSON
    data_db = request.json

    try:
        collection = db["budget"]
        operation = 'expenses' if type_budget_operation == 'expense' else 'revenue'
        # Handle getting budget
        response = collection.find_one({"_id": ObjectId(data_db['budget_id'])})
        
        # Handle inserting budget_operation
        if request.method == 'POST':

            response[operation].update({f"{str(datetime.now().timestamp()).replace(".","")}" : {
                "name" : data_db['name'],
                "budget_project_type" : data_db['budget_project_type'],
                "amount" : data_db['amount'],
                "budget_category_type" : data_db['budget_category_type'],
                "date" : data_db['date'],
                "creation_date" : datetime.now().strftime('%Y-%m-%d %H:%M')
                }
            })
            
            collection.update_one({"_id": ObjectId(data_db['budget_id'])}, {"$set": {f"{operation}": response[operation]}})
            #Recalculating the balance
            calculating_budget(collection, data_db['budget_id'])
            return {"budget_operation_insert" : True}
        
        
        # Handle budget_operation update
        elif request.method == 'PUT':
            response[operation].update({f"{data_db['operation_id']}" : {
                "name" : data_db['name'],
                "budget_project_type" : data_db['budget_project_type'],
                "amount" : data_db['amount'],
                "budget_category_type" : data_db['budget_category_type'],
                "date" : data_db['date']
                }
            })
            
            collection.update_one({"_id": ObjectId(data_db['budget_id'])}, {"$set": {f"{operation}": response[operation]}})
            #Recalculating the balance
            calculating_budget(collection, data_db['budget_id'])
            return {"budget_operation_update" : True}

        # Handle budget_operation deletion
        elif request.method == 'DELETE':
            #removing item
            del response[operation][data_db['operation_id']]
            collection.update_one({"_id": ObjectId(data_db['budget_id'])}, {"$set": {f"{operation}": response[operation]}})
            #Recalculating the balance
            calculating_budget(collection, data_db['budget_id'])
            return {"budget_operation_delete" : True}

        # Handle unknown methods
        else:
            return {"error" : f"budget_{request.method}_unsupported"}
    except Exception as e:
        print(e)
        return {"error" : "except_budget_module"}