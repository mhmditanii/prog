import dearpygui.dearpygui as dpg
import threading
import data_req
import re

def is_valid_url(url):
    pattern = r"^https://[^\s/]+\.com(?:/[^\s]*)?$"
    return re.match(pattern, url)

def validate_url(sender):
    url = dpg.get_value("url_input")
    if is_valid_url(url):
        dpg.bind_item_theme("url_input", "valid_theme")
        dpg.configure_item("search_button", enabled=True)
    else:
        dpg.bind_item_theme("url_input", "invalid_theme")
        dpg.configure_item("search_button", enabled=False)

def toggle_search_terms(sender, app_data):
    dpg.configure_item("search_terms_input", show=app_data)

def search_callback():
    url = dpg.get_value("url_input")
    if not is_valid_url(url):
        dpg.set_value("result_box", "Invalid URL. Please enter a valid one.")
        return
    data_req.url = url 
    dpg.set_value("result_box", "Scraping, please wait...")

    def run_scraper():
        try:
            data_req.open_website()
            headlines = None

            if dpg.get_value("search_terms_checkbox"):
                terms = dpg.get_value("search_terms_input")
                terms = [term.strip() for term in terms.split(",")]
                headlines = data_req.search_website_for_keywords(terms)
            else:
                headlines = data_req.scrape_headlines()
                data_req.save_results_json(headlines)

            if not headlines:
                dpg.set_value("result_box", "No headlines found.")
            else:
                result_text = "\n\n".join(f"{i+1}. {headline}" for i, headline in enumerate(headlines))
                dpg.set_value("result_box", result_text)
        except Exception as e:
            dpg.set_value("result_box", f"Error: {e}")

    threading.Thread(target=run_scraper, daemon=True).start()

# GUI setup
dpg.create_context()
dpg.create_viewport(title='News Scraper', width=1280, height=720)
dpg.setup_dearpygui()

with dpg.theme(tag="invalid_theme"):
    with dpg.theme_component(dpg.mvInputText):
        dpg.add_theme_color(dpg.mvThemeCol_Text, [255, 0, 0, 255])

with dpg.theme(tag="valid_theme"):
    with dpg.theme_component(dpg.mvInputText):
        dpg.add_theme_color(dpg.mvThemeCol_Text, [0, 255, 0, 255])

with dpg.window(label="Main Window", tag="MainWindow", no_title_bar=True, no_resize=True, no_move=True, width=1280, height=720):
    dpg.add_spacer(height=20)
    dpg.add_text("Scrape Headlines from a URL")
    dpg.add_input_text(label="URL", tag="url_input", hint="ex. https://example.com", width=600, callback=validate_url)
    dpg.add_checkbox(label="Add Search Terms", tag="search_terms_checkbox", callback=toggle_search_terms)
    dpg.add_input_text(label="Search Terms", hint = "seperate terms by','", tag="search_terms_input", width=600, show=False)
    dpg.add_button(label="Search", tag="search_button", callback=search_callback, width=150, enabled=False)
    dpg.add_spacer(height=20)
    dpg.add_text("Results")
    dpg.add_input_text(tag="result_box", multiline=True, readonly=True, width=1000, height=400)

dpg.set_primary_window("MainWindow", True)
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

