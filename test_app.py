import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="module")
def driver():
    # Setup Chrome options for testing
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Runs without opening a physical browser window
    
    # Initialize the browser driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Give the server a moment to be up if needed, though we will test the layout file directly
    yield driver
    driver.quit()

# Test 1: Check if the header title matches
def test_header_and_layout():
    # We will import the layout directly from your app to verify the elements are present
    from app import app
    
    layout = app.layout
    children_elements = str(layout)
    
    # 1. Assert Header text is present in layout definitions
    assert "Quantium Sales Visualiser" in children_elements, "Header title is missing!"
    
    # 2. Assert Region Picker (Radio Items component ID) is present
    assert "region-filter" in children_elements, "Region picker filter is missing!"
    
    # 3. Assert Visualisation graph (Graph component ID) is present
    assert "sales-chart" in children_elements, "Sales chart visualization is missing!"
    
    print("\n All 3 layout checks passed successfully!")