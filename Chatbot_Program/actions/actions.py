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
