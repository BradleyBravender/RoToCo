# This script graphs the FLOAM x, y, and z translation, and x, y, z, and w rotation against the vicon_tracker's.
import rosbag
import matplotlib.pyplot as plt

bag = rosbag.Bag('Test1.bag')
floam = '/odom'
vicon = '/vicon/Jackal/Jackal'

floam_pos_x = []
floam_pos_y = []
floam_pos_z = []
floam_orient_x = []
floam_orient_y = []
floam_orient_z = []
floam_orient_w = []

floam_timestamp = []

vicon_trans_x = []
vicon_trans_y = []
vicon_trans_z = []
vicon_rota_x = []
vicon_rota_y = []
vicon_rota_z = []
vicon_rota_w = []

vicon_timestamp = []

for topic, msg, t in bag.read_messages(topics=[floam]):
    floam_pos_x.append(msg.pose.pose.position.x)
    floam_pos_y.append(msg.pose.pose.position.y)
    floam_pos_z.append(msg.pose.pose.position.z)
    floam_orient_x.append(msg.pose.pose.orientation.x)
    floam_orient_y.append(msg.pose.pose.orientation.y)
    floam_orient_z.append(msg.pose.pose.orientation.z)
    floam_orient_w.append(msg.pose.pose.orientation.w)
    floam_timestamp.append(t.to_sec())

for topic, msg, t in bag.read_messages(topics=[vicon]):
    vicon_trans_x.append(msg.transform.translation.x)
    vicon_trans_y.append(msg.transform.translation.y)
    vicon_trans_z.append(msg.transform.translation.z)
    vicon_rota_x.append(msg.transform.rotation.x)
    vicon_rota_y.append(msg.transform.rotation.y)
    vicon_rota_z.append(msg.transform.rotation.z)
    vicon_rota_w.append(msg.transform.rotation.w)
    vicon_timestamp.append(t.to_sec())
    
# Create a 2x2 grid of subplots
fig, axs = plt.subplots(2, 4)

for ax in axs.flat:
    ax.set_xticklabels([])
    ax.set_yticklabels([])


# Plot data on the first subplot
axs[0, 0].plot(floam_timestamp, floam_pos_x, label='Floam', linewidth=0.6)
axs[0, 0].plot(vicon_timestamp, vicon_trans_x, label='Vicon', linewidth=0.6)
axs[0, 0].set_title('X Position')

axs[0, 1].plot(floam_timestamp, floam_pos_y, label='Floam', linewidth=0.6)
axs[0, 1].plot(vicon_timestamp, vicon_trans_y, label='Vicon', linewidth=0.6)
axs[0, 1].set_title('Y Position')

axs[0, 2].plot(floam_timestamp, floam_pos_z, label='Floam', linewidth=0.6)
axs[0, 2].plot(vicon_timestamp, vicon_trans_z, label='Vicon', linewidth=0.6)
axs[0, 2].set_title('Z Position')

axs[1, 0].plot(floam_timestamp, floam_orient_x, label='Floam', linewidth=0.6)
axs[1, 0].plot(vicon_timestamp, vicon_rota_x, label='Vicon', linewidth=0.6)
axs[1, 0].set_title('X Rotation')

axs[1, 1].plot(floam_timestamp, floam_orient_y, label='Floam', linewidth=0.6)
axs[1, 1].plot(vicon_timestamp, vicon_rota_y, label='Vicon', linewidth=0.6)
axs[1, 1].set_title('Y Rotation')

axs[1, 2].plot(floam_timestamp, floam_orient_z, label='Floam', linewidth=0.6)
axs[1, 2].plot(vicon_timestamp, vicon_rota_z, label='Vicon', linewidth=0.6)
axs[1, 2].set_title('Z Rotation')

axs[1, 3].plot(floam_timestamp, floam_orient_w, label='Floam', linewidth=0.6)
axs[1, 3].plot(vicon_timestamp, vicon_rota_w, label='Vicon', linewidth=0.6)
axs[1, 3].set_title('W Rotation')

plt.legend(loc='best')
plt.savefig('Graph.png', dpi=600)

plt.show()
