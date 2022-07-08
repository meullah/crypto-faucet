import tx
import queue
import requests
import threading
from web3 import Web3
from flask import Flask, request, render_template

adapter = requests.adapters.HTTPAdapter(pool_connections=20, pool_maxsize=20)
session = requests.Session()
session.mount('http://', adapter)
session.mount('https://', adapter)
w3 = Web3(Web3.HTTPProvider("https://seed84.xyz", session=session))

q = queue.Queue()
recent_tx = []


def worker():
    global recent_tx
    while True:
        receiver_address = q.get()
        res = tx.sendTransaction(w3, receiver_address)
        if len(recent_tx) < 5:
            recent_tx = [res] + recent_tx
        else:
            recent_tx[1:] = recent_tx[:-1]
            recent_tx[0] = res
        q.task_done()


threading.Thread(target=worker, daemon=True).start()

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def getWalletAddress():
    if request.method == "POST":
        # getting input with name = walletAddress in HTML form
        to_address = request.form.get("walletAddress")
        q.put(to_address)
        return render_template("index.html", transactions=recent_tx)
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
