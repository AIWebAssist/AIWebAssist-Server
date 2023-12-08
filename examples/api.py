from flask import Flask, request, jsonify
from multiprocessing import Process
from flask_cors import cross_origin

app = Flask(__name__)
DEV = False # TODO: remove patch

@app.route('/process', methods=['POST', 'OPTIONS'])
@cross_origin()
def process():
    if request.method == 'POST':
        return handle_process_request()
    elif request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response, 200

@app.route('/status', methods=['POST', 'OPTIONS'])
@cross_origin()
def status():
    if request.method == 'POST':
        return handle_status_request()
    elif request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response, 200
    

def handle_process_request():
    try:
        data = request.get_json()
        if data is not None or "session_id" not in data or "user_task" not in data:
            user_task = data["user_task"]
            session_id = str(data.pop("session_id"))
            return init_and_process(session_id,user_task,data,max_message=-1)
        else:
            return jsonify({'error': 'Invalid JSON input'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def handle_status_request():
    try:
        data = request.get_json()
        if data is not None or "session_id" not in data:
            session_id = str(data.pop("session_id"))
            return process_status(session_id,data)
        else:
            return jsonify({'error': 'Invalid JSON input'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

SOME_DB = dict()
THREADS = dict()
def init_agent(user_task,session_id,max_message=1):
    from scrape_anything import Agent
    from scrape_anything import TextOnlyLLM,VisionBaseLLM
    from scrape_anything import DevRemoteFeedController
    from queue import Queue

    feed_from_chrome = Queue(maxsize=1)
    feed_from_agent = Queue(maxsize=1)
    status_feed_queue = Queue(maxsize=1)

    controller = DevRemoteFeedController(
        incoming_data_queue=feed_from_chrome,
        outgoing_data_queue=feed_from_agent,
        status_queue=status_feed_queue,
        user_task=user_task,
        max_loops=max_message
    ) 
    agnet = Agent(llm=VisionBaseLLM(),max_loops=max_message)
    THREADS[session_id] = agnet.run_parallel(controller)
    SOME_DB[session_id] = (feed_from_chrome,feed_from_agent,status_feed_queue)

def clean_session(session_id):
    SOME_DB.pop(session_id)

def process_status(session_id,data):
    (_,_,status_queue) = SOME_DB[session_id]
    status = data['execution_status']
    status_queue.put(status)

    return jsonify({}), 200


def process_request(data,session_id):
    from scrape_anything import OutGoingData,IncommingData,Error

    (feed_from_chrome,feed_from_agent,_) = SOME_DB[session_id]
    feed_from_chrome.put(IncommingData(url=data['url'],
                                       task=data['user_task'],
                                       viewpointscroll=data['viewpointscroll'],
                                       viewportHeight=data['viewportHeight'],
                                       scroll_width=data['width'],
                                       scroll_height=data['width'],
                                       width=data['width'],
                                       height=data['height'],
                                       raw_on_screen=data['raw_on_screen'],
                                       screenshot= None if DEV else data['screenshot'])) # TODO: remove patch
    response:OutGoingData = feed_from_agent.get()
    if isinstance(response,Error) and (response.is_fatel or response.session_closed):
        clean_session(session_id)
        return jsonify(response.__dict__),500
    elif isinstance(response,OutGoingData):
        if response.session_closed:
            clean_session(session_id)
        return jsonify(response.__dict__),200
    else:
        raise ValueError(type(response)+" is not supported.")


def init_and_process(session_id,user_task,params,max_message=-1):
    if session_id not in SOME_DB:
        init_agent(user_task,session_id,max_message=max_message)
    return process_request(params,session_id)


def start_server(dev=True):
    global DEV 
    global SERVER_THREAD
    DEV = dev
    try:
        SERVER_THREAD = Process(target=app.run,kwargs={"host":"scrape_anything", "port":3000, "debug":True, "use_reloader":False,"ssl_context":"adhoc"})
        SERVER_THREAD.start()
    finally:
        for t in THREADS.values():
            t.stop()

def stop_server():
    SERVER_THREAD.terminate()
    SERVER_THREAD.join()

if __name__ == '__main__':
    start_server(dev=False)