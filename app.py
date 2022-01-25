from flask import Flask, render_template, request,Response
import crepe
from scipy.io import wavfile
from numpy import asarray
from numpy import savetxt
from numpy import loadtxt

import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
# Plotting Packages
import matplotlib.pyplot as plt
import seaborn as sbn
# Configuring Matplotlib
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 300
savefig_options = dict(format="png", dpi=300, bbox_inches="tight")
# Computation packages
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw

# from score import Score
from numpy import loadtxt
# import numpy as np
from scipy import spatial


from dtaidistance import dtw
from dtaidistance import dtw_visualisation as dtwvis


# Enter path of both audio files
#
path1 = r'./audio_files/audio_1_tutor_pal.wav'
path2 = r'./audio_files/audio_2_user_pal.wav'
#

class music():


    def __init__(self,p1,p2,o1_tut,o2_tut,o1_user,o2_user):
        self.p1=p1
        self.p2=p2
        self.o1_tut=o1_tut
        self.o2_tut=o2_tut
        self.o1_user=o1_user
        self.o2_user=o2_user



    def tutor(self):

        sr, audio = wavfile.read(self.p1)
        self.time, self.frequency, confidence, activation = crepe.predict(audio, sr, viterbi=True)
        print(self.time)
        print("#################")
        print(self.frequency)
        print("#################")


        # define data
        data_1_time = asarray(self.time)
        # save to csv file
        savetxt(self.o1_tut, data_1_time, delimiter=',')

        data_1_freq = asarray(self.frequency)
        # save to csv file
        savetxt(self.o2_tut, data_1_freq, delimiter=',')
#

    def user(self):
        sr2, audio2 = wavfile.read(self.p2)
        self.time2, self.frequency2, confidence2, activation2 = crepe.predict(audio2, sr2, viterbi=True)
        print(self.time2)
        print("#################")
        print(self.frequency2)
        print("#################")


        data_2_time = asarray(self.time2)
        # save to csv file
        savetxt(self.o1_user, data_2_time, delimiter=',')

        data_2_freq = asarray(self.frequency2)
        # save to csv file
        savetxt(self.o2_user, data_2_freq, delimiter=',')

    def plott(self):

        print(len(self.time))
        print(len(self.time2))
        # t2=time2-1
        f = plt.figure()
        f.set_figwidth(30)
        f.set_figheight(15)
        plt.plot(self.time, self.frequency)
        plt.plot(self.time2, self.frequency2)

        plt.legend(["tutor", "student"])
        # plotting
        plt.title("Frequency vs time")
        plt.xlabel("time")
        plt.ylabel("frequency")
        # plt.plot(x, y, color="red")
        plt.grid()
        plt.savefig(r"plots\frequency_plot")

        plt.show()


def normalization(pos_list):
    norm1 = pos_list / np.linalg.norm(pos_list)
    return (norm1)

def percentage_score(score):
    percentage =  100 - (score* 100)
    return int(percentage)

tut_f = loadtxt(r'./csv_files/tutor_freq_test.csv', delimiter=',')
tut_t = loadtxt(r'./csv_files/tutor_time_test.csv', delimiter=',')
user_f = loadtxt(r'./csv_files/user_freq_test.csv', delimiter=',')
user_t = loadtxt(r'./csv_files/user_time_test.csv' ,delimiter=',')


my_list=user_f
mynewlist1=np.array(tut_f)

my_list1 = np.array(my_list)

# print(min(my_list1),max(my_list1))
# print(min(mynewlist1),max(mynewlist1))
my_list=normalization(my_list1)
mynewlist=normalization(mynewlist1)

c2=dtw.distance(my_list, mynewlist, window=2)
print("distance",c2)


c3=percentage_score(c2)
print("Score",c3)

s1,s2=my_list, mynewlist

path = dtw.warping_path(s1, s2, window=2)
# print(path)
dtwvis.plot_warping(s1, s2, path, filename=r"plots\warp.png")



import moviepy.editor as mp

audio1 = mp.AudioFileClip(path1)
video1 = mp.VideoFileClip(r'output_animation\animation_1.mp4')    #     if you have run the jupyter notebook for animation chane the path
final = video1.set_audio(audio1)                                  #     to animation_2.mp4
final.write_videofile(r"output_animation\tutor_voiced_ani.mp4")

audio2 = mp.AudioFileClip(path2)
video2 = mp.VideoFileClip(r'output_animation\animation_1.mp4')
final2 = video2.set_audio(audio2)
final2.write_videofile(r"output_animation\user_voiced_ani.mp4")

app = Flask(__name__)

@app.route("/")  
def home():
    return render_template("choreo.html")

@app.route("/output")
def output():
    p1=path1
    p2=path2
    csv_audio_1_t=r'csv_files\tutor_time_test.csv'       ## Predefined names of csv files
    csv_audio_1_f=r'csv_files\tutor_freq_test.csv'
    csv_audio_2_t=r'csv_files\user_time_test.csv'
    csv_audio_2_f=r'csv_files\user_freq_test.csv'
    obj1=music(p1,p2,csv_audio_1_t,csv_audio_1_f,csv_audio_2_t,csv_audio_2_f)
    obj1.tutor()
    obj1.user()
    obj1.plott()
    # obj1.load()
    print("finish")
    return render_template("output.html",c3=c3)


if __name__ == "__main__":
    app.run()