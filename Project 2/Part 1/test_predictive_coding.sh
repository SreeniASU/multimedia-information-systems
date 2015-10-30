#!/usr/bin/env bash

python predictive_coding.py data/2.mp4 70 70 1
diff 2_1.tpc data/2_1.tpc 2>&1 > data/2_1.diff
length = $(wc -l data/2_1.diff)
if [ $length -gt 0 ]
then
    cat data/2_1.diff
else
    echo "2_1 test passed!"
    rm data/2_1.diff
    rm 2_1.tpc
fi
