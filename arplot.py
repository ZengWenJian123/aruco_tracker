import matplotlib.pyplot as plt
import numpy as np
import matplotlib

fig=plt.figure()
ax=fig.gca(projection='3d')
#设置字体和字号中文
matplotlib.rcParams['font.family'] = ['sans-serif']
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['font.size'] = 10

# 绘制二维码
qr_x = np.arange(-0.044, 0.044, 0.01)
qr_y = np.arange(-0.044, 0.044, 0.01)
qr_x, qr_y = np.meshgrid(qr_x, qr_y)
#qr_z = np.arange(-0.044, 0.044, 0.01)
qr_z = np.zeros((1,1))
qr_plot = ax.plot_surface(qr_x, qr_y, qr_z)

# 绘制颤抖以指示图案的顶部
top = ax.quiver(0, 0, 0, 0, 1, 0, length=0.1, colors='k')

# 绘制相机位置
camera_x = (285, 367)
camera_y = (328, 392)
camera_z = (253, 401)
camera = ax.plot(camera_x, camera_y, camera_z, 'bo', label="camera")


# 格式化图
ax.set_zlim(-0, 1)
ax.set_xlim(-0.5, 0.5)
ax.set_ylim(-0.5, 0.5)
ax.set_xlabel('X (米)')
ax.set_ylabel('Y (米)')
ax.set_zlabel('Z (米)')
ax.legend(numpoints=1)

plt.show()