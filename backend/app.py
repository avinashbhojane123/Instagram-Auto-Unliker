# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from instagrapi import Client
# import threading
# import time

# app = Flask(__name__)
# CORS(app)

# cl = Client()
# is_running = False
# unliker_thread = None
# log_messages = []
# unliked_count = 0  # ✅ Add this line for the counter

# # Logging helper
# def log(msg):
#     print(msg)
#     log_messages.append(msg)
#     if len(log_messages) > 100:
#         log_messages.pop(0)

# def auto_unlike(username, password, unlike_delay=1, recheck_delay=10):
#     global is_running, unliked_count
#     unliked_count = 0  # ✅ Reset counter at start
#     try:
#         cl.login(username, password)
#         log("✅ Logged in successfully.")

#         while is_running:
#             log("🔄 Fetching liked posts...")
#             try:
#                 liked_medias = cl.private_request("feed/liked/", params={"count": 3000})["items"]
#             except Exception as e:
#                 log(f"❌ Failed to fetch liked posts: {e}")
#                 break

#             if not liked_medias:
#                 log("✅ No liked posts found. Rechecking later...")
#                 time.sleep(recheck_delay)
#                 continue

#             log(f"👍 Found {len(liked_medias)} liked posts.")
#             for media in liked_medias:
#                 if not is_running:
#                     break
#                 try:
#                     cl.media_unlike(media["id"])
#                     unliked_count += 1  # ✅ Increment counter
#                     log(f"❌ Unliked post ID: {media['id']}")
#                     time.sleep(unlike_delay)
#                 except Exception as e:
#                     log(f"⚠️ Failed to unlike post ID {media['id']}: {e}")
#             time.sleep(recheck_delay)

#     except Exception as e:
#         log(f"❌ Login failed: {e}")
#     finally:
#         is_running = False
#         log("🛑 Auto Unliker stopped.")

# @app.route('/start', methods=['POST'])
# def start():
#     global is_running, unliker_thread
#     if is_running:
#         return jsonify({"message": "Already running."}), 400

#     data = request.json
#     username = data.get("username")
#     password = data.get("password")
#     unlike_delay = data.get("unlikeDelay", 1)
#     recheck_delay = data.get("recheckDelay", 10)

#     is_running = True
#     unliker_thread = threading.Thread(target=auto_unlike, args=(username, password, unlike_delay, recheck_delay))
#     unliker_thread.start()

#     return jsonify({"message": "Started Auto Unliker."})

# @app.route('/stop', methods=['POST'])
# def stop():
#     global is_running
#     is_running = False
#     return jsonify({"message": "Stopped Auto Unliker."})

# @app.route('/logs', methods=['GET'])
# def get_logs():
#     return jsonify({
#         "logs": log_messages,
#         "unliked_count": unliked_count  # ✅ Include counter in response
#     })

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time

app = Flask(__name__)
CORS(app)

is_running = False
unliker_thread = None
log_messages = []
unliked_count = 0

def log(msg):
    print(msg)
    log_messages.append(msg)
    if len(log_messages) > 100:
        log_messages.pop(0)

@app.route("/")
def home():
    return jsonify({
        "status": "running",
        "service": "Instagram Auto Unliker"
    })

@app.route("/healthz")
def healthz():
    return jsonify({"status": "ok"}), 200

def auto_unlike(username, password, unlike_delay=1, recheck_delay=10):
    global is_running, unliked_count

    try:
        # Import here instead of globally
        from instagrapi import Client

        cl = Client()
        unliked_count = 0

        cl.login(username, password)
        log("✅ Logged in successfully.")

        while is_running:
            log("🔄 Fetching liked posts...")

            try:
                liked_medias = cl.private_request(
                    "feed/liked/",
                    params={"count": 3000}
                )["items"]
            except Exception as e:
                log(f"❌ Failed to fetch liked posts: {e}")
                break

            if not liked_medias:
                log("✅ No liked posts found. Rechecking later...")
                time.sleep(recheck_delay)
                continue

            log(f"👍 Found {len(liked_medias)} liked posts.")

            for media in liked_medias:
                if not is_running:
                    break

                try:
                    cl.media_unlike(media["id"])
                    unliked_count += 1
                    log(f"❌ Unliked post ID: {media['id']}")
                    time.sleep(unlike_delay)

                except Exception as e:
                    log(f"⚠️ Failed to unlike post ID {media['id']}: {e}")

            time.sleep(recheck_delay)

    except Exception as e:
        log(f"❌ Login failed: {e}")

    finally:
        is_running = False
        log("🛑 Auto Unliker stopped.")

@app.route('/start', methods=['POST'])
def start():
    global is_running, unliker_thread

    if is_running:
        return jsonify({"message": "Already running"}), 400

    data = request.json

    username = data.get("username")
    password = data.get("password")
    unlike_delay = data.get("unlikeDelay", 1)
    recheck_delay = data.get("recheckDelay", 10)

    is_running = True

    unliker_thread = threading.Thread(
        target=auto_unlike,
        args=(username, password, unlike_delay, recheck_delay)
    )

    unliker_thread.daemon = True
    unliker_thread.start()

    return jsonify({"message": "Started Auto Unliker"})

@app.route('/stop', methods=['POST'])
def stop():
    global is_running

    is_running = False

    return jsonify({
        "message": "Stopped Auto Unliker"
    })

@app.route('/logs', methods=['GET'])
def get_logs():
    return jsonify({
        "logs": log_messages,
        "unliked_count": unliked_count
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
