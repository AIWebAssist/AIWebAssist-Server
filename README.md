# AIWebAssist Server



## Running Localy 

1. create local SSL certificates:
 - ```chmod +x ssl/generate_certs.sh```
 - ```./ssl/generate_certs.sh``` and enter at least email 
 - add "myCa.pem" into keychain, double click and 'trust always'

2. Add scrape_anything to host file:
  - ```sudo nano /private/etc/hosts```
  - ```127.0.0.1 scrape_anything```

3. Start server:

  - using docker:
    ```bash
      docker compose up
    ```
  - local:
    ```bash
      python3 -m venv env && source env/bin/activate &&  pip install -r requirements.txt
    ```
    then:
    ```python main.py```

## Calling the backend:

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

or you can install the extesnion.