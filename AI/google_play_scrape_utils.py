from .common_imports import *

# Google Play Store Scraper
def fetch_app_description(app_id: str, app_name: str, country: str = 'in', lang: str = 'en'):
    """
    Fetches the app description from the Google Play Store
    """
    loaded_api_result_app = google_play_scraper.app(app_id,lang='en',country='in') 
    loaded_api_result_app['title'] = app_name
    return loaded_api_result_app
