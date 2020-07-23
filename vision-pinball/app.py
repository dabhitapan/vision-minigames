from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)
import csv


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/sys_info.json")
def system_info():  # you need an endpoint on the server that returns your info...
    left_paddle = 0
    right_paddle = 0
    with open('C:/wrnchAI-engine-CPU-1.15.0-Windows-amd64/src/wrnchAI/wrSamples/python/data.csv', 'r',
              newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            # node_arr = []
            # for i in range(0, 12, 2):
            #     node_arr.append([float(row[i]), float(row[i + 1])])

            if row[1] < row[3]:
                left_paddle = 1
            if row[11] < row[9]:
                right_paddle = 1

    return str(left_paddle) + str(right_paddle)


if __name__ == '__main__':
    app.run()
