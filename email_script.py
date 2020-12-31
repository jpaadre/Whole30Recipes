import requests
import json
import yagmail
from datetime import datetime

def pull_recipes():
    with open(".//credentials//recipe_api.json", "r") as handler:
        recipes = json.load(handler)
    
    headers = {}
    headers['x-rapidapi-key'] = recipes['x-rapidapi-key']
    headers['x-rapidapi-host'] = recipes['x-rapidapi-host']
    
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/random"

    querystring = {"number":"5","tags":"whole30"}
    
    response = requests.request("GET", url, headers=headers, params=querystring)
    json_recipes = json.loads(response.text)
    
    return json_recipes

def format_recipe_string(key):
    recipe_string = f"""<h3><strong>{key['title']}</strong></h3>
                    <p><strong><a href="{key['sourceUrl']}">Recipe</a></strong></p>
                    <p>{key['summary']}</p>
                    <p>&nbsp;</p>"""
    return recipe_string

def format_recipe_email_body(json_recipes):
    recipe_html = []
    for i in json_recipes['recipes']:
        recipe_string = format_recipe_string(i)
        recipe_html.append(recipe_string)
    
    recipe_body = "<p>&nbsp;</p>".join(recipe_html)
    email_contents = "<h2><strong>Whole30 Recipes for the Week</strong></h2>" + recipe_body
    return email_contents

def send_email(email_contents):
    today = datetime.now()
    today_form = today.strftime("%B %d")
    
    subject = "Whole30 Suggestions: " + today_form
    
    with open(".//credentials//gmail_api.json", "r") as handler:
        gmail = json.load(handler)
    yag = yagmail.SMTP(user=gmail['user'], password=gmail['password'])
    
    yag.send(to='jeff.paadre@gmail.com', subject=subject, contents=email_contents)
    return 

def email_pipeline():
    json_recipes = pull_recipes()
    email_contents = format_recipe_email_body(json_recipes)
    send_email(email_contents)
    return
    
if __name__ == "__main__":
    email_pipeline()
    