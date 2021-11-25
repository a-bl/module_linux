from flask import Flask, render_template
import random
app = Flask(__name__)

# List of cat images
images = [
    "https://media.giphy.com/media/JhUZYdpnqrgcM/giphy.gif",
    "https://media.giphy.com/media/XAy4bUZMEMieyLIQ1C/giphy.gif",
    "https://media.giphy.com/media/KtKi9n1k5h5bW/giphy.gif",
    "https://media.giphy.com/media/FiKrAB6rT9Oms/giphy.gif",
    "https://media.giphy.com/media/Ter8NaRzBVjGGk6MRS/giphy.gif",
    "https://media.giphy.com/media/feoIvi3j0MxcFTazV8/giphy.gif",
    "https://media.giphy.com/media/tAVCppet3HpPa/giphy.gif",
    "https://media.giphy.com/media/If1XFiwkPe00QHCGZ4/giphy.gif"
]
@app.route('/')
def index():
    url = random.choice(images)
    return render_template('index.html', url=url)

if __name__ == "__main__":
    app.run(host="0.0.0.0")