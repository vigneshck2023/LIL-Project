import requests
from bs4 import BeautifulSoup
from recipe_scrapers import scrape_me
from tabulate import tabulate
import webbrowser
import tkinter as tk
import time

def program():
    result_label.configure(text=f"")
    query = entry1.get()
    num_results = 100
    similarRecipes = []
    submit = []
    try:
        similarRecipes = scrape_google_search_results(query, num_results)
    except Exception as e:
        #print("Server down :(")
        result_label.configure(text=f"Server down :()")
        #print(e)
    for i in similarRecipes:
        try:
            pass
        #   print(i.title())
        except:
            continue
    foodConstraint = entry2.get()

    #print("Recommendation Conceptual Demonstration")
    #inputRecipe = scrape_me(input())
    #for i in inputRecipe.ingredients():
    #    if foodConstraint in i:
    #        print(foodConstraint.capitalize() + " found in the recipe " + inputRecipe.title())
    #print("Search alternative recipes: ")
    #similarRecipes = [scrape_me("https://www.allrecipes.com/recipe/17981/one-bowl-chocolate-cake-iii/"), scrape_me("https://www.foodnetwork.com/recipes/food-network-kitchen/basic-chocolate-cake-recipe-2120876"), scrape_me("https://handletheheat.com/best-chocolate-cake/"), scrape_me("https://www.indianhealthyrecipes.com/eggless-chocolate-cake-moist-and-soft/#Ingredients_and_substitutions"), scrape_me("https://www.mybakingaddiction.com/eggless-chocolate-cake/")]

    state = 0
    for i in similarRecipes:
        """
        for j in i.ingredients():
            if foodConstraint in j:
                state = 1
                break
        if state == 1:
            print(foodConstraint + " in " + i.title() + " from " + i.site_name())
        else:
            print(foodConstraint + " not in " + i.title() + "from" + i.site_name())
        """
        try:
            a = isPresent(i, foodConstraint, submit)
        except:
            continue
    textString = f""
    for i in submit:
        textString += f"\n{i[0]} {i[1]} {i[2]}"
    result_label.configure(text=textString)
    #print(textString)




def isPresent(myList, food, submit):
    for item in myList.ingredients():
        if food in item:
            return True
    try:
        submit.append([myList.title(), myList.site_name(),myList.canonical_url()])
#        choice = input(f"Recipe without {food} found. Open?")
#        if choice == 'y':
#            webbrowser.open(myList.canonical_url(), new=2)
#        else:
#            print("End")
#        return False
    except:
        return True
def scrape_google_search_results(query, num_results):
    url = f"https://www.google.com/search?q={query}&num={num_results}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    search_results = soup.select("div.g")

    urls = []
    for result in search_results:
        link = result.select_one("a")
        if link:
            try:
                url = scrape_me(link["href"])
                if url.title() is not None:
                    urls.append(url)
            except:
                continue

    return urls

app = tk.Tk()
app.title("Food Recommender System")

# Set the window size (width x height)
app.geometry("1000x800")
#app.attributes("-fullscreen", True)

# Create input fields
label1 = tk.Label(app, text="Whats on your mind?:")
label1.pack()

entry1 = tk.Entry(app)
entry1.pack()

label2 = tk.Label(app, text="FOODS TO AVOID:")
label2.pack()

entry2 = tk.Entry(app)
entry2.pack()


calculate_button = tk.Button(app, text="Find results for you!", command=program)
calculate_button.pack()

result_label = tk.Label(app, text="")
result_label.pack()

app.mainloop()
