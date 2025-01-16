# Twitter Trending Topics Scraper

This project scrapes trending topics from Twitter and stores them in a MongoDB database. It uses Selenium for web scraping.

# Note

 THIS SCRIPT DOES NOT USE ANY ENVIRONMENT VARIABLES AND IS INTENDED FOR TESTING PURPOSES ONLY. IF YOU ENCOUNTER ERRORS WHILE USING IT, IT DOES NOT NECESSARILY INDICATE AN ISSUE WITH THE APPLICATION ITSELF. REPEATED TESTING MAY RESULT IN TWITTER BLOCKING THE ACCOUNT, LEADING TO LOGIN FAILURES. IN SUCH CASES, THE PROGRAM MIGHT SHUT DOWN OR CRASH WITHOUT PROVIDING RESULTS. IF NEEDED, USE YOUR TWITTER CREDENTIALS INSTEAD.


## Features

- Scrapes trending topics from Twitter
- Stores scraped data in MongoDB
- Displays the latest and historical scrape results
- Uses ProxyMesh for rotating proxies



## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/twitter-trending-scraper.git
cd twitter-trending-scraper
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MongoDB

- Create a MongoDB Atlas account and set up a cluster.
- Create a database named `twitterDB` and a collection named `trends`.
- Update the MongoDB connection string in `app.py` with your credentials.

### 5. Configure ProxyMesh

- Create a ProxyMesh account.
- Add your IP to the ProxyMesh allowlist.
- Update the ProxyMesh credentials in `app.py` with your username and password.

### 6. Run the Application

```bash
python app.py
```

### 7. Access the Web Interface

- Open your browser and go to `http://127.0.0.1:5000/`
- Click the "Scrape New Trending Topics" button to start scraping.

## Project Structure

```
twitter-trending-scraper/
│
├── app.py                  # Main application file
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html          # HTML template for the web interface
└── proxy_auth_plugin.zip   # Chrome extension for proxy authentication
```

## Troubleshooting

### Common Errors

- **ERR_TUNNEL_CONNECTION_FAILED**: Ensure your IP is added to the ProxyMesh allowlist and the proxy credentials are correct.
- **MongoDB Connection Error**: Verify your MongoDB connection string and network access settings.

### Logs

Check the terminal output for detailed logs and error messages.



## Contact

For any questions or support, please contact [yourname@example.com](mailto:sidanace@gmail.com).
