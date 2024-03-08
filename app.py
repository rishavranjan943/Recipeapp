from flask import Flask,render_template,request

# render_template -> used to render html web applications
# request -> used to get data from the web application

import requests
from urllib.parse import unquote

from dotenv import load_dotenv
import os



app=Flask(__name__)

API_KEY = os.environ.get("API_KEY")

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        query=request.form.get('search_query','')

        recipes=search_recipes(query)
        return render_template('index.html', recipes=recipes, search_query=query)
    
    else:
        search_query=request.args.get('search_query', '')
        decoded_search_query=unquote(search_query)
        recipes=search_recipes(decoded_search_query)
        return render_template('index.html', recipes=recipes, search_query=decoded_search_query)
    

def search_recipes(query):
    url = f'https://api.spoonacular.com/recipes/complexSearch'
    params = {
        'apiKey': API_KEY,
        'query': query,
        'number': 10,
        'instructionsRequired': True,
        'addRecipeInformation': True,
        'fillIngredients': True,
    }
    response=requests.get(url, params=params)

    if response.status_code==200:
        data=response.json()
        return data['results']  
    
    return []

@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    # Get the search query from the URL query parameters
    search_query = request.args.get('search_query', '')
    # Build the URL to get information about the specific recipe ID from Spoonacular API
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
    params = {
        'apiKey': API_KEY,
    }

    # Send a GET request to the Spoonacular API to get the recipe information
    response = requests.get(url, params=params)
    # If the API call is successful
    if response.status_code == 200:
        recipe = response.json()
        return render_template('view_recipe.html', recipe=recipe, search_query=search_query)
    return "Recipe not found", 404


# Run the app in debug mode if executed directly
if __name__ == '__main__':
    app.run(debug=True)