# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Dict, Text, List 
import json 
import random
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# open json file 
cocktails = open('cocktail.json')

# returns json object as dictionary
cocktails_dict = json.load(cocktails)

# help method to iterate through dictionary and find cocktail recipe
def lookup_cocktail_recipe(cocktail_name: str, recipes: dict) -> dict:
            if cocktail_name in recipes:
                return recipes[cocktail_name]
            else:
                return {}


# help method to turn cocktail dictionary from json into list
def get_all_cocktails():
    return [(key, value) for key, value in cocktails_dict.items()]

# returns the name of the user 
class action_username(Action):

    def name(self) -> Text:
        return "action_get_name"

    def run(self, dispatcher, tracker, domain):
        username = tracker.get_slot("username")
    
        return []

# finds the cocktail recipe
class action_store_cocktailname(Action):
   
    def name(self) -> Text:
        return "action_get_cocktail_recipe"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        cocktail = tracker.get_slot("cocktail")

        # Look up the cocktail recipe from the json file 
        recipe = lookup_cocktail_recipe(cocktail, cocktails_dict)

       # response
        dispatcher.utter_message(recipe)

        return []

# filter cocktail if alcoholic or not -> action_store_alcohol
class action_store_alcohol(Action):
    def name(self) -> Text:
        return "action_store_alcohol"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        filter = tracker.get_slot("filter")
        cocktails = get_all_cocktails()

        # Filter the cocktails based on the user's preference
        if filter == "Alcoholic":
            filtered_cocktails = [c for c in cocktails if c["strAlcoholic"]]
        elif filter == "Non alcoholic":
            # is_alcoholic        
            filtered_cocktails = [c for c in cocktails if not c["strAlcoholic"]]
        else:
            filtered_cocktails = cocktails

        dispatcher.utter_message(filtered_cocktails)

        return []

# random cocktail option
class action_random_recipe(Action):

    def name(self) -> str:
        return "action_random_recipe"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:
     
        entry = random.choice(list(cocktails_dict.items()))

        # TODO: entry[0] or just entry?? 
        response = f"Hier ein guter Cocktail für dich: {entry}!"
        dispatcher.utter_message(response)

        return []

# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

# To run install Flask & flask-cors with:
# "pip install Flask, flask-cors"

from sys import displayhook
from typing import Any, Text, Dict, List
from pyparsing import nestedExpr

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import json

class ActionGetRecipy(Action):
    
    def name(self):
        return "action_get_recipe"

    def run(self, dispatcher, tracker, domain):
        name = "Alabama Slammer"        
        url = "https:\/\/www.thecocktaildb.com\/images\/media\/drink\/jntghf1606771886.jpg"
        ingredient1 = "Southern Comfort"
        ingredient2 = "Amaretto"
        ingredient3 = "Sloe gin"
        ingredient4 = "Lemon juice"
        inst = "Alle Zutaten (au\u00dfer Zitronensaft) in einem Highball-Glas \u00fcber Eis gie\u00dfen. Umr\u00fchren, einen Schuss Zitronensaft hinzuf\u00fcgen und servieren."
        sepIngredients = ","
        sepInfo=";"
        ingredients = [ingredient1, ingredient2, ingredient3, ingredient4]
        infoArray = [name, url, sepIngredients.join(ingredients), inst]
        message = sepInfo.join(infoArray) + " | "
        print(message)
        dispatcher.utter_message("-rec: " + message + message + message)

        return[]
