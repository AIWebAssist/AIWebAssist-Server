# AIWebAssist Server


## Running Localy 

1. create local SSL certificates:
    - Allow the script to run: ```chmod +x ssl/generate_certs.sh```
    - Run the script and create on the spot ssl certificates: ```./ssl/generate_certs.sh``` and enter at least email 
    - Add "myCa.pem" into keychain, double click and 'trust always'

2. Add scrape_anything to host file:
    - ```sudo nano /private/etc/hosts```
    - ```127.0.0.1 scrape_anything```

3. Start server:

    - Docker:
      ```bash
        docker compose up
      ```
    - Local:
      ```bash
        python3 -m venv env && source env/bin/activate &&  pip install -r requirements.txt
      ```
      then:
      ```python main.py```

## Calling the backend:

Get Token:

  ```bash
  curl --insecure -L -X POST \
    https://127.0.0.1:3000/auth \
    -H 'Content-Type: application/json' \
    -d '{
      "email": "sefi"
  }'
  ```
to get token JWT_TOEKN, then:

Call to get action request:

    ```bash
    curl --insecure -L  -X POST \
      https://127.0.0.1:3000/process \
      -H 'Content-Type: application/json' \
      -H 'Authorization: Bearer JWT_TOEKN' \
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
      -H 'Authorization: Bearer JWT_TOEKN' \
      -d '{
        "execution_status": "response",
        "session_id": "session_id"
    }'
    ```

Or 
  - You can install the [extesnion](https://github.com/AIWebAssist/AIWebAssistExtension)
