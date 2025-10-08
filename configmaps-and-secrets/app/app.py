from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def index():
    # ConfigMap values (non-sensitive)
    app_message = os.getenv("APP_MESSAGE", "Hello from default value")
    db_user = os.getenv("DB_USER", "unknown-user")

    # Secret as env var
    db_pass_env = os.getenv("DB_PASSWORD", "<not-set>")

    # Secret as mounted file
    try:
        with open("/etc/db/password", "r") as f:
            db_pass_file = f.read().strip()
    except:
        db_pass_file = "<file-not-found>"

    return f"""
    <h2>🔧 ConfigMap & Secret Demo</h2>
    <ul>
      <li>APP_MESSAGE (ConfigMap env): {app_message}</li>
      <li>DB_USER (ConfigMap env): {db_user}</li>
      <li>DB_PASSWORD (Secret env): {db_pass_env[:3]}***</li>
      <li>DB_PASSWORD (Secret file): {db_pass_file[:3]}***</li>
    </ul>
    <p>Note: Env vars require pod restart to refresh; mounted files update automatically.</p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
