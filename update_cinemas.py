import json
import requests
import os
from datetime import datetime

CINEMAS_FILE = 'cinemas.json'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def load_cinemas():
    if not os.path.exists(CINEMAS_FILE):
        return {"cinemas": []}
    with open(CINEMAS_FILE, 'r') as f:
        return json.load(f)

def save_cinemas(data):
    with open(CINEMAS_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def scrape_everyman(venue_url):
    """
    Scrapes Everyman Bristol movie data using their Gatsby page-data.json.
    Returns a list of dictionaries with 'title', 'link', 'times' (empty).
    """
    print("Scraping Everyman Bristol...")
    # The page-data URL is specific to the venue.
    # Base URL: https://www.everymancinema.com/page-data/venues-list/x0x3q-everyman-bristol/page-data.json
    api_url = "https://www.everymancinema.com/page-data/venues-list/x0x3q-everyman-bristol/page-data.json"
    movies = []
    
    try:
        response = requests.get(api_url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        
        # Correct path: result -> data -> page -> widgets
        widgets = data.get('result', {}).get('data', {}).get('page', {}).get('widgets', [])
        print(f"DEBUG: Found {len(widgets)} widgets.")
        
        film_pages = []
        for i, widget in enumerate(widgets):
            typename = widget.get('__typename')
            if typename == 'WidgetNavigation':
                print(f"DEBUG: Found WidgetNavigation at index {i}")
                items = widget.get('navigationShape', {}).get('menu', {}).get('items', [])
                print(f"DEBUG: Menu items count: {len(items)}")
                for item in items:
                    label = item.get('label')
                    print(f"DEBUG: Checking item label: {label}")
                    if label == 'All films':
                         film_pages = item.get('page', {}).get('childPages', [])
                         print(f"DEBUG: Found 'All films' with {len(film_pages)} child pages.")
                         break
        
        print(f"Found {len(film_pages)} films via page-data.")


        for film in film_pages:
            slug = film.get('slug', '')
            if not slug:
                continue
            
            # Slug format: "film-listing/12345-movie-title"
            # Extract Title: Remove "film-listing/" and id.
            clean_slug = slug.replace("film-listing/", "")
            parts = clean_slug.split("-")
            # Usually the first part is ID if it's numeric
            if parts and parts[0].isdigit():
                parts.pop(0)
            
            title = " ".join(parts).title()
            
            # Construct deep link
            link = f"https://www.everymancinema.com/{slug}/"
            
            movies.append({
                "title": title,
                "link": link,
                "times": [] # Times not available in this JSON, frontend will handle this
            })
            
    except Exception as e:
        print(f"Error scraping Everyman: {e}")
        
    return movies

def main():
    data = load_cinemas()
    updated_count = 0
    
    for cinema in data.get('cinemas', []):
        if "Everyman" in cinema['name']:
            shows = scrape_everyman(cinema['url'])
            # Always update if we tried, even if empty (to plain outcome)
            # But only if successful call
            if shows or isinstance(shows, list):
                cinema['showtimes'] = shows
                cinema['last_updated'] = datetime.now().isoformat()
                updated_count += 1
        
        # Add scrapers for others here
        
    save_cinemas(data)
    print(f"Updated {updated_count} cinemas.")

if __name__ == "__main__":
    main()
