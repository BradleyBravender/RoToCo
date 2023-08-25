from tf.transformations import euler_from_quaternion
import pandas as pd
import rosbag

floam_time, floam_x, floam_y, floam_yaw = [], [], [], []
vicon_time, vicon_x, vicon_y, vicon_yaw = [], [], [], []

def main():

    # Open the rosbag file
    bag = rosbag.Bag('Test1.bag') # change this bag file name to your own
        
    # Iterate over all messages in the rosbag file
    for topic, msg, t in bag.read_messages(topics=['/odom', '/vicon/Jackal/Jackal']): # change topic names if yours are different
            if topic == '/odom':
                # Extract the position data
                x = msg.pose.pose.position.x
                y = msg.pose.pose.position.y
                z = msg.pose.pose.position.z
                
                # Extract the quaternion from the message
                quaternion = (
                    msg.pose.pose.orientation.x,
                    msg.pose.pose.orientation.y,
                    msg.pose.pose.orientation.z,
                    msg.pose.pose.orientation.w)
                
                # Convert the quaternion to Euler angles
                roll, pitch, yaw = euler_from_quaternion(quaternion)
                
                floam_time.append(t)
                floam_x.append(x)
                floam_y.append(y)
                floam_yaw.append(yaw)
            
            elif topic == '/vicon/Jackal/Jackal':
                #Extract the position data
                x = msg.transform.translation.x
                y = msg.transform.translation.y
                z = msg.transform.translation.z
            
                # Extract the quaternion from the message
                quaternion = (
                    msg.transform.rotation.x,
                    msg.transform.rotation.y,
                    msg.transform.rotation.z,
                    msg.transform.rotation.w)
            
                # Convert the quaternion to Euler angles
                roll, pitch, yaw = euler_from_quaternion(quaternion)
                
                vicon_time.append(t)
                vicon_x.append(x)
                vicon_y.append(y)
                vicon_yaw.append(yaw)
   
    # Close the rosbag file
    bag.close()

    # Create a DataFrame for the vicon_yaw data
    vicon_df = pd.DataFrame({'Timestamp': vicon_time, 'x': vicon_x, 
                             'y': vicon_y, 'Yaw': vicon_yaw})
    
    # Set the Timestamp column as the index
    vicon_df = vicon_df.set_index('Timestamp')
    
    # Resample the data to match the floam_time timestamps
    #floam_time = pd.to_numeric(floam_time, errors='coerce')
    vicon_resampled = vicon_df.reindex(floam_time, method='nearest')
    
    # Get the resampled yaw values
    vicon_resampled_x = vicon_resampled['x'].values
    vicon_resampled_y = vicon_resampled['y'].values
    vicon_resampled_yaw = vicon_resampled['Yaw'].values
      
    print("The average and maximum errors in meters in the x direction is," +
          str(error(floam_x, vicon_resampled_x)))
    print("The average and maximum errors in meters in the y direction is," +
          str(error(floam_y, vicon_resampled_y)))
    print("The average and maximum errors in radians in the yaw rotation is," + 
          str(error(floam_yaw, vicon_resampled_yaw)))

def error(floam, vicon):
    error = [abs(a - b) for a, b in zip(floam, vicon)]
    avg_error = (sum(error) / len(error))
    max_error = max(error)
    return(avg_error, max_error)

main()
