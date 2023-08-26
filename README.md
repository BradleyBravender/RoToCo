# RoToCo
RoToCo, or the ROS Topic Comparison tool, is a simple script I made to compare the accuracy of one ROS topic to another. It was specifically designed to compare odometry data in the lab I interned in, so it would need a little reworking to compare other ROS Topics.

## A Basic Overview of rotoco.py
Our objective for this script in the lab was to determine the accuracy of the ROS odometry topic ```/odom``` when the Clearpath Jackal robot ran the [FLOAM](https://github.com/wh200720041/floam) SLAM algorithm. In that regard, we determined that the best approach was to launch FLOAM alongside the vicon_tracker ROS package inside the lab, and then record the odometry topics for both ```/odom``` for FLOAM and ```/vicon/Jackal/Jackal``` for vicon_tracker. Because of the accuracy of vicon_tracker, it was selected as the reference in which to compare the /odom topic to.

## How it Works
Once you've saved your ROS bag file, run this script in the same directory (or modify the path it searches for). This script first opens the bag file converts both odometry's quaternion coordinates to euler coordinates. We were only interested in the x, y, and yaw movements for this test as those are the only movements the Jackal can control its translation in.

Because the timestamps were different for both odometries, we needed to use one's timestamp as the 'official' timestamp and then interpolate the other's timestamp so that both were mapped on identical stamps.
The vicon_tracker recorded data at a significantly higher frequency than FLOAM. To preserve the integrity of the data (i.e. to remove excess existing data points intead of to generate excess non-existing data points), I decided to interpolate the vicon's odometry on the FLOAM's timestamp, thereby transforming the vicon's x, y, and yaw lists to inherit the same shape and timestamps that the corresponding FLOAM lists had.

Lastly, I created a function called ```error``` that took two arguments: a FLOAM list and a corresponding vicon list, and returned the abolute and maximum error from the FLOAM list as the experiemental dataset and the vicon_tracker as the reference data set.

## A Side Note
I've also added grapher.py in the source folder, which graphed the FLOAM's x, y, and z translation and x, y, z, and w rotation odometry data against vicon_tracker's.
