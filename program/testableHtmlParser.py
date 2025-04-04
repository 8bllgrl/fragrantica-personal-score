from enum import Enum
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import re

from program.aopadder import AOP
from program.model.parfum import *

@AOP.log_method_call
@AOP.log_execution_time
def setup_driver():
    """Sets up and returns a headless Selenium WebDriver."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

@AOP.log_method_call
@AOP.log_execution_time
def find_main_title(soup):
    """Finds and returns the main perfume title from the page."""
    title_element = soup.find("h1", {"itemprop": "name"})
    if title_element:
        return title_element.get_text(strip=True)
    return None

@AOP.log_method_call
@AOP.log_execution_time
def extract_style_value(style_string, property_name):
    """Extracts a specific CSS property value from a style string."""
    match = re.search(f"{property_name}: ([^;]+);", style_string)
    return match.group(1) if match else None

@AOP.log_method_call
@AOP.log_execution_time
def extract_style_value_notes(style_string, property_name):
    """Extracts a specific CSS property value from a style string."""
    match = re.search(f"{property_name}: ([^;]+);", style_string)
    return float(match.group(1).replace("rem", "")) if match else None

@AOP.log_method_call
@AOP.log_execution_time
def handle_missing_notes(soup):
    """Fallback method to handle missing notes."""
    notes = []
    alternative_section = soup.find("div", style=lambda
        s: s and "display: flex" in s and "text-align: center" in s and "background: white" in s)
    if alternative_section:
        title = alternative_section.find("h3")
        if title and title.find("span", string="Fragrance Notes"):
            notes_container = alternative_section.find("div", style=lambda
                s: s and "display: flex" in s and "flex-flow: wrap" in s)
            if notes_container:
                for note_div in notes_container.find_all("div", recursive=False):
                    img_tag = note_div.find("img")
                    name_tag = note_div.find("a")

                    if img_tag and name_tag:
                        name = note_div.get_text(strip=True).replace(name_tag.get_text(strip=True), "").strip()
                        name = name.replace("-", " ")

                        image_url = img_tag["src"]
                        width = extract_style_value_notes(img_tag.get("style", ""), "width")
                        opacity = extract_style_value_notes(note_div.get("style", ""), "opacity")

                        notes.append(Note(name, image_url, width, opacity, NoteCategory.UNKNOWN))

    return notes

@AOP.log_method_call
@AOP.log_execution_time
def find_perfume_notes(soup):
    """Finds and organizes fragrance notes."""
    categories = {
        "Top Notes": NoteCategory.TOP,
        "Middle Notes": NoteCategory.MIDDLE,
        "Base Notes": NoteCategory.BASE,
        "N/A": NoteCategory.UNKNOWN,
    }

    notes = []
    for category_name, category_enum in categories.items():
        section = soup.find("h4", string=category_name)
        if section:
            container = section.find_next("div", style=True)
            for note_div in container.find_all("div", recursive=False):
                img_tag = note_div.find("img")
                name_tag = note_div.find("a")

                if img_tag and name_tag:
                    name = note_div.get_text(strip=True).replace(name_tag.get_text(strip=True), "").strip()
                    name = name.replace("-", " ")

                    image_url = img_tag["src"]
                    width = extract_style_value_notes(img_tag.get("style", ""), "width")
                    opacity = extract_style_value_notes(note_div.get("style", ""), "opacity")

                    notes.append(Note(name, image_url, width, opacity, category_enum))

    if not notes:
        notes = handle_missing_notes(soup)

    notes.sort(key=lambda note: note.width, reverse=True)
    return notes

@AOP.log_method_call
@AOP.log_execution_time
def find_accords_section(soup):
    """Finds all accord elements and stores them as objects."""
    accord_elements = soup.select("div.cell.accord-box div.accord-bar")
    accords = []

    for accord in accord_elements:
        name = accord.get_text(strip=True)
        style = accord.get("style", "")
        background = extract_style_value(style, "background")
        width = extract_style_value(style, "width")
        opacity = extract_style_value(style, "opacity")

        accords.append(Accord(name, background, width, opacity))

    return accords

@AOP.log_method_call
@AOP.log_execution_time
def scrape_page(url, driver=None):
    """Main function to fetch page source and extract required details."""
    if driver is None:
        driver = setup_driver()

    driver.get(url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    title = find_main_title(soup)
    accords = find_accords_section(soup)
    notes = find_perfume_notes(soup)

    driver.quit()

    return PerfumeDetails(perfume_name=title, accords=accords, notes=notes, url=url)