import time, uuid
import os
from flask import Flask, render_template, redirect, url_for, send_from_directory
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

@app.route('/scrape')
def scrape():
    print("=== Starting scraping process ===")
    unique_id = str(uuid.uuid4())
    
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # Remove headless mode to see the automation
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-notifications')
    
    try:
        print("Launching Chrome...")
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        wait = WebDriverWait(driver, 20)
        
        # Login process
        print("Navigating to Twitter login...")
        driver.get("https://twitter.com/login")
        time.sleep(3)  # Wait for page load
        
        # Login credentials (replace with your credentials)
        USERNAME = "0901io211099"
        PASSWORD = "UMmhMP(qN9(7A+)"
        
        print("Entering username...")
        username_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]'))
        )
        username_input.send_keys(USERNAME)
        username_input.send_keys(Keys.RETURN)
        time.sleep(2)
        
        print("Entering password...")
        password_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]'))
        )
        password_input.send_keys(PASSWORD)
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)  # Wait for login
        
        print("Navigating to Trending page...")
        driver.get("https://twitter.com/explore/tabs/trending")
        time.sleep(5)
        
        print("Looking for trending topics...")
        # Wait for trending section to load
        time.sleep(5)
        
        # Updated selector to find the trending topics
        topic_containers = driver.find_elements(By.CSS_SELECTOR, "div.css-175oi2r.r-1adg3ll.r-1ny4l3l")
        
        trends = []
        for container in topic_containers[:5]:
            try:
                topic_element = container.find_element(By.CSS_SELECTOR, "div.css-175oi2r")
                trend_text = topic_element.text
                print(f"Found trend: {trend_text}")
                trends.append(trend_text)
            except Exception as e:
                print(f"Error extracting trend: {e}")
        
        print(f"Collected trends: {trends}")
        
        if not trends:
            raise Exception("No trending topics found after authentication")
            
        # MongoDB part
        try:
            print("Connecting to MongoDB...")
            client = MongoClient("mongodb+srv://siddhant:database@cluster0.p5jvp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0/twitterDB",
                                 serverSelectionTimeoutMS=30000,  # Increase from 5000 to 30000
                                 connectTimeoutMS=30000,
                                 socketTimeoutMS=30000)
            # Test the connection
            client.server_info()
            
            db = client["twitterDB"]
            collection = db["trends"]
            
            data = {
                "unique_id": unique_id,
                "trend1": trends[0] if len(trends) > 0 else "N/A",
                "trend2": trends[1] if len(trends) > 1 else "N/A",
                "trend3": trends[2] if len(trends) > 2 else "N/A",
                "trend4": trends[3] if len(trends) > 3 else "N/A",
                "trend5": trends[4] if len(trends) > 4 else "N/A",
                "end_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "ip_address": "Sample-IP"
            }
            
            collection.insert_one(data)
            print("Data saved to MongoDB")
            return redirect(url_for('index'))
            
        except Exception as mongo_error:
            print(f"MongoDB Error: {mongo_error}")
            return f"Database Error: {str(mongo_error)}", 500
            
    except Exception as e:
        print(f"Scraping Error: {e}")
        return f"Scraping Error: {str(e)}", 500
        
    finally:
        time.sleep(2)  # Give time to see the final state
        if 'driver' in locals():
            driver.quit()
            print("Browser closed")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

@app.route('/')
def index():
    client = MongoClient("mongodb+srv://siddhant:database@cluster0.p5jvp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0/twitterDB",
                         serverSelectionTimeoutMS=30000,
                         connectTimeoutMS=30000,
                         socketTimeoutMS=30000)
    print("Connected to the MongoDB database successfully!")
    db = client["twitterDB"]
    collection = db["trends"]
    all_data = collection.find().sort("_id", -1)
    return render_template('index.html', data=all_data)

if __name__ == '__main__':
    app.run(debug=True)