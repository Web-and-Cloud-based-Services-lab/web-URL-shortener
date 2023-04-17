from api import app
from dataInitiator import dataInitiator

if __name__ == '__main__':
    # dataInitiator.sample_urls_to_database()
    app.run(debug=False)