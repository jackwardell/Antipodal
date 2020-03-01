from flask import Flask, render_template

app = Flask(__name__)


class Config:
    name = "Wardell's Antipodal Namesake Coefficient"


@app.route('/')
def hello_world():
    return render_template(
        'index.html',
        config=Config
    )


if __name__ == '__main__':
    app.run()
