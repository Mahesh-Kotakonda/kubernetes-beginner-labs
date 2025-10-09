# app/src/server.py
from flask import Flask, request
import time, os, signal, threading, logging

app = Flask(__name__)

# state flags
is_ready = False
is_alive = True

# logging to file and stdout (so sidecar can tail file)
LOG_DIR = "/var/log/app"
LOG_FILE = os.path.join(LOG_DIR, "app.log")
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
fh = logging.FileHandler(LOG_FILE)
fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.addHandler(fh)
sh = logging.StreamHandler()
sh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.addHandler(sh)

def startup_sequence():
    global is_ready
    startup_sleep = int(os.getenv("STARTUP_SLEEP", "15"))
    logger.info(f"Startup sequence: sleeping {startup_sleep}s to simulate warmup")
    time.sleep(startup_sleep)
    is_ready = True
    logger.info("Startup complete -> is_ready = True")

@app.route("/")
def home():
    logger.info("GET /")
    return "Pod Lifecycle Demo", 200

@app.route("/startup")
def startup():
    return ("Startup OK", 200)

@app.route("/ready")
def ready():
    if is_ready:
        return ("Ready", 200)
    else:
        return ("Not Ready", 500)

@app.route("/healthz")
def healthz():
    if is_alive:
        return ("Healthy", 200)
    else:
        return ("Unhealthy", 500)

# Toggle endpoints for testing
@app.route("/toggle-ready", methods=["POST"])
def toggle_ready():
    global is_ready
    val = request.args.get("value", "")
    is_ready = val.lower() in ("1", "true", "t", "yes", "y")
    logger.info(f"toggle-ready -> {is_ready}")
    return ("OK", 200)

@app.route("/toggle-alive", methods=["POST"])
def toggle_alive():
    global is_alive
    val = request.args.get("value", "")
    is_alive = val.lower() in ("1", "true", "t", "yes", "y")
    logger.info(f"toggle-alive -> {is_alive}")
    return ("OK", 200)

@app.route("/crash", methods=["POST"])
def crash():
    logger.info("Crashing by request (exit 1)")
    os._exit(1)  # immediate crash for demo

def handle_sigterm(sig, frame):
    global is_ready, is_alive
    logger.info("SIGTERM received: marking not ready, running cleanup")
    is_ready = False
    # simulate cleanup
    time.sleep(5)
    is_alive = False
    logger.info("Cleanup complete, exiting.")
    os._exit(0)

signal.signal(signal.SIGTERM, handle_sigterm)

if __name__ == "__main__":
    threading.Thread(target=startup_sequence, daemon=True).start()
    app.run(host="0.0.0.0", port=8080)
