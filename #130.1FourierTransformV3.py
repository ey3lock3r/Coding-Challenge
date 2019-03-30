import numpy as np
import copy
import matplotlib.pyplot as plt
import matplotlib.lines as ln
import matplotlib.animation as animation
import math as m
import cmath as cm
from signal_func import load_signal as load

def dft(signal):
    ln = len(signal)
    X  = []
    for k in range(ln):
        cx_sum = complex(0)
        for n in range(ln):
            #phi = (2 * np.pi * k * n) / ln
            #cx = complex(np.cos(phi), -np.sin(phi))
            cx = np.exp(-2j * np.pi * k * n / ln)
            cx_sum += (signal[n] * cx)
        
        #should be changed using normal div op?
        #cx_sum = complex(cx_sum.real/ln, cx_sum.imag/ln)
        #cx_sum.imag /= ln
        cx_sum /= ln

        freq  = k
        amp   = np.sqrt(cx_sum.real**2 + cx_sum.imag**2)
        phase = m.atan2(cx_sum.imag, cx_sum.real)
        #phase = cm.phase(cx_sum)
        comp = {
            're': cx_sum.real,
            'im': cx_sum.imag,
            'freq': freq,
            'amp': amp,
            'angle': phase
        }
        X.append(comp)
    
    return X

# load x y coordinates
x_signal = load()
#x_signal = sorted(x_signal, key=lambda a: (a['amp']))
Fourier = sorted(dft(x_signal), key=lambda a: (a['amp']))

circles = len(Fourier)
twopi   = 2 * np.pi
full_cyl = twopi / circles
angle   = 0
cnt     = 0
shift   = 100

fig, f_ax1 = plt.subplots()
fig.set_dpi(100)
fig.set_size_inches(12, 7)

f_ax1.set_aspect('equal', adjustable='datalim', anchor='C')
f_ax1.set_xlim((-600, 600))
f_ax1.set_ylim((-400, 400))

# define circles and lines
circle_arr = []
line_arr   = []

for i in range(circles):
    tr = Fourier[i]['amp']
    t_circ = plt.Circle((0, 0), tr, color='#00ffff', alpha=1, fill=False)
    circle_arr.append(t_circ)
    f_ax1.add_patch(t_circ)

    line, = f_ax1.plot([], [], lw=2, marker='o', markevery=[1])
    line_arr.append(line)

xdata = []
ydata = []
linex = []
liney = []
def comp_epicycles():
    global twopi, full_cyl, xdata, ydata, Fourier, circles, linex, liney
    t = 0
    while True:        
        xarr = []
        yarr = []
        x, y = 0, 0
        xarr.append(x)
        yarr.append(y)
        for i in range(circles):
            freq = Fourier[i]['freq']
            tr   = Fourier[i]['amp']
            phse = Fourier[i]['angle']

            x += (tr * np.cos(freq * t + phse))
            y += (tr * np.sin(freq * t + phse))

            xarr.append(x)
            yarr.append(y)
        
        linex.append(x)
        liney.append(y)

        xdata.append(copy.deepcopy(xarr))
        ydata.append(copy.deepcopy(yarr))
        t += full_cyl
        if t > twopi:
            break

comp_epicycles()
f_len = len(linex)

# define lines
sine, = f_ax1.plot([], [], lw=2)

def updatefig(data):
    global circles, ydata, xdata, cnt, linex, liney, f_len
    
    for i in range(circles):
        prevx = xdata[cnt][i]
        prevy = ydata[cnt][i]

        x = xdata[cnt][i+1]
        y = ydata[cnt][i+1]

        circle_arr[i].center = (prevx, prevy)
        line_arr[i].set_data([prevx,x], [prevy,y])

    sine.set_data(linex[:cnt], liney[:cnt])
    cnt += 1
    if cnt == f_len:
        cnt = 0

    return [*circle_arr, *line_arr, sine]

ani = animation.FuncAnimation(fig, updatefig, interval=200, blit=True)
#ani.save("codetrain.mp4")
plt.show()