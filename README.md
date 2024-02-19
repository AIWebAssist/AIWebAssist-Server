# AIWebAssist Server
Backend to support making a decision of what action to preform in web broswer base on user task.

## Project stracture

Files defining the code runtime:
- **`.devcontainer`**: Configuration for development container settings.

- **`.vscode`**: VSCode-specific settings, including launch configurations.

- **`Dockerfile`**: Configuration file for building a Docker image.
  
- **`docker-compose.yaml`**: Docker Compose configuration for easy deployment.

- **`requirements-dev.txt`**: List of development dependencies.

- **`requirements.txt`**: List of dependencies for the server.

File defining logic:

- **`scrape_anything`**: Directory that contains the entire logic to process the request.

- **`simulation_utils`**: Directory that contains code the support simulation of the calls to the server.

- **`main.py`**: The main entry to the server.

- **`simulate.py`**: The main entry to the simulation.

## Local Setup

1. Create local SSL certificates (if you are running on windows, run the commends from wsl)

    a. Allow the script by running: `chmod +x ssl/generate_certs.sh`

    b. Run the script and create on-the-spot SSL certificates: `./ssl/generate_certs.sh` and enter at least your email.

    c. Add "myCa.pem" into the keychain, double click and 'trust always'. if you are using windows you can follow the original [thread](https://stackoverflow.com/a/60516812)

2. Add a local route from `scrape_anything` to `localhost`:

    a. Open host files as admin. 

      - Linux/Mac: `sudo nano /private/etc/hosts`
      
      - Windows `C:\Windows\System32\drivers\etc\host`

    b. Add the following entry: `127.0.0.1 scrape_anything`

3. Create local env:

    a. Copy `.env.example` and rename to `.env`

    b. Populate the values in the `.env` file

## Creating development environment:

1. Create a local Python environment:

    a. On the terminal run `python3 -m venv env`

    b. Activate the created environment source:
    
      - Linux/Mac: `env/bin/activate`

      - Windows `env/Scripts/activate.bat`

    c. Install Python dependencies `pip3 install -r requirements-dev.txt` and `pip3 install -r requirements.txt`

    d. Allow the script by running: `chmod +x setup.sh` (for windows from wsl)

    e. Run Setup: `./setup` (for windows from wsl)

2. Entry Points: (If you are using [VScode IDE](https://code.visualstudio.com/) you can simply use the pre-configured in vscode)

    - Running a full simulation of backend-client call:

      ```python
      python main.py 
      ```

    - Or, running the server only:

      ```python
      python simulate.py 
      ```

    - don't forgut to install the python extensions.

## Running the backend locally independent:

1. Install [Docker](https://www.docker.com/products/docker-desktop/)

2. Start the Docker server from local setup:

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