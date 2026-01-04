from flask import Flask, Response
from datetime import datetime

app = Flask(__name__)

@app.get("/date")
def date_endpoint():
    now = datetime.now()
    stamp = now.strftime("%H:%M:%S")
    label = "EVEN" if now.second % 2 == 0 else "ODD"
    return Response(f"{stamp} {label}\n", mimetype="text/plain")

@app.get("/")
def root():
    return "OK\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
