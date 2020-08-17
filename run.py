"""
This file is responsible for running the whole Eton Blog application.
"""

from etonblog import app

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")
