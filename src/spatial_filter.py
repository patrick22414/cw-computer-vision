import numpy as np
from matplotlib import pyplot as plt


def conv(im: np.ndarray, kernel: np.ndarray, pad='zero'):
    if kernel.shape[0] % 2 == 0 or kernel.shape[1] % 2 == 0:
        raise ValueError("Kernel must have odd number of rows and cols")

    if pad not in ['zero', 'none', 'edge']:
        raise ValueError("Currently available padding method: 'none', 'zero', 'edge'")

    if im.ndim == 2 and kernel.ndim == 2:
        return _conv_1c(im, kernel, pad)

    elif im.ndim == 3 and kernel.ndim == 2:
        kernel = np.stack([kernel] * im.shape[-1], axis=2)
        return _conv_mc(im, kernel, pad)

    elif im.ndim == 3 and kernel.ndim == 3:
        if im.shape[2] != kernel.shape[2]:
            raise ValueError("Image and kernel do not match in number of channels")
        return _conv_mc(im, kernel, pad)

    else:
        raise ValueError("Image or kernel is not of valid number of dimensions")


def _conv_1c(im, kernel, pad):
    h, w = im.shape
    kh, kw = kernel.shape

    if pad == 'none':
        im_pad = im.copy()
        im_res = np.zeros([h - kh + 1, w - kw + 1])
    elif pad == 'zero':
        im_pad = np.pad(im, [(kh // 2, kh // 2), (kw // 2, kw // 2)], 'constant', constant_values=0)
        im_res = np.zeros_like(im)
    elif pad == 'edge':
        im_pad = np.pad(im, [(kh // 2, kh // 2), (kw // 2, kw // 2)], 'edge')
        im_res = np.zeros_like(im)
    else:
        return

    start = [(x, y) for x in range(h) for y in range(w)]
    end = [(x, y) for x in range(kh, h + kh) for y in range(kw, w + kw)]

    for s, e in zip(start, end):
        im_res[s] = np.sum(im_pad[s[0]:e[0], s[1]:e[1]] * kernel)

    return im_res


def _conv_mc(im, kernel, pad):
    h, w, _ = im.shape
    kh, kw, _ = kernel.shape

    if pad == 'none':
        im_pad = im.copy()
        im_res = np.zeros([h - kh + 1, w - kw + 1])
    elif pad == 'zero':
        im_pad = np.pad(im, [(kh // 2, kh // 2), (kw // 2, kw // 2), (0, 0)], 'constant', constant_values=0)
        im_res = np.zeros_like(im)
    elif pad == 'edge':
        im_pad = np.pad(im, [(kh // 2, kh // 2), (kw // 2, kw // 2), (0, 0)], 'edge')
        im_res = np.zeros_like(im)
    else:
        return

    start = [(x, y) for x in range(h) for y in range(w)]
    end = [(x, y) for x in range(kh, h + kh) for y in range(kw, w + kw)]

    for s, e in zip(start, end):
        patch = im_pad[s[0]:e[0], s[1]:e[1], :] * kernel
        im_res[s] = np.sum(np.sum(patch, axis=0), axis=0)

    return im_res


if __name__ == '__main__':
    im = plt.imread('F:\Documents\GitHub\cw-computer-vision\images\HMS.jpg') / 256

    laplacian_kernel = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
    laplacian_extended_kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])

    sobel_x_kernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sobel_y_kernel = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

    im_1 = conv(im, laplacian_kernel, 'edge')
    im_2 = conv(im, laplacian_extended_kernel, 'edge')

    div_x, div_y = 2, 3
    fig, ax = plt.subplots(div_x, div_y)

    for x in range(div_x):
        for y in range(div_y):
            ax[x, y].axis('off')

    ax[0, 0].imshow(im, cmap='gray')
    ax[0, 0].set_title("Origin")

    ax[0, 1].imshow(np.abs(im_1), cmap='gray')
    ax[0, 1].set_title("Laplacian")

    ax[1, 1].imshow(im - im_1, cmap='gray')
    ax[1, 1].set_title("Laplacian + Origin")

    ax[0, 2].imshow(np.abs(im_2), cmap='gray')
    ax[0, 2].set_title("Laplacian_extended")

    ax[1, 2].imshow(im - im_2, cmap='gray')
    ax[1, 2].set_title("Laplacian_extended + Origin")

    plt.show()