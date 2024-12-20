from random import choice, randint
from pushtodoc import push_to_doc, update_id

from discord import Intents, Client, Message

def get_response(user_input: str):
    

    if user_input == "c.update":
        return "Checking for confessionals..."
    
    if user_input == "hello bot!":
        return "Hello there!"
    
    if user_input == "t8mqy7zl6gywwqg2lcmd2v266sva24zw":
        response = push_to_doc()
        return response
    
    if user_input[0:11] == "c.changeDoc" and user_input[-1] == ")":
        id = user_input[12:-1]
        update_id(id)
        return "Changed Document ID"