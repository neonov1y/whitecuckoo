from flask import Flask, render_template, request
from werkzeug import secure_filename
import json
import subprocess
import functions

app = Flask(__name__)


@app.route('/')
def index():
    # Open MySQL connection

    functions.mysql_create_connection()

    # Get information about program

    data = functions.size_db()
    cuckoo_status = functions.cuckoo_status()

    # Close MySQL connection

    functions.mysql_close_connection()

    return render_template('index.html', data_connections_number=data[0], files_number=data[1],
                           file_actions_number=data[2], connections_number=data[3], process_number=data[4],
                           registry_actions_number=data[5], cuckoo_status=cuckoo_status)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # Save the uploaded file in the directory to uploads

    f = request.files['fil']
    f.save('uploads/' + secure_filename(f.filename))

    # Open MySQL connection

    functions.mysql_create_connection()

    # Check the uploaded report

    data = functions.check_report("uploads/", secure_filename(f.filename))

    # Delete uploaded file from host

    subprocess.call(["rm", "uploads/" + secure_filename(f.filename)])

    # Close MySQL connection

    functions.mysql_close_connection()

    return json.dumps(data)


if __name__ == '__main__':
    app.run(debug=True)
