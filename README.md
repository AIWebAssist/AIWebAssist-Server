# AIWebAssist Server


  ```bash
    docker build .  --target prod -t web_assists_prod 
  ```

```bash 
  docker run -p 3000:3000 -it --rm web_assists_prod 
```


```bash
   python3 -m venv env && source env/bin/activate
```


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
    "screenshot": "screenshot_image_value"
}'
```

Call to report the status:
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




```sudo nano /private/etc/hosts```
```127.0.0.1 scrape_anything```

```
  OPENAI_API=
  JWT_TOEKN=
```