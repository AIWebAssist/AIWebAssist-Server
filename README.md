# AIWebAssist Server


''' docker build .  --target prod -t web_assists_prod '''
''' docker run -p 3000:3000 -it --rm web_assists_prod '''


'''python3 -m venv env && source env/bin/activate '''


curl --insecure -L -X POST \
  https://127.0.0.1:3000/status \
  -H 'Content-Type: application/json' \
  -d '{
    "execution_status": "response",
    "session_id": "session_id"
}'


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