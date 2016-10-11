#!/usr/bin/env python3
#encoding: utf8

BASELINE_TIME = [3, 7, 6, 8, 10, 22, 32, 58, 114, 201]

# movie write

MOVIE_COMPRESS_SINGLE = \
    [2, 2, 8, 12, 30, 50, 102, 220, 359, 744]
MOVIE_ENCRYPT_SINGLE = \
    [16, 19, 31, 89, 194, 367, 692, 1417, 2926, 5727]
MOVIE_ENCRYPT_PLUS_COMPRESS = \
    [9, 25, 45, 108, 234, 401, 794, 1668, 3417, 6900]
MOVIE_TILL_IPFS = \
    [20, 51, 86, 208, 428, 821, 1650, 3227, 6473, 12943]
MOVIE_IPFS_RAW = \
    [59, 84, 100, 152, 221, 378, 648, 1223, 2328, 4625]
MOVIE_BRIG_ADD =  \
    [338, 363, 397, 495, 634, 1279, 2629, 4028, 7239, 13910]

PLOT_MOVIE_WRITE = {
    'short': 'movie_write.svg',
    'title': 'Throughput of encryption, compression and stacked (movie.mp4)',
    'names': [
        ('baseline', BASELINE_TIME),
        ('only compress', MOVIE_COMPRESS_SINGLE),
        ('only encrypt', MOVIE_ENCRYPT_SINGLE),
        ('encrypt/compress', MOVIE_ENCRYPT_PLUS_COMPRESS),
        ('ipfs add', MOVIE_IPFS_RAW),
        ('ipfs add/encrypt/zip', MOVIE_TILL_IPFS),
        ('brig stage', MOVIE_BRIG_ADD),
    ]
}

# movie read

MOVIE_DECOMPRESS = \
    [82, 825, 928, 1202, 1221, 1244, 2213, 3236, 5282, 22059]
MOVIE_DECRYPT =  \
    [85, 110, 126, 171, 234, 376, 738, 1414, 2693, 6229]
MOVIE_IPFS_CAT_AND_DECRYPT_DECOMPRESS =  \
    [105, 118, 137, 194, 290, 481, 892, 1692, 3121, 6303]
MOVIE_IPFS_CAT =  \
    [75, 89, 109, 136, 192, 321, 582, 1059, 2019, 3956]
MOVIE_BRIG_CAT =  \
    [331, 355, 375, 471, 637, 972, 1888, 2887, 4005, 6932]
MOVIE_FUSE_CAT = \
    [147, 245, 464, 760, 1598, 2783, 6009, 11861, 24226, 50311]

PLOT_MOVIE_READ = {
    'short': 'movie_read.svg',
    'title': 'Throughput of decryption, decompression & more (movie.mp4)',
    'names': [
        ('baseline', BASELINE_TIME),
        ('only decompress', MOVIE_DECOMPRESS),
        ('only decrypt', MOVIE_DECRYPT),
        ('both', MOVIE_IPFS_CAT_AND_DECRYPT_DECOMPRESS),
        ('ipfs cat', MOVIE_IPFS_CAT),
        ('brig cat', MOVIE_BRIG_CAT),
        ('fuse cat', MOVIE_FUSE_CAT),
    ]
}

# =====================

# Archive write
ARCHIVE_COMPRESS_SINGLE =  \
    [6, 15, 21, 45, 73, 157, 329, 551, 1251, 3003]
ARCHIVE_ENCRYPT_SINGLE =  \
    [16, 34, 40, 91, 204, 343, 694, 1437, 2879, 5667]
ARCHIVE_ENCRYPT_PLUS_COMPRESS =  \
    [18, 16, 50, 99, 181, 304, 671, 1257, 2904, 6701]
ARCHIVE_TILL_IPFS =  \
    [9, 33, 74, 146, 307, 533, 992, 1978, 4498, 10492]
ARCHIVE_IPFS_RAW =  \
    [75, 87, 111, 154, 205, 346, 666, 1209, 2357, 4616]
ARCHIVE_BRIG_ADD =  \
    [325, 350, 380, 423, 546, 926, 1455, 2749, 5380, 12683]

PLOT_ARCHIVE_WRITE = {
    'short': 'archive_write.svg',
    'title': 'Throughput of encryption, compression and stacked (archive.tar)',
    'names': [
        ('baseline', BASELINE_TIME),
        ('only compress', ARCHIVE_COMPRESS_SINGLE),
        ('only encrypt', ARCHIVE_ENCRYPT_SINGLE),
        ('encrypt/compress', ARCHIVE_ENCRYPT_PLUS_COMPRESS),
        ('ipfs add', ARCHIVE_IPFS_RAW),
        ('ipfs add/encrypt/zip', ARCHIVE_TILL_IPFS),
        ('brig stage', ARCHIVE_BRIG_ADD),
    ]
}

ARCHIVE_DECOMPRESS = \
    [84, 82, 96, 108, 133, 182, 271, 467, 957, 2100]
ARCHIVE_DECRYPT = \
    [99, 91, 125, 153, 233, 381, 676, 1342, 2525, 4990]
ARCHIVE_IPFS_CAT_AND_DECRYPT_DECOMPRESS = \
    [110, 115, 137, 181, 254, 392, 698, 1406, 2644, 5163]
ARCHIVE_IPFS_CAT = \
    [76, 91, 95, 130, 202, 330, 573, 1077, 2033, 3904]
ARCHIVE_BRIG_CAT = \
    [349, 341, 354, 402, 517, 715, 1093, 1928, 3160, 5961]
ARCHIVE_FUSE_CAT = \
    [104, 231, 319, 688, 956, 2817, 5078, 9613, 18996, 42485]

PLOT_ARCHIVE_READ = {
    'short': 'archive_read.svg',
    'title': 'Throughput of decryption, decompression & more (archive.tar)',
    'names': [
        ('baseline', BASELINE_TIME),
        ('only decompress', ARCHIVE_DECOMPRESS),
        ('only decrypt', ARCHIVE_DECRYPT),
        ('both', ARCHIVE_IPFS_CAT_AND_DECRYPT_DECOMPRESS),
        ('ipfs cat', ARCHIVE_IPFS_CAT),
        ('brig cat', ARCHIVE_BRIG_CAT),
        ('fuse cat', ARCHIVE_FUSE_CAT),
    ]
}

import pygal
import pygal.style


def render_plot(data, logarithmic=False):
    pygal.style.LightSolarizedStyle.background = "#FFFFFF"
    pygal.style.LightSolarizedStyle.plot_background = "#FFFFFF"

    line_chart = pygal.Line(
        legend_at_bottom=True,
        logarithmic=logarithmic,
        style=pygal.style.LightSolarizedStyle,
        interpolate='cubic'
    )
    line_chart.title = data['title']
    line_chart.x_labels = ['{} MB'.format(2 ** idx) for idx in range(0, 10)]
    line_chart.x_title = "Input size in MB"
    line_chart.y_title = "Time in milliseconds"
    for name, points in data['names']:
        line_chart.add(name, points)

    line_chart.render_to_file(data['short'])


render_plot(PLOT_MOVIE_WRITE, logarithmic=True)
render_plot(PLOT_MOVIE_READ, logarithmic=True)
render_plot(PLOT_ARCHIVE_WRITE, logarithmic=True)
render_plot(PLOT_ARCHIVE_READ, logarithmic=True)
