import os.path
import sys
subfolder = os.getcwd().split('Behavior-tools')[0]
sys.path.append(subfolder)
# add parent directory: (where nnet & config are!)
sys.path.append(subfolder + "/pose-tensorflow/")
sys.path.append(subfolder + "/Generating_a_Training_Set")
from myconfig_analysis import videofolder, cropping, Task, date, \
    resnet, shuffle, trainingsiterations, pcutoff, deleteindividualframes, x1, x2, y1, y2, videotype, alphavalue, dotsize, colormap
import pandas as pd
import numpy as np
from tqdm import tqdm
import collections
import imageio
from BehaviorAnalyst import BehaviorAnalyst

# Test
from PIL import Image, ImageDraw, ImageFont

X = BehaviorAnalyst()

MARKER_CUTOFF = 5

def test(Dataframe):

    state_collector = collections.defaultdict(dict)

    ''' Creating individual frames with labeled body parts and making a video''' 
    scorer=np.unique(Dataframe.columns.get_level_values(0))[0]
    bodyparts2plot = list(np.unique(Dataframe.columns.get_level_values(1)))

    nframes = len(Dataframe.index)

    for index in tqdm(range(nframes)):

        frame_name = Dataframe.index[index]

        for main_bpindex, main_bp in enumerate(bodyparts2plot):
            for factor_bpindex, factor_bp in enumerate(bodyparts2plot):
                if (
                    (main_bp[-5:] not in factor_bp) and \
                    (factor_bp + " VS " + main_bp not in state_collector.keys()) and \
                    (frame_name not in state_collector[main_bp + " VS " + factor_bp].keys()) \
                    ):
                    xA = Dataframe[scorer][main_bp]['x'].values[index]
                    yA = Dataframe[scorer][main_bp]['y'].values[index]
                    xB = Dataframe[scorer][factor_bp]['x'].values[index]
                    yB = Dataframe[scorer][factor_bp]['y'].values[index]
                    if (((xA >= MARKER_CUTOFF) or (yA >= MARKER_CUTOFF)) and ((xB >= MARKER_CUTOFF) or (yB >= MARKER_CUTOFF))):
                        point_A = [[xA, yA]]
                        point_B = [[xB, yB]]
                        heat_prob, fac = X.analyzeHeatProbOnFrame(point_A, point_B)
                        if index != 0:
                            recent_cs = state_collector[main_bp + " VS " + factor_bp][Dataframe.index[index - 1]]['cs']
                            current_cs = recent_cs + fac
                        else:
                            current_cs = fac
                    else:
                        if index != 0:
                            heat_prob = state_collector[main_bp + " VS " + factor_bp][Dataframe.index[index - 1]]['heat_prob']
                            if heat_prob:
                                current_cs = state_collector[main_bp + " VS " + factor_bp][Dataframe.index[index - 1]]['cs'] + 1
                            else:
                                current_cs = state_collector[main_bp + " VS " + factor_bp][Dataframe.index[index - 1]]['cs']
                        else:
                            heat_prob = False
                            current_cs = 0

                    if current_cs < 0:
                        current_cs = 0

                    state = {
                        "heat_prob": heat_prob,
                        "cs": current_cs
                    }

                    state_collector[main_bp + " VS " + factor_bp][frame_name] = state
    
    return state_collector

Dataframe = pd.read_hdf("../temp/train_10fr_500/CollectedData_Sky.h5")
a = dict(test(Dataframe))

# ------
font = ImageFont.truetype("arial.ttf", size=25)
color = 'rgb(255, 0, 0)'
nframes = len(Dataframe.index)
for index in tqdm(range(nframes)):

    (x, y) = (20, 10)

    frame_name = Dataframe.index[index]
    image = Image.open(frame_name)
    draw = ImageDraw.Draw(image)

    for pare in a:
        cs = a[pare][frame_name]['cs']
        if cs > 5:
            cows = pare.split(" VS ")
            message = "Heat Occurrence: "
            if ("Nose" in cows[0]):
                message = message + "Cow" + cows[0][len(cows[0]) - 1] + " "
            if ("Nose" in cows[1]):
                message = message + "Cow" + cows[1][len(cows[1]) - 1] + " "
            draw.text((x, y), message, fill=color, font=font)
            y -= 30

    image.save('cow_all10_heat/' + frame_name.split('/')[1])
# ------
# count = 1
# for pare in a:
#     print("-------->", pare, count)
#     count += 1
#     for frame in a[pare]:
#         if a[pare][frame]['cs'] >= 5:
#             print("=======>", frame, "Count State:", a[pare][frame]['cs'])
