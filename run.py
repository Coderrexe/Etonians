# This file is responsible for running the entire Etonians application.
# Copyright © Etonians 2020. All rights reserved.
# Copyright © Simba Shi 2020. All rights reserved.

from etonians import create_app
from etonians.config import Config

app = create_app(Config)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
