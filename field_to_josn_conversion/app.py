from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
     return render_template('testing.html')

@app.route('/display', methods=["GET", "POST"])
def display():
     return jsonify(request.form)

if __name__ == "__main__":
     app.run(host='0.0.0.0')
