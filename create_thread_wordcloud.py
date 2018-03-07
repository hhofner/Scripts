'''
Extract comments from Reddit thread and make a word cloud.
'''

thread = 'https://www.reddit.com/r/soccer/comments/82hkyv/match_thread_paris_saintgermain_vs_real_madrid/'

import praw
from wordcloud import WordCloud
from PIL import Image
import numpy as np

reddit = praw.Reddit(user_agent='Comment Extraction (by /u/username)',
                     client_id='', client_secret="")

submission = reddit.submission(url=thread)

comments = ""
rand = 10
submission.comments.replace_more(limit=None)
for comment in submission.comments.list():
    if rand > 0:
        print(comment.body)
        rand -= 1
    comments = comments + " " + comment.body

import matplotlib.pyplot as plt
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

#lower max_font_size
wordcloud = WordCloud(max_font_size=40).generate(comments)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

# #######################################################################
#
# # read mask image
# psg_mask = np.array(Image.open("img/psg_logo.png"))
#
# wc = WordCloud(background_color="white", max_words=2000, mask=psg_mask)
# # generate word cloud
# wc.generate(comments)
#
# # store to file
# wc.to_file("psg.png")
#
# # show
# plt.imshow(wc, interpolation='bilinear')
# plt.axis("off")
# plt.figure()
# # plt.imshow(psg_mask, cmap=plt.cm.gray, interpolation='bilinear')
# plt.axis("off")
# plt.show()
