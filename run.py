# This file is responsible for running the entire Etonians.co.uk application.
# Copyright © Etonians.co.uk 2020. All rights reserved.
# Copyright © Simba Shi 2020. All rights reserved.

from etonians import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
