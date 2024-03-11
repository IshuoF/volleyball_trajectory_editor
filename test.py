import numpy as np
import matplotlib.pyplot as plt

def volleyball_trajectory(t, v0, theta, h0):
    g = 9.8  # 重力加速度
    air_resistance = 0.2  # 空氣阻力
    v_x = v0 * np.cos(theta)
    v_y = v0 * np.sin(theta)
    
    x = v_x * t
    y = v_y * t 
    z = h0 + air_resistance * t**2 - 0.5 * g * t**2 # 只考慮空氣阻力，不考慮重力
    
    return np.array([x, y, z])

# 球場尺寸
field_width = 2
field_length = 15

# 起始和終止條件
start_point = np.array([0, 0, 2.5])  # 起點設在球場的左下角
end_point = np.array([field_width, field_length, 0])  # 終點設在球場的右上角
h0 = start_point[2]

# 計算初始速度和角度
delta_x = end_point[0] - start_point[0]
delta_y = end_point[1] - start_point[1]
delta_z = end_point[2] - start_point[2]
delta_t = 1.5  # 擬定的飛行時間
v0 = np.sqrt(delta_x**2 + delta_y**2 + delta_z**2) / delta_t  # 初始速度
theta = np.arctan2(delta_y, delta_x)  # 垂直平面的角度

# 生成30個點
num_points = 30
times = np.linspace(0, delta_t, num_points)
trajectory = np.array([volleyball_trajectory(t, v0, theta, h0) for t in times])

# 繪製軌跡
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2], marker='o')

# 設置球場尺寸
ax.set_xlim(0, field_width)
ax.set_ylim(0, field_length)
ax.set_zlim(0, max(trajectory[:, 2]))

# 設置座標軸標籤
ax.set_xlabel('X (Width)')
ax.set_ylabel('Y (Length)')
ax.set_zlabel('Z (Height)')

plt.show()
