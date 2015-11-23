#!/usr/bin/env python
import numpy as np
import cv2
import sys
import matplotlib.pyplot as plt
from os import listdir, path
import utility as util
from block_dwt import video_blockdwt
from block_dct import FindDiscreteCosineTransform
from block_quantize import quantize
from diff_quantize import diff_quantize
from frame_dwt import video_framedwt 

def aggregate_features(features_per_frame, feature):
    if 'block_coords' in feature:
        features_per_frame[feature['frame_num'] - 1][(feature['block_coords'], feature['key'])] = feature['val']
    else:
        features_per_frame[feature['frame_num'] - 1][feature['key']] = feature['val']

    return features_per_frame

def indexes_of_closest_matches(target_features, features_per_frame):
    def score_feature(feature):
        score = 0.0
        for key in target_features:
            if key in feature:
                score += abs(target_features[key] - feature[key])
            else:
                score += abs(target_features[key])

        for key in feature:
            if key not in target_features:
                score += abs(feature[key])

        return score

    scores = map(score_feature, features_per_frame)
    closest_matches = [i[0] for i in sorted(enumerate(scores), key=lambda x:x[1])]
    return closest_matches

def show_ten_closest(frame_data, feature_summary, frame_num):
    # Reduce feature_summary to list of one dictionary per frame
    # Where each dictionary has (block_id, key) as the keys and val
    # as the value
    features_list = [{} for i in range(len(frame_data))]
    features_per_frame = reduce(aggregate_features, feature_summary, features_list)
    target_features = features_per_frame[frame_num - 1]
    closest_matches = indexes_of_closest_matches(target_features, features_per_frame)
    for i in range(1,11):
        index = closest_matches[i]
        rgb_target = cv2.cvtColor(frame_data[index].astype(np.uint8), cv2.COLOR_GRAY2BGR)
        print i
        cv2.imshow(str(i), rgb_target)
        cv2.waitKey(0)

    cv2.destroyAllWindows()
    return


if __name__ == '__main__':
    if len(sys.argv) == 1:
        root_dir = util.safeGetDirectory()
        all_files = [f for f in listdir(root_dir) if path.isfile(path.join(root_dir, f))]
        input_file = util.getVideoFile(all_files)
        f = util.getConstant('the frame number')
        n = util.getConstant('n (for block-level quantization)')
        m = util.getConstant('m (for frame-level dwt)')
        filename = path.join(root_dir, input_file)
    elif len(sys.argv) == 5:
        f = int(sys.argv[1])
        n = int(sys.argv[2])
        m = int(sys.argv[3])
        filename = path.realpath(sys.argv[4])
    else:
        print 'Usage: python match_frame.py <f> <n> <m> <../path/to/file.mp4>'
        exit()

    # Read the video data
    video = cv2.VideoCapture(filename)
    frame_data = util.getContent(video)

    target_frame_data = frame_data[f-1]
    rgb_target = cv2.cvtColor(target_frame_data.astype(np.uint8), cv2.COLOR_GRAY2BGR)
    cv2.imshow('Original frame', rgb_target)
    cv2.waitKey(0)

    block_quantized = quantize(frame_data, n)
    show_ten_closest(frame_data, block_quantized, f)

    block_dct = FindDiscreteCosineTransform(frame_data, n)
    show_ten_closest(frame_data, block_dct, f)

    block_dwt = video_blockdwt(frame_data, n)
    show_ten_closest(frame_data, block_dwt, f)

    block_diff_quantized = diff_quantize(frame_data, n)
    show_ten_closest(frame_data, block_diff_quantized, f)

    frame_dwt = video_framedwt(frame_data, m)
    show_ten_closest(frame_data, frame_dwt, f)
    print "all done!"
