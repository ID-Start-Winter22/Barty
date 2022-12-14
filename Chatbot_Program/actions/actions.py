# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Dict, Text, List 
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json 
import random

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
