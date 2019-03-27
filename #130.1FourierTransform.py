import numpy as np
import copy
import matplotlib.pyplot as plt
import matplotlib.lines as ln
import matplotlib.animation as animation
import math as m

def dft(signal):
    ln = len(signal)
    X  = []
    for k in range(ln):
        re = 0
        im = 0
        for n in range(ln):
            phi = (2 * np.pi * k * n) / ln
            re += signal[n] * np.cos(phi)
            im -= signal[n] * np.sin(phi)
        
        re /= ln
        im /= ln
        freq  = k
        amp   = np.sqrt(re**2 + im**2)
        angle = m.atan2(im, re)
        comp = {
            're': re,
            'im': im,
            'freq': freq,
            'amp': amp,
            'angle': angle
        }
        X.append(comp)
    
    return X

signal = np.random.randint(-50, 100, 50)
#signal = range(100)
Fouriery = dft(signal)
circles = len(Fouriery)
full_cyl = 2 * np.pi / circles
r     = 60
rad = lambda a: r * (2 / (a * np.pi))
angle   = 0
shift   = 100
s_num   = 400 #sine data

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
    tr = Fouriery[i]['amp']
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
    global angle, circles, ydata, r, shift, adata, s_num, full_cyl
    
    x, y = 0, 0
    for i in range(circles):
        freq = Fouriery[i]['freq']
        tr   = Fouriery[i]['amp']
        phse = Fouriery[i]['angle']
        prevx = x
        prevy = y
        x += (tr * np.cos(freq * angle + phse + (np.pi/2)))
        y += (tr * np.sin(freq * angle + phse + (np.pi/2)))

        circle_arr[i].center = (prevx, prevy)
        line_arr[i].set_data([prevx,x], [prevy,y])

    ydata.insert(0, y)
    ydata = ydata[0:s_num]

    line2.set_data([shift, x], [y, y])
    
    tdata = adata[0:len(ydata)]
    sine.set_data(tdata, ydata)
    angle += full_cyl
    return [*circle_arr, *line_arr, sine, line2]

ani = animation.FuncAnimation(fig, updatefig, interval=200, blit=True)
plt.show()