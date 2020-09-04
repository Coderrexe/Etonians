# This file is responsible for running the entire Etonians.co.uk application.
# Copyright © Etonians.co.uk 2020
# Copyright © Simba Shi 2020

from etonblog import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")
