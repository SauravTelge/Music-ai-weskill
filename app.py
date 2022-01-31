from flask import Flask, render_template, request,Response
import crepe
from scipy.io import wavfile
from numpy import asarray
from numpy import savetxt
from numpy import loadtxt
import datetime
# import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from google.cloud import storage
# Plotting Packages
# import matplotlib.pyplot as plt
# import seaborn as sbn
# # Configuring Matplotlib
# import matplotlib as mpl
# from google.cloud import storage
# from rq import Queue
# from rq.job import Job
# from worker import conn

# Computation packages
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
import os
# from score import Score
from numpy import loadtxt
# import numpy as np
# from scipy import spatial


# from dtaidistance import dtw
# from dtaidistance import dtw_visualisation as dtwvis


# mpl.rcParams['figure.dpi'] = 300
# savefig_options = dict(format="png", dpi=300, bbox_inches="tight")

# q = Queue(connection=conn)
app = Flask(__name__)
app.config['GOOGLE_APPLICATION_CREDENTIALS']= 'gcs.json'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = app.config['GOOGLE_APPLICATION_CREDENTIALS']

# config = {
#   "apiKey": "AIzaSyC-te8CQAw8M2mMOrlt9Hnfmf2D_p7Ija8",
#   "authDomain": "letsdance-c6c04.firebaseapp.com",
#   "databaseURL": "https://letsdance-c6c04-default-rtdb.firebaseio.com",
#   "storageBucket": "letsdance-c6c04.appspot.com",
#   "serviceAccount": "fireb.json"
# }


def cors_configuration(bucket_name):
    """Set a bucket's CORS policies configuration."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    bucket.cors = [
        {
            "origin": ["*"],
            "responseHeader": [
                "Content-Type",
                "x-goog-resumable"],
            "method": ['PUT', 'POST'],
            "maxAgeSeconds": 3600
        }
    ]
    bucket.patch()
    print("Set CORS policies for bucket {} is {}".format(bucket.name, bucket.cors))
    return bucket
bucket = cors_configuration("ws-dance-ai")

# Enter path of both audio files
#



@app.route("/")  
def home():
    return render_template("choreo.html")

@app.route('/getSignedURL')
def getSignedURL():
    print("hi1")
    bucket_name = "ws-dance-ai" 
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    filename = request.args.get('filename')
    action = request.args.get('action')
    blob = bucket.blob(filename)
    print("hi2")
    url = blob.generate_signed_url(
        expiration=datetime.timedelta(minutes=60),
        method=action, version="v4")
    print("hi3")
    return url

@app.route("/output",methods=["GET", "POST"])
def output():
    if request.method == "POST":
        fl = request.form["filename"]
        name = request.form["name"]
        bucket_name = "ws-dance-ai" 
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
    # Upload file to Google Bucket
        blob = bucket.blob(f'{fl}') 
        blob.download_to_filename(f'/tmp/{fl}')
        sr2, audio2 = wavfile.read(f"/tmp/{fl}")
        time2, frequency2, confidence2, activation2 = crepe.predict(audio2, sr2, viterbi=True)
        data_2_time = asarray(time2)
        # save to csv file
        savetxt('tutor_time_test.csv', data_2_time, delimiter=',')

        data_2_freq = asarray(frequency2)
        # save to csv file
        savetxt('tutor_freq_test.csv', data_2_freq, delimiter=',')
        # genre = request.form["genre"]
        # poses = request.form["pose"]
       
    # video1(fl)  
    # job=q.enqueue(video1,fl,poses,job_timeout=1500)
    # dir = fl
    # fl=dir.rsplit('.', 1)[0]
    # print(fl) 
    
    return render_template("output.html")


if __name__ == "__main__":
    app.run()