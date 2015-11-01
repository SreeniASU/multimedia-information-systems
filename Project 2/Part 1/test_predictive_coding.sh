#!/usr/bin/env bash

python predictive_coding.py data/2.mp4 70 70 1
diff 2_1.tpc data/2_1.tpc 2>&1 > data/2_1.diff
length=$( grep -c . data/2_1.diff )
if [ $length -gt 0 ]
then
    cat data/2_1.diff
else
    echo "2_1 test passed!"
    rm data/2_1.diff
    rm 2_1.tpc
fi

python predictive_coding.py data/2.mp4 70 70 2
diff 2_2.tpc data/2_2.tpc 2>&1 > data/2_2.diff
length=$( grep -c . data/2_2.diff )
if [ $length -gt 0 ]
then
    cat data/2_2.diff
else
    echo "2_2 test passed!"
    rm data/2_2.diff
    rm 2_2.tpc
fi

python predictive_coding.py data/2.mp4 70 70 3
diff 2_3.tpc data/2_3.tpc 2>&1 > data/2_3.diff
length=$( grep -c . data/2_3.diff )
if [ $length -gt 0 ]
then
    cat data/2_3.diff
else
    echo "2_3 test passed!"
    rm data/2_3.diff
    rm 2_3.tpc
fi

python predictive_coding.py data/2.mp4 70 70 4
diff 2_4.tpc data/2_4.tpc 2>&1 > data/2_4.diff
length=$( grep -c . data/2_4.diff )
if [ $length -gt 0 ]
then
    cat data/2_4.diff
else
    echo "2_4 test passed!"
    rm data/2_4.diff
    rm 2_4.tpc
fi
