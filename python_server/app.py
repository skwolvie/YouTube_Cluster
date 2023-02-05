from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('app.html')

@app.route('/preview')
def preview():
    return render_template('preview.html')

if __name__ == '__main__':
    app.run(debug=True)
