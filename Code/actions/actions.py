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
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType, ConversationResumed
from rasa_sdk.executor import CollectingDispatcher

import json
import random

with open(".\data\cocktail.json", "r") as file:
    rawData = json.load(file)
data = rawData["drinks"]

class StartSession(Action):
    
    def name(self):
        return "action_session_start"
    
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text = "👋 Hi, ich bin Berty der Barkeeper")
        dispatcher.utter_message(text = "Wer ist den die entzückende Person mit der ich rede")


class DisplatTaste(Action):
    
    def name(self):
        return 'action_display_taste'

    def run(self, dispatcher, tracker, domain: Dict[Text, Any]):
        messages = ['Nach was ist dir denn Heute?', 'In welche rechting solls gehen?', 'Was darf ich denn anbieten?']
        options = [
            {"title": "Fruchtig", "payload": 'taste fruchtig'},
            {"title": "Süß", "payload": 'taste suess'},
            {"title": "Sauer", "payload": 'taste sauer'},
            {"title": "Bitter", "payload": 'taste bitter'},
            {"title": "Erfrischend", "payload": 'taste erfrischend'},
            {"title": "Cremig", "payload": 'taste cremig'}
        ]
        dispatcher.utter_message(text = random.sample(messages, 1)[0], buttons = options)
        
class DisplatAlcohol(Action):
    
    def name(self):
        return 'action_display_alcohol'

    def run(self, dispatcher, tracker, domain: Dict[Text, Any]):
        reactions = {
            "suess": "Aha, also soll er genauso süß sein wie du.🍬",
            "fruchtig": "Uhhh Fruchtig.🍓 Mach dich auf eine Abenteuerreise durch einen tropischen Dschungel gefasst.",
            "sauer": "Süßes oder Saures? Nichts Süßes? Na dann bekommst du was Saures.🍋",
            "bitter": "Bitter🍫, das kriege ich hin.",
            "erfrischend": "Also was erfrischendes.💦 Brauchst du etwa Abkühlung von deinem hitzigen Leben",
            "cremig": "Mhmm, cremig.🥥 Da denke ich immer an Mama's Sahne Torte."
        }
        
        options = [
            {"title": "Mit Alkohol", "payload": '/alcohol_selected{"alcohol": "Alcoholic"}'},
            {"title": "Ohne Alkohol", "payload": '/alcohol_selected{"alcohol": "Non alcoholic"}'},
        ]
        dispatcher.utter_message(text = reactions[tracker.get_slot("taste")])
        dispatcher.utter_message(text = "Willst du deinen Cocktail mit oder ohne Alkohol?", buttons = options)
        
class Alcoholic(Action):
    
    def name(self):
        return 'action_alcoholic'
    
    def run(self, dispatcher, tracker, domain):
        SlotSet(key = 'alcohol', value = 'Alcoholic')
        dispatcher.utter_message('Ahh. Du bist also ein draufgänger.')

 
class getCocktails(Action):
    
    def name(self):
        return 'action_get_cocktails'
    
    def run(self, dispatcher, tracker, domain):
        reactions = {
            "Alcoholic": "Ahh. Du bist also ein draufgänger.",
            "Non alcoholic": "Sehr vorbildlich."
        }
        
        cocktailSelectionText = [
            "Da hätte ich ein paar die passen könnten",
            "Ich hab was gefunden. \n Trommelwirbel🥁🥁🥁",
            "Wie wäre es mit einen von diesen?"
        ]
        
        alcohol = tracker.get_slot("alcohol")
        taste = tracker.get_slot("taste")
        
        results = filterCocktails(taste, alcohol)
        
        dispatcher.utter_message(text = reactions[tracker.get_slot("alcohol")][0])
        dispatcher.utter_message(text = random.sample(cocktailSelectionText, 1))
        dispatcher.utter_message(json_message = results)         
        
def filterCocktails(taste, alcohol):
    filteredCocktails = []
    
    for cocktailName in data:
        cocktail = data[cocktailName]
        if cocktail["strAlcoholic"] == alcohol and cocktail["taste1"] == taste:
            filteredCocktails.append(compileCocktailData(cocktail))
            
    if len(filteredCocktails) < 3:
        for cocktailName in data:
            cocktail = data[cocktailName]
            if cocktail["strAlcoholic"] == alcohol and cocktail["taste2"] == taste:
                filteredCocktails.append(compileCocktailData(cocktail))
    if len(filteredCocktails) < 3: return filteredCocktails
    return random.sample(filteredCocktails, 3)

def compileCocktailData(cocktail):
    ingridientsList = []
    
    for key in cocktail:
        if key.startswith('strIngredient') and cocktail[key] != 'null':
            ingridientsList.append(cocktail[key])
    
    if cocktail['strInstructionsDE'] == 'null': instruction = cocktail['strInstructions']
    else: instruction = cocktail['strInstructionsDE']
    
    return {'name': cocktail['strDrink'], "ingredients": ingridientsList, "url": cocktail['strDrinkThumb'], "instructions": instruction}