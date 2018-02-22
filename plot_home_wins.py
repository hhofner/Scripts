'''
Plot home wins for team1 against team2
'''

team1 = 'Bremen'
team2 = 'Hamburger'

folders = ['2012-13', '2013-14',
           '2014-15', '2015-16',
           '2016-17']

files = ['1-bundesliga-i.txt',
         '1-bundesliga-ii.txt',
         'cup.txt']

import os
import matplotlib.pyplot as plt

mapping = {1:'win',0:'tie',-1:'loss'}

home_results = []
cwd = os.getcwd()

for folder in folders:
    os.chdir(folder)
    print('Entering dir: %s' % folder)
    for txt in files:
        print('Parsing file: %s' % txt)
        score = None
        try:
            with open(txt, 'r') as stats:
                lines = stats.readlines()
                for line in lines:
                    content = line.split()
                    if len(content) < 4:
                        continue
                    if (team1 in content) and (team2 in content) \
                        and content.index(team1) < content.index(team2):
                        print('Found content: %s' % line)
                        for c in content:
                            if len(c) == 3 and (':' in c or '-' in c):
                                if ':' in c:
                                    score = c.split(':')
                                    break
                                else:
                                    score = c.split('-')
                                    break
                        if int(score[0]) - int(score[1]) > 0:
                            home_results.append(1)
                        elif int(score[0]) - int(score[1]) == 0:
                            home_results.append(0)
                        else:
                            home_results.append(-1)

        except IOError:
            print('File %s not valid.' % txt)
            continue
    os.chdir(cwd)

print(home_results)

with plt.xkcd():
    # BTW, this silly abbreviation is
    # Get Current Axis...
    axes = plt.gca()

    y_axis = [-1.5, -1, -0.5, 0, 0.5, 1, 1.5]
    y_values = ['','Win', '', 'Tie', '', 'Loss', '']
    # axes.get_xaxis().set_ticks([])
    plt.xticks([])
    axes.set_ylim([-1.5,1.5])
    axes.set_yticklabels(y_values)
    axes.axhline(y=0.5, linestyle='--', color='gray', linewidth=0.5)
    axes.axhline(y=-0.5, linestyle='--', color='gray', linewidth=0.5)
    axes.plot(home_results, linestyle=':', marker='o', markersize=15, color='black')
    plt.title('Last 5 Results\nWerder Bremen - Hamburger SV')

plt.show()
