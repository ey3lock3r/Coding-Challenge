import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()
fig.set_dpi(1200)
# fig.set_size_inches(12, 12)
ax.set_aspect('equal', adjustable='datalim', anchor='C')
# colors = ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
#         'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
#         'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']
MAX_ITER = 255
lw = 2048
n_range = np.linspace(-2, 2, num=lw)
X, Y = np.meshgrid(n_range, n_range)
Z = X + Y * 1j
mat = np.zeros((lw,lw, 3))

mandelbrotset = lambda z, c: z**2 + c

for x in range(lw):
    for y in range(lw):
        c = Z[x,y]
        a = mandelbrotset(0, c)
        iter = 0        
        while a.real**2 + a.imag**2 <= 2*2 and iter < MAX_ITER + 1:
            a = mandelbrotset(a, c)
            iter += 1
        
        Z[x,y] = iter

mat[Z==MAX_ITER] = [0,0,0]
mat[Z<MAX_ITER] = [1,1,1]

ax.imshow(mat)
ax.set_axis_off()
path = '/Users/IBM_ADMIN/Documents/Coding Challenge/Coding-Challenge/'
plt.savefig(path + 'mandelbrot_set.svg', format='svg', dpi=1200, bbox_inches='tight')
plt.show()
