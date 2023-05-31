from flask import Flask, render_template

app = Flask(__name__, template_folder='template', static_folder='static')

@app.route('/')
def platfomr():
    return render_template('register.html')

if __name__ == '__main__':
    app.run()
