import numpy as np
import copy
import matplotlib.pyplot as plt
import matplotlib.lines as ln
import matplotlib.animation as animation
import math as m
import cmath as cm
from signal_func import load_signal as load
# class Complex(object):
#     def __init__(self, a, b):
#         self.re = a
#         self.im = b

#     def mul(self, c):
#         re = self.re * c.re - self.im * c.im
#         im = self.re * c.im + self.im * c.re
#         return Complex(re, im)
    
#     def add(self, c):
#         self.re += c.re
#         self.im += c.im

def dft(signal):
    ln = len(signal)
    X  = []
    for k in range(ln):
        cx_sum = complex(0)
        for n in range(ln):
            phi = (2 * np.pi * k * n) / ln
            cx = complex(np.cos(phi), -np.sin(phi))
            cx_sum += (signal[n] * cx)
        
        #should be changed using normal div op?
        cx_sum = complex(cx_sum.real/ln, cx_sum.imag/ln)
        #cx_sum.imag /= ln

        freq  = k
        amp   = np.sqrt(cx_sum.real**2 + cx_sum.imag**2)
        #angle = m.atan2(cx_sum.imag, cx_sum.real)
        angle = cm.phase(cx_sum)
        comp = {
            're': cx_sum.real,
            'im': cx_sum.imag,
            'freq': freq,
            'amp': amp,
            'angle': angle
        }
        X.append(comp)
    
    return X

#signal = np.random.randint(-50, 100, 50)
#signal = range(100)
#x_signal = list(map(lambda a: complex(a['x'], a['y']), s.drawing))
x_signal = load()

Fourier = dft(x_signal)
circles = len(Fourier)
twopi   = 2 * np.pi
full_cyl = twopi / circles
#r     = 60
#rad = lambda a: r * (2 / (a * np.pi))
angle   = 0
shift   = 100
#s_num   = 400 #sine data

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

# define lines
#line2, = f_ax1.plot([], [], lw=2)
sine, = f_ax1.plot([], [], lw=2)

def updatefig(data):
    global angle, circles, ydata, xdata, full_cyl, twopi
    
    x, y = 0, 0
    for i in range(circles):
        freq = Fourier[i]['freq']
        tr   = Fourier[i]['amp']
        phse = Fourier[i]['angle']
        prevx = x
        prevy = y

        x += (tr * np.cos(freq * angle + phse))
        y += (tr * np.sin(freq * angle + phse))

        circle_arr[i].center = (prevx, prevy)
        line_arr[i].set_data([prevx,x], [prevy,y])

    xdata.append(x)
    ydata.append(y)
    #ydata = ydata[0:s_num]

    #line2.set_data([shift, x], [y, y])
    
    #tdata = adata[0:len(ydata)]
    #sine.set_data(tdata, ydata)
    sine.set_data(xdata, ydata)
    angle += full_cyl
    if angle > twopi:
        xdata = []
        ydata = []
        angle = 0

    return [*circle_arr, *line_arr, sine]

ani = animation.FuncAnimation(fig, updatefig, interval=200, blit=True)
plt.show()