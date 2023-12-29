from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager, jwt_required, create_access_token,get_jwt_identity
from scrape_anything import Agent
from scrape_anything import TextOnlyLLM, VisionBaseLLM
from scrape_anything import RemoteFeedController
from scrape_anything.util import DataBase,Logger
from scrape_anything import OutGoingData, IncommingData, Error
from queue import Queue
import os


class Server:
    agents_queues = dict()
    agents_threads = dict()

    def __init__(self,experiment_uuid=""):
        CORS_HEADERS = 'Content-Type'
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = os.environ['JWT_TOEKN']
        self.jwt = JWTManager(self.app)
        self.experiment_uuid = experiment_uuid
        CORS(self.app)

        self.app.route("/process", methods=["POST", "OPTIONS"])(self.process)
        self.app.route("/status", methods=["POST", "OPTIONS"])(self.status)
        self.app.route("/auth", methods=["POST"])(self.register)

    def register(self):
        data = request.get_json()
        email = data['email']
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token)

    #@jwt_required()
    @cross_origin()
    def process(self):
        if  get_jwt_identity() is None:
            return response, 333
        if request.method == "POST":
            return self.handle_process_request()
        elif request.method == "OPTIONS":
            response = jsonify({})
            response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
            return response, 200

    #@jwt_required()
    @cross_origin()
    def status(self):
        if  get_jwt_identity() is None:
            return response, 333
        if request.method == "POST":
            return self.handle_status_request()
        elif request.method == "OPTIONS":
            response = jsonify({})
            response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
            return response, 200

    def create_access_token(self, identity):
        return create_access_token(identity=identity)
    
    def handle_process_request(self):
        try:
            data = request.get_json()
            if data is None or "session_id" not in data or "user_task" not in data:
                raise ValueError("Invalid JSON input or missing required fields")

            user_task = data["user_task"]
            session_id = str(data.pop("session_id"))

            if session_id not in self.agents_queues:
                self.init_agent(user_task, session_id, max_message=-1)

            return self.process_request(data, session_id)

        except Exception as e:
            Logger.error(f"Error processing request: {str(e)}")
            return jsonify({"error": str(e)}), 500

    def handle_status_request(self):
        try:
            data = request.get_json()
            if data is None or "session_id" not in data:
                raise ValueError("Invalid JSON input or missing required fields")

            session_id = str(data.pop("session_id"))
            return self.process_status(session_id, data)

        except Exception as e:
            Logger.error(f"Error processing status request: {str(e)}")
            return jsonify({"error": str(e)}), 500
        
    def init_agent(self, user_task, session_id, max_message=-1):
        feed_from_chrome = Queue(maxsize=1)
        feed_from_agent = Queue(maxsize=1)
        status_feed_queue = Queue(maxsize=1)

        controller = RemoteFeedController(
            incoming_data_queue=feed_from_chrome,
            outgoing_data_queue=feed_from_agent,
            status_queue=status_feed_queue,
            user_task=user_task,
            max_loops=max_message,
        )
        agnet = Agent(
            llm=VisionBaseLLM(),
            max_loops=max_message,
            session_id=DataBase.get_session_id(self.experiment_uuid),
        )
        self.agents_threads[session_id] = agnet.run_parallel(controller)
        self.agents_queues[session_id] = (
            feed_from_chrome,
            feed_from_agent,
            status_feed_queue,
        )

    def process_status(self, session_id, data):
        (_, _, status_queue) = self.agents_queues[session_id]
        status = data["execution_status"]
        status_queue.put(status)

        return jsonify({}), 200

    def process_request(self, data, session_id):

        (feed_from_chrome, feed_from_agent, _) = self.agents_queues[session_id]
        feed_from_chrome.put(
            IncommingData(
                url=data["url"],
                task=data["user_task"],
                viewpointscroll=data["viewpointscroll"],
                viewportHeight=data["viewportHeight"],
                scroll_width=data["width"],
                scroll_height=data["width"],
                width=data["width"],
                height=data["height"],
                raw_on_screen=data["raw_on_screen"],
                screenshot=data["screenshot"],
            )
        )
        response: OutGoingData = feed_from_agent.get()
        if isinstance(response, Error) and (
            response.is_fatel or response.session_closed
        ):
            self.agents_queues.pop(session_id)
            return jsonify(response.__dict__), 500
        elif isinstance(response, OutGoingData):
            if response.session_closed:
                self.agents_queues.pop(session_id)
            return jsonify(response.__dict__), 200
        else:
            raise ValueError(type(response) + " is not supported.")

    def start(self):
        self.app.run(
            host="0.0.0.0",
            port=3000,
            debug=True,
            use_reloader=False,
            ssl_context="adhoc",
        )
