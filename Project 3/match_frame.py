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
    # Reduce function that takes a feature and places it in the correct
    # Frame in the features_per_frame list
    if 'block_coords' in feature:
        features_per_frame[feature['frame_num'] - 1][(feature['block_coords'], feature['key'])] = feature['val']
    else:
        features_per_frame[feature['frame_num'] - 1][feature['key']] = feature['val']

    return features_per_frame

def indexes_of_closest_matches(target_features, features_per_frame):
    def score_feature(feature):
        # Could be an integer or float
        score = 0.0
        for key in target_features:
            if key in feature:
                # Add up all of the absolute values when both frames
                # have a similar key
                score += abs(target_features[key] - feature[key])
            else:
                # If this frame doesn't have that key, just add the
                # absolute value to the sum
                score += abs(target_features[key])

        for key in feature:
            if key not in target_features:
                # Also add any keys that the frame has and the target
                # doesn't have
                score += abs(feature[key])

        return score

    # Take all of the frames, and for each one apply the score_feature function,
    # which adds up all of the differences in the values in similar keys
    scores = map(score_feature, features_per_frame)
    closest_match_indexes = [i[0] for i in sorted(enumerate(scores), key=lambda x:x[1])]
    sorted_scores = sorted(scores)
    return closest_match_indexes, sorted_scores

def show_ten_closest(frame_data, feature_summary, frame_num, description):
    # List of dictionaries - has length of the number of frames, which we will fill
    features_list = [{} for i in range(len(frame_data))]
    # Turn our feature_summary into a more useful list, that has one entry
    # per frame, each entry being a dictionary of keys and values. In most cases
    # the key is a tuple of block index and one other value, which is a wavelet id
    # or quanta depending on which part you're using. The nice thing is that this code
    # works in either case
    features_per_frame = reduce(aggregate_features, feature_summary, features_list)
    # Grab the frame we're interested in:
    target_features = features_per_frame[frame_num - 1]
    # Get the frame numbers of the most similar frames
    closest_match_indexes, sorted_scores = indexes_of_closest_matches(target_features, features_per_frame)
    for i in range(1,11):
        # For each of those frame numbers, display the image in a window with the number
        index = closest_match_indexes[i]
        score = sorted_scores[i]
        rgb_target = cv2.cvtColor(frame_data[index].astype(np.uint8), cv2.COLOR_GRAY2BGR)
        frame_description = description + ' #' + str(i) + ': frame ' + str(index + 1) + '. Score: ' + str(score)
        print frame_description
        cv2.imshow(frame_description, rgb_target)
        cv2.waitKey(0)

    cv2.destroyAllWindows()
    return

def show_ten_quantized_closest(frame_data,frame_block_dict,target_frame_number, description ):
    target_frame_block_hist_dict = frame_block_dict[target_frame_number-1]
    top_ten_frames = list()

    print("Comparing frames...")
    for keyA in frame_block_dict:
        if keyA == target_frame_number-1:  #dont compare the frame against itself
            continue
        else:
            frame_score = float(0)
            for keyB in frame_block_dict[keyA]:
                block_hist = frame_block_dict[keyA][keyB[0],keyB[1]]
                frame_score += cv2.compareHist(target_frame_block_hist_dict[keyB[0],keyB[1]],block_hist, 0) #Correlation compare

        top_ten_frames.append((keyA, frame_score))

    top_ten_frames.sort(key=lambda tup: tup[1])  # sorts in place
    top_ten_frames.reverse()

    top_ten_frame_indexes = list((x[0] for x in top_ten_frames))    #just need to the frame number, not the diff so we strip that out
    top_ten_frame_values = list((x[1] for x in top_ten_frames))
    for i in range(0,10):
        # For each of those frame numbers, display the image in a window with the number
        index = top_ten_frame_indexes[i]
        score = top_ten_frame_values[i]
        print frame_data[index - 1]
        rgb_target = cv2.cvtColor(frame_data[index-1].astype(np.uint8), cv2.COLOR_GRAY2BGR)
        frame_description = description + ' #' + str(i + 1) + ': frame ' + str(index) + '. Score: ' + str(score)
        print frame_description
        cv2.imshow(frame_description, rgb_target)
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
    cv2.imshow('Original frame: ' + str(f), rgb_target)
    print 'Displaying Original frame - press any key to continue :)'
    cv2.waitKey(0)

    block_quantized, frame_block_dict = quantize(frame_data, n)
    block_quantized = None #free memory for this, returned from argument but not applicable here
    show_ten_quantized_closest(frame_data, frame_block_dict, f, 'Quantization')

    block_dct = FindDiscreteCosineTransform(frame_data, n)
    show_ten_closest(frame_data, block_dct, f, 'DCT')

    block_dwt = video_blockdwt(frame_data, n)
    show_ten_closest(frame_data, block_dwt, f, 'Block-level DWT')

    block_diff_quantized, frame_block_dict = diff_quantize(frame_data, n)
    show_ten_quantized_closest(frame_data, frame_block_dict, f, 'Diff Quantization')

    frame_dwt = video_framedwt(frame_data, m)
    show_ten_closest(frame_data, frame_dwt, f, 'Frame-level DWT')
    print "All done!"
