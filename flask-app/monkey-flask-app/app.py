from flask import Flask, render_template
import random
app = Flask(__name__)

# List of cat images
images = [
    "https://media.giphy.com/media/tmQrpA8zpG4a16SSxm/giphy.gif",
    "https://media.giphy.com/media/5Zesu5VPNGJlm/giphy.gif",
    "https://media.giphy.com/media/dchERAZ73GvOE/giphy.gif",
    "https://media.giphy.com/media/73vsXqHC22yuA/giphy.gif",
    "https://media.giphy.com/media/3o6EhU7SUa3afFIJFe/giphy.gif",
    "https://media.giphy.com/media/qixJFUXq1UNLa/giphy.gif",
    "https://media.giphy.com/media/QOcpXsHPGpvax1E6FH/giphy.gif",
    "https://media.giphy.com/media/12oyZr7VXoTn68/giphy.gif",
    "https://media.giphy.com/media/XhvC8izkjCUg0/giphy.gif",
    "https://media.giphy.com/media/TgCDUdwJQJlgeRRtD6/giphy.gif",
    "https://media.giphy.com/media/tKLx8kC5EbFOU/giphy.gif"
]
@app.route('/')
def index():
    url = random.choice(images)
    return render_template('index.html', url=url)

if __name__ == "__main__":
    app.run(host="0.0.0.0")