from flask import Flask, render_template
import random
app = Flask(__name__)

# List of cat images
images = ["https://randomfox.ca/images/"+str(i)+".jpg" for i in range(1, 121)]

@app.route('/')
def index():
    url = random.choice(images)
    return render_template('index.html', url=url)

if __name__ == "__main__":
    app.run(host="0.0.0.0")