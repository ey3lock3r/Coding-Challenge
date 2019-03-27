import numpy as np
import copy
import matplotlib.pyplot as plt
import matplotlib.lines as ln
import matplotlib.animation as animation

r     = 60
rad = lambda a: r * (2 / (a * np.pi))
circles = 4
angle   = 0
shift   = 100
s_num   = 400

fig, f_ax1 = plt.subplots()
fig.set_dpi(100)
fig.set_size_inches(12, 7)

f_ax1.set_aspect('equal', adjustable='datalim', anchor='C')
f_ax1.set_xlim((-150, 600))
f_ax1.set_ylim((-200, 200))

# define circles and lines
circle_arr = []
line_arr   = []
for i in range(circles):
    n  = i * 2 + 1
    
    tr = rad(n)
    t_circ = plt.Circle((0, 0), tr, color='#00ffff', alpha=1, fill=False)
    circle_arr.append(t_circ)
    f_ax1.add_patch(t_circ)

    line, = f_ax1.plot([], [], lw=2, marker='o', markevery=[1])
    line_arr.append(line)

adata = range(shift, shift + s_num)
ydata = []

# define lines
line2, = f_ax1.plot([], [], lw=2)
sine, = f_ax1.plot([], [], lw=2)

def updatefig(data):
    global angle, circles, ydata, r, shift, adata, s_num
    
    x, y = 0, 0
    for i in range(circles):
        n = i * 2 + 1

        tr = rad(n)
        prevx = x
        prevy = y
        x += (tr * np.cos(n * angle))
        y += (tr * np.sin(n * angle))

        circle_arr[i].center = (prevx, prevy)
        line_arr[i].set_data([prevx,x], [prevy,y])

    ydata.insert(0, y)
    ydata = ydata[0:s_num]

    line2.set_data([shift, x], [y, y])
    
    tdata = adata[0:len(ydata)]
    sine.set_data(tdata, ydata)
    angle += 0.1
    return [*circle_arr, *line_arr, sine, line2]

ani = animation.FuncAnimation(fig, updatefig, interval=100, blit=True)
plt.show()