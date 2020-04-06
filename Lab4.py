# real time systems
# Lab4
# author: Roman Myronenko
# group: IO-72
# var: 18
import matplotlib.pyplot as plt
import numpy
import random
import math


def signal(n, omega, min_value=0, max_value=1):
    '''Return signal function.'''
    A = [min_value + (max_value - min_value) * random.random() for _ in range(n)]
    phi = [min_value + (max_value - min_value) * random.random() for _ in range(n)]

    def f(t):
        x = 0
        for i in range(n):
            x += A[i]*math.sin(omega/n*t*i + phi[i])
        return x
    return f


def get_w(N, p, k):
    """Return tuple with real and imagination parts of w."""
    return math.cos(-2*math.pi*p*k/N), math.sin(-2*math.pi*p*k/N)


def fft(x):
    '''Fast Fourier transform'''
    N = len(x)
    global F_I, F_II
    F_I = []
    F_II = []
    for p in range(N):
        F_I.append([0, 0])
        F_II.append([0, 0])

        for k in range(N // 2):
            w = get_w(N//2, p, k)
            F_I[-1][0] += x[2 * k] * w[0]
            F_I[-1][1] += x[2 * k] * w[1]
            F_II[-1][0] += x[2 * k + 1] * w[0]
            F_II[-1][1] += x[2 * k + 1] * w[1]

    F = []
    for p in range(N):
        w = get_w(N, p, 1)
        F.append(F_I[p][0]+1j*F_I[p][1] + (w[0]+1j*w[1])*(F_II[p][0]+1j*F_II[p][1]))
    FR = [i.real for i in F]
    Fi = [i.imag for i in F]
    return FR, Fi





# option values
n = 10
omega = 1100
N = 1024

range_min = 0
range_max = 1

x_gen = signal(n, omega, range_min, range_max)
x = [x_gen(i) for i in range(N)]
(FR, Fi) = fft(x)

F = [FR[i] + Fi[i] for i in range(N)]


#show results
fig = plt.figure()

ax_1 = fig.add_subplot(3, 2, 1)
ax_2 = fig.add_subplot(3, 2, 2)
ax_3 = fig.add_subplot(3, 2, 3)
ax_4 = fig.add_subplot(3, 2, 4)
ax_5 = fig.add_subplot(3, 2, 5)

ax_1.plot(range(N), FR)
ax_2.plot(range(N), Fi)
ax_3.plot(range(N), x)
ax_4.plot(range(N), F)
ax_5.plot(range(N), numpy.fft.fft(x))

ax_1.set(title='FR')
ax_2.set(title='Fi')
ax_3.set(title='x')
ax_4.set(title='F')
ax_5.set(title='numpy')


plt.show()

