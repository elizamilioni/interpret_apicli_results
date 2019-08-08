import json
import sys
import os
import glob
import numpy as np
import matplotlib.pyplot as plt

PATH = "/home/liz/github_repos/api-cli/results_frame"

def interpret(direc, mode):
    pos = []
    eng = []
    val = []
    pol = []
    emotion =  np.zeros((8))
    ch = []
    tmp = 0
    i = 0
    for f in glob.glob(os.path.join(PATH, direc, "*.json")):
        with open(f) as json_file:
            data = json.load(json_file)
            for frame in data['frames']:
                if frame['speakers'] != None:
                    for sp in frame['speakers']:
                        if sp['valence'] != None and sp['politeness'] != None and mode == "means":
                            #print((frame['st'],sp['positivity']['framelevel'], sp['politeness']['framelevel']))
                            eng.append(sp['engagement']['framelevel'])
                            pol.append(sp['politeness']['framelevel'])
                            val.append(sp['valence']['framelevel'])
                            pos.append(sp['positivity']['framelevel'])
                        """ uppos = sp['positivity']['uptonow']
                            upeng = sp['engagement']['uptonow']
                            upval = sp['valence']['uptonow']
                            uppol = sp['politeness']['uptonow']"""
                        
                        if sp['emotion'] != None and mode == "emotion":
                            emotion[int(sp['emotion']['framelevel'])] += 1
                        
                        if sp['emotion'] != None and sp['valence']!=None and sp['politeness']!=None and mode == "changes":
                            ch.append((frame['st'], sp['emotion']['framelevel'], sp['positivity']['framelevel'], sp['politeness']['framelevel'], 
                                        sp['engagement']['framelevel'], sp['valence']['framelevel']))
                            if tmp != sp['emotion']['framelevel'] and i!=0 and mode == "changes" and set(ch[i-1][2:]) != set(ch[i][2:]):
                                print(ch[i-1], ch[i])
                            tmp = sp['emotion']['framelevel']
                            i += 1
                            
    if mode == "emotion":
        s = np.sum(emotion)
        print("emotion: happy, neutral, angry, sad, ambiguous, none")
        print(emotion[1]/s, emotion[2]/s, emotion[3]/s, emotion[4]/s, emotion[6]/s, emotion[7]/s)
    if mode == "means":
        print("means framelevel: positivity, engagement, valence, politeness")
        print(np.mean(pos), np.mean(eng), np.mean(val), np.mean(pol))

if __name__ == "__main__":
    print("modes: 1) means, 2) emotion 3) changes")
    interpret(sys.argv[1], sys.argv[2])
