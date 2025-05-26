# Home Test

## How to setup the project? 🗂️

- Setup the Python virtual environment and it needs `Python >= 3.12.7`

  - Create by Python `venv` module

    ```bash
    # Create a new virtual environment
    python -m venv .venv

    # Start virtual environment
    source .venv/bin/activate

    # Update the pip
    pip install --upgrade pip

    # Install required packages
    pip install -r $( pwd )/requirements/requirements-dev.txt
    ```

  - Use uv to build environment

    Create virtual environment by [`uv`](https://docs.astral.sh/uv/)

    ```bash
    # Create the environment by `uv.lock` and `pyproject.toml` files
    uv sync

    # Start the virtual environment
     source .venv/bin/activate
    ```

## Project Structure 🗼

- **Directories**

  - [src](./src) - It is used for setting main modules.
    - [finnhub](./src/finnhub/) - Finnhub API client implementation
    - [twitch](./src/twitch/) - Twitch page implementation
      - [elements] - Twitch page element implementation
    - [utils](./src/utils) - The utilities module and the utility functions.
    - [validate_models](./src/validate_models/) - API response validation models
    - [config.py](./src/config.py) - Set environment and configuration files
    - [webdriver](./src/webdriver/) - Encapsulates the Selenium driver to simplify usage.
  - [tests](./tests) - It is used for saving the test cases
  - [unit_tests](./unit_tests/) - It is used for setting unit test for main modules
  - [driver_config](./driver_config/) - The webdriver configuration, which includes different browser types.
  - [envs](./envs/) - Set the enviroment variables
  - [requirements](./requirements/) - Project dependencies, which includes development dependencies and deployment dependiencies.
  - [html_reports](./html_reports/) - Save the test reports
  - [pytest.ini](./pytest.ini) - Pytest settings

## How to execute the test? 💻

Before executing the test, you need to apply for the FinnHub API key and set it to
the `FINN_HUB_API_KEY` variable in the `./envs/.env` file

There are two ways that you can execute the test.

- Run on local browser

  - You need to check the [`chrom_config.json`](./driver_config/chrome_config.json) file first (using chrome as example). Must ensure that the `remote_url` is set to `null`; Otherwise, it will use remote Selenium server.

    ```json
    {
        "driver": {
            "browser": "chrome",
            "remote_url": null, // <- Make sure it is null
            "driver_path": null,
            "browser_options": [
            "--disable-gpu",
            "--no-sandbox",
            "--start-maximized",
            "--enable-logging"
            ],
            "capabilities": {
            "goog:loggingPrefs": {
                "performance": "ALL",
                "browser": "ALL",
                "client": "ALL",
                "server": "ALL",
                "driver": "ALL"
            }
            },
            "experimental_options": { "mobileEmulation": { "deviceName": "iPhone X" } },
            "extension_paths": [],
            "webdriver_kwargs": {},
            "page_load_wait_time": 10,
            "implicitly_wait": 5
        },
        "log": {
            "screenshot_on": true
        },
        "viewport": {
            "maximize": true,
            "width": 1440,
            "height": 900,
            "orientation": "portrait"
        }
    }
    ```

  - After checking, running the following command, It will automatically dowload the webdriver on your local computer then execting the test cases.

    ```bash
    # Execute all test cases
    pytest -vv tests --html="./html_reports/$(date '+%Y-%m-%d-%H-%M-%S').html" --self-contained-html

    ## Only execute web test
    # pytest -vv -m web_test tests --html="./html_reports/$(date '+%Y-%m-%d-%H-%M-%S').html" --self-contained-html

    ## Only execute the api test
    # pytest -vv -m api_test tests --html="./html_reports/$(date '+%Y-%m-%d-%H-%M-%S').html" --self-contained-html
    ```

- Run on docker selenium

  - You need to check the [`chrom_config.json`](./driver_config/chrome_config.json) file first (using chrome as example). Must ensure that the `remote_url` is set to `http://127.0.0.1:4444`; Otherwise, it will use local driver.

    ```json
    {
        "driver": {
            "browser": "chrome",
            "remote_url": "http://127.0.0.1:4444", // <- Make sure it
            "driver_path": null,
            "browser_options": [
            "--disable-gpu",
            "--no-sandbox",
            "--start-maximized",
            "--enable-logging"
            ],
            "capabilities": {
            "goog:loggingPrefs": {
                "performance": "ALL",
                "browser": "ALL",
                "client": "ALL",
                "server": "ALL",
                "driver": "ALL"
            }
            },
            "experimental_options": { "mobileEmulation": { "deviceName": "iPhone X" } },
            "extension_paths": [],
            "webdriver_kwargs": {},
            "page_load_wait_time": 10,
            "implicitly_wait": 5
        },
        "log": {
            "screenshot_on": true
        },
        "viewport": {
            "maximize": true,
            "width": 1440,
            "height": 900,
            "orientation": "portrait"
        }
    }
    ```

  - Start the Selenium remote server with docker (using chrome as example)

    ```bash
    # Can open `http://localhost:7900/` to inspect visually container activity with their browser
    docker run -d -p 4444:4444 -p 5900:5900 -p 7900:7900 -e SE_VNC_NO_PASSWORD=true --shm-size="2g" selenium/standalone-chromium:4.32.0-20250515
    ```

  - Running the following command, It will automatically connect to the remote Selenium server then execting the test cases.

    ```bash
    # Execute all test cases
    pytest -vv tests --html="./html_reports/$(date '+%Y-%m-%d-%H-%M-%S').html" --self-contained-html

    ## Only execute web test
    # pytest -vv -m web_test tests --html="./html_reports/$(date '+%Y-%m-%d-%H-%M-%S').html" --self-contained-html

    ## Only execute the api test
    # pytest -vv -m api_test tests --html="./html_reports/$(date '+%Y-%m-%d-%H-%M-%S').html" --self-contained-html
    ```

- Once the test finished, the test report will be geneated in the [`html_reports/`](./html_reports/) directory

## Summary

- WAP
  - The test flow can refer to [`test_twitch.py`](./tests/twitch/test_twitch.py). It handles the two situations while clicking the streamer element.
    - Recommended Twitch channel: It isn't live, no video is available and it has a chance automatically added to the streamer list once Selenium locates the target elements.

    <img src=./image/recommanded_channel.png alt="Description" width="300" height="500"/>

    - The pop-up warning message element overlay the video element.

    <img src=./image/warning_msg_popup.png alt="Description" width="300" height="500"/>

  - Both of the above situations occur after clicking the streamer element, so I created two steps to handle it.
    - Check the element whether it is a video element(wait until video time large than 0 and not in paused). If it is, take a screenshot and stop while loop. Otherwise, processed to the next step.
    - Locate the pop-up element. If found, click `start watching` button then use step1 again to check whether the element is video or not. If yes, take a screenshot and stop while loop. Otherwise, back to the streamer list page and scroll down again, and click the streamer.

- [Finnhub](https://finnhub.io/docs/api/) API Testing

| Method | Path            | API NAME               | Test Cases                                                                                                                                                                                                                                            |
| ------ | --------------- | ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GET    | symbol_lookup   | /api/v1/search         | Steps: (1). Use the symbol_lookup API with different arguments and token to get status code and response (2). Check the status code and its response structure                                                                                        |
| GET    | company_profile | /api/v1/stock/profile2 | (1). Use the company_profile API with different arguments and token to get status code and response (2). Check the status code and its response structure                                                                                             |
| GET    | quote           | /api/v1/quote          | Steps: (1). Use the quote API with different arguments and token to get status code and response (2). Check the status code and its response structure                                                                                                |
| GET    | company_news    | /api/v1/company-news   | Steps: (1). Use the company_news API with different arguments and token to get status code and response (2). Check the status code and its response structure (3). Check the datetime of the response whether it is between the from_date and to_date |

- Validation
  - All of the API validate their status codes, response data format and date types. Each API must conform to the specification, which servers as the foundation.
  - The datetime filter function on Company News API. If it fails, the API may return data that doesn't match user's expections.
  - API key authorized validation. To ensure API security and reliablity.

- Result & Reports

  - ScreenShot

    <img src=./image/2025-05-26-10-18-36.png alt="screenshot" width="300" height="500"/>

  - Reports: [Example html reports](./html_reports/2025-05-26-18-18-02.html)

    <img src=./image/html-reprots.png alt="html-reports" width="900" height="800"/>
