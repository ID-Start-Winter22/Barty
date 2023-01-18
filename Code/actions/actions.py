# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
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

from sys import displayhook
from typing import Any, Text, Dict, List
from pyparsing import nestedExpr

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import json
import random

alcohol = ""
taste = ""
with open(".\data\cocktail.json", "r") as file:
    data = json.load(file)

class DisplatTaste(Action):
    
    def name(self):
        return 'action_display_taste'

    def run(self, dispatcher,tracker,domain: Dict[Text, Any]):
        options = [
            {"title": "Fruchtig", "payload": "fruchtig"},
            {"title": "Süß", "payload": "suess"},
            {"title": "Sauer", "payload": "sauer"},
            {"title": "Bitter", "payload": "bitter"},
            {"title": "Erfrischend", "payload": "erfrischend"},
            {"title": "Cremig", "payload": "cremig"}
        ]
        dispatcher.utter_message(text = "These are your option", buttons = options)
        
class HandleTaste(Action):
    
    def name(self):
        return 'action_handle_taste'
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]):
        taste = tracker.latest_message["text"]
        dispatcher.utter_message(text = taste)
        
class DisplatAlcohol(Action):
    
    def name(self):
        return 'action_display_alcohol'

    def run(self, dispatcher,tracker,domain: Dict[Text, Any]):
        options = [
            {"title": "Mit Alkohol", "payload": "Alcoholic"},
            {"title": "Ohne Alkohol", "payload": "Non alcoholic"},
        ]
        dispatcher.utter_message(text = "These are your option", buttons = options)
        
class HandleAlcohol(Action):
    
    def name(self):
        return 'action_handle_alcohol'
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]):
        alcohol = tracker.latest_message["text"]
        dispatcher.utter_message(text = alcohol)
        
class getCocktails(Action):
    
    def name(self):
        return 'action_get_cocktails'
    
    def run(self, dispatcher,tracker,domain: Dict[Text, Any]):
        results = getCocktails()
        alcohol = ""
        taste = ""
        dispatcher.utter_message(json_message = results)
        
        
def getCocktails():
    filteredCocktails = []
    for cocktail in data["drinks"]:
        cocktailDict = data["drinks"][cocktail]
        
        if cocktailDict["strAlcoholic"] == alcohol and cocktailDict["taste1"] == taste:

            filteredCocktails.append(compileCocktailData(cocktailDict))
            
    if len(filteredCocktails) < 3: return filteredCocktails
    return random.sample(filteredCocktails, 3)

def compileCocktailData(cocktail):
    ingridientsList = []
    
    for key in cocktailDict:
        if key.startswith('strIngredient') and cocktailDict[key] != 'null':
            ingridientsList.append(cocktail[key])
    
    if cocktailDict['strInstructionsDE'] == 'null': instruction = cocktailDict['strInstructions']
    else: instruction = cocktailDict['strInstructionsDE']
    
    return {'name': cocktail['strDrink'], "ingredients": ingridientsList, "url": cocktail['strDrinkThumb'], "instructions": instruction}