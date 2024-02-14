# AIWebAssist Server


## Local Setup 

1. Create a local SSL certificates:

    a. Allow the script by running: ```chmod +x ssl/generate_certs.sh```

    b. Run the script and create on the spot ssl certificates: ```./ssl/generate_certs.sh``` and enter at least your email. 

    c. Add "myCa.pem" into keychain, double click and 'trust always'


2. Add a local route from  ```scrape_anything``` to ```localhost```:

    a. Open host files with sudo: ```sudo nano /private/etc/hosts```

    b. Add the following entry: ```127.0.0.1 scrape_anything```

3. Create local env:

    a. Copy ```.env.example``` and rename to ```.env```

    b. Populate the values in the ```.env``` file

## Creating devlopment environment:

1. Create local python environment:

    a. On the termianl run ```python3 -m venv env```

    b. Activate the create environment source ```env/bin/activate```

    c. Install python dependencies ```pip3 install -r requirements-dev.txt``` and ```pip3 install -r requirements.txt```

    d. Allow the script by running: ```chmod +x setup.sh```

    e. Run Setup: ```./setup```
 

2. Entry Points:
(If you are using [VScode IDE](https://code.visualstudio.com/) you can simply use the per-configured in vscode)

  - Running a full simulatation of backend-client call:
    ```python
      python main.py 
    ```

  - Or, running the server only:
    ```python
      python simulate.py 
    ```

## Running the backend localy independent:

  1. Install [docker](https://www.docker.com/products/docker-desktop/)

  2. Start the docker server from locall setup:
      
      ```bash
        docker compose up -d 
      ```


## The backend interface:


### Using bash:

  Every call should start with:

    ```bash
    curl --insecure -L  -X POST \
      https://127.0.0.1:3000/process \
      -H 'Content-Type: application/json' \
      -d '{
        "viewpointscroll": "viewpointscroll_value",
        "viewportHeight": "viewportHeight_value",
        "scroll_width": "scroll_width_value",
        "scroll_height": "scroll_height_value",
        "width": "width_value",
        "height": "height_value",
        "raw_on_screen": "elements_value",
        "url": "url_value",
        "user_task": "objective_value",
        "session_id": "session_id_value",
        "screenshot": "screenshotImage_value"
    }'
    ```

  And end with:

    ```bash
    curl --insecure -L -X POST \
      https://127.0.0.1:3000/status \
      -H 'Content-Type: application/json' \
      -d '{
        "execution_status": "response",
        "session_id": "session_id"
    }'
    ```

### Using the extesnion:

You can install the [extesnion](https://github.com/AIWebAssist/AIWebAssistExtension)