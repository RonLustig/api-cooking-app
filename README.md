# Cooking App

## Description
This is a Django-based Cooking App that helps users discover and cook recipes. 
The app uses APIs to provide 301 recipes. You can search for recipes by including ingredients you want or excluding ingredients you don’t want. You can also view recipe details on the recipe page.

## Features
- Browse 301 recipes with cooking instructions and macronutrient information.
- Add or remove recipes from your favorites list.
- Leave reviews on recipes or read reviews from others.
- Create your own recipes to share.
- Search recipes by including or excluding specific ingredients 

## Prerequisites
- Python 3.x installed
- pip (Python package installer)

## Setup Instructions
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/repo-name.git
   cd repo-name
2. Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install the required dependencies:
pip install -r requirements.txt
4. Set up the database:
python manage.py migrate
5. Start the server:
python manage.py runserver
6. Open your browser and go to:
http://127.0.0.1:3000/