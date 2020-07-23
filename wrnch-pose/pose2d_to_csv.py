# Copyright (c) 2019 wrnch Inc.
# All rights reserved

from __future__ import print_function, division

import cv2
import wrnchAI
from visualizer import Visualizer
from utils import videocapture_context
import csv
import os

params = wrnchAI.PoseParams()
params.bone_sensitivity = wrnchAI.Sensitivity.high
params.joint_sensitivity = wrnchAI.Sensitivity.high
params.enable_tracking = True

# Default Model resolution
params.preferred_net_width = 328
params.preferred_net_height = 184

output_format = wrnchAI.JointDefinitionRegistry.get('j23')

estimator = wrnchAI.PoseEstimator(models_path=os.environ['MODEL_PATH'],
                                  license_string=os.environ['LISCENSE_KEY'],
                                  params=params,
                                  gpu_id=0,
                                  output_format=output_format)
options = wrnchAI.PoseEstimatorOptions()
joint_definition = estimator.human_2d_output_format()
bone_pairs = joint_definition.bone_pairs()


def main():
    print('Opening webcam...')
    with videocapture_context(0) as cap:
        visualizer = Visualizer()

        while True:
            _, frame = cap.read()

            if frame is not None:
                estimator.process_frame(frame, options)
                humans2d = estimator.humans_2d()
                if humans2d:
                    human = humans2d[0]
                    visualizer.draw_image(frame)
                    joints = human.joints()
                    with open('data.csv', 'w', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(joints[20:32].tolist())
                    visualizer.draw_points(joints[20:32])
                    visualizer.draw_lines(joints, bone_pairs)

                    visualizer.show()

            key = cv2.waitKey(1)

            if key & 255 == 27:
                break


if __name__ == '__main__':
    main()
