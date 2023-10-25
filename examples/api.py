from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_json():
    try:
        data = request.get_json()
        if data is not None or "session_id" not in data or "user_task" not in data:
            user_task = data["user_task"]
            session_id = data.pop("session_id")
            response_data = init_and_process(session_id,user_task,data)
            return jsonify(response_data)
        else:
            return jsonify({'error': 'Invalid JSON input'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


SOME_DB = dict()
THREADS = dict()
def init_agent(user_task,session_id):
    from scrape_anything import Agent
    from scrape_anything import ChatLLM
    from scrape_anything import RemoteFeedController
    from queue import Queue

    feed_from_chrome = Queue(maxsize=1)
    feed_from_agent = Queue(maxsize=1)

    controller = RemoteFeedController(
        incoming_data_queue=feed_from_chrome,
        outgoing_data_queue=feed_from_agent,
        user_task=user_task,
        ) 
    agnet = Agent(llm=ChatLLM(),max_loops=1)
    THREADS[session_id] = agnet.run_parallel(controller)
    SOME_DB[session_id] = (feed_from_chrome,feed_from_agent)

def process_request(data,session_id):
    from scrape_anything import OutGoingData,IncommingData
    import json

    (feed_from_chrome,feed_from_agent) = SOME_DB[session_id]
    feed_from_chrome.put(IncommingData(url=data['url'],
                                       task=data['user_task'],
                                       viewpointscroll=data['viewpointscroll'],
                                       viewportHeight=data['viewportHeight'],
                                       scroll_width=data['width'],
                                       scroll_height=data['width'],
                                       width=data['width'],
                                       height=data['height'],
                                       raw_on_screen=data['raw_on_screen']))
    response:OutGoingData = feed_from_agent.get()
    return json.dumps(response)


def init_and_process(session_id,user_task,params):
    if session_id not in SOME_DB:
        init_agent(user_task,session_id)
    return process_request(params,session_id)
    

def start_server():
    try:
        threading.Thread(target=lambda: app.run(host="scrape_anything", port=3000, debug=True, use_reloader=False)).start()
    finally:
        for t in THREADS.values():
            t.stop()

if __name__ == '__main__':
    start_server()