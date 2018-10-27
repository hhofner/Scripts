'''
Plot my PPS history since February of 2018
'''

import matplotlib.pyplot as plt
import matplotlib.dates
import Image
import datetime
import numpy as np
import os

#image_path = '~path'
replay_path = "" # path removed for reasons
os.chdir(replay_path)

dates = []
pps   = []

for filename in os.listdir(os.getcwd()):
    file = open(filename, 'r')
    for line in file:
        if 'statistics.pps' in line:
            start = line.index('=')
            temp_pps = float(line[start+1:].rstrip())  # rstrip removes /n from string

            stripped_filename = filename[:-4]
            stuff = stripped_filename.split('_')
            elem  = list(map(int, stuff))  # typecast the entire list into list of ints

            temp = datetime.datetime(year=elem[0], month=elem[1], day=elem[2],
                                     hour=elem[3], minute=elem[4], second=elem[5])

            dates.append(temp)
            pps.append(temp_pps)

fig = plt.figure()
#fig.subtitle('Piece Per Second (PPS) History')

dates_to_plot = matplotlib.dates.date2num(dates)
print('Begining to plot')
plt.plot_date(dates_to_plot, pps, marker=".", color='#303338')

plt.axvline(datetime.datetime(2018,05,01), color='#edb73b')
plt.axvline(datetime.datetime(2018,06,01), color='#edb73b')
plt.axvspan(datetime.datetime(2018,05,01), datetime.datetime(2018,06,01), color='#e8b645', alpha=0.5)
plt.text(datetime.datetime(2018,05,15), 3, 'No Data Available', rotation='vertical')

avg = 0
for p in pps:
    avg += p
avg = avg/len(pps)

plt.axhline(avg, color='black')
plt.text(datetime.datetime(2018,03,18), avg+0.12, 'Avg PPS: %s' % avg,
         color='black', bbox=dict(facecolor='none', edgecolor='black', pad=7.0))

plt.title('NullpoMino 40 Line Race\nPiece Per Seconds(PPS) Records')
plt.xlabel('Datetime')
plt.ylabel('Piece Per Second')

'''im = Image.open(image_path)
height = im.size[1]
im = np.array(im).astype(np.float) / 255

#Image
fig.figimage(im, 0, fig.bbox.ymax - height)'''

plt.show()
