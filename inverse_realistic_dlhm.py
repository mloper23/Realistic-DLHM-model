import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from skimage import color, io
from scipy.fft import fft2, ifft2
import cv2 as cv


def i_realistic_dlhm(hologram, L, z, W_c, wavelength):
    # Size of the input sample
    N, M = hologram.shape

    # Magnification factor
    Mag = L / z
    W_s = W_c / Mag

    # Wave number
    k = 2 * np.pi / wavelength

    # Spatial coordinates in the camera's plane
    x = np.linspace(-W_c / 2, W_c / 2, N)
    y = np.linspace(-W_c / 2, W_c / 2, M)
    u, v = np.meshgrid(x, y)

    # Radial distribution spherical wavefront source
    r = np.sqrt(u ** 2 + v ** 2 + (L - z) ** 2)
    r = r / np.max(np.max(r))

    # Spatial frequency coordinates at the sample's plane
    df = 1 / W_s
    fx, fy = np.meshgrid(np.arange(-N / 2 * df, N / 2 * df, df),
                         np.arange(-M / 2 * df, M / 2 * df, df))

    # Complex exponential term for the diffraction
    E = np.exp(-1j * (L - z) * np.sqrt(k ** 2 - 4 * np.pi ** 2 * (fx ** 2 + fy ** 2)))

    # ASM
    Uz = ifts(fts(hologram) * E)
    Amplitude = np.abs(Uz)
    Phase = np.angle(Uz)

    # Finding the maximum distortion
    Max_D = np.abs((L + np.abs(np.sqrt(W_c ** 2 / 2 + L ** 2) - L)) / z - L / z)
    print(Max_D)

    # Distort the hologram
    camMat = np.array([[N, 0, N / 2], [0, M, M / 2], [0, 0, 1]])
    dist = np.array([Max_D, 0, 0, 0])
    Amplitude = cv.undistort(Amplitude, camMat, dist)


    return Amplitude, Phase

def ifts(A):
    return np.fft.ifftshift(np.fft.ifft2(np.fft.fftshift(A)))

def fts(A):
    return np.fft.ifftshift(np.fft.fft2(np.fft.fftshift(A)))
