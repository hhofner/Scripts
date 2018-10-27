# Scripts
## List of miscellaneous  scripts in various languages for various purposes

### TCP Tic-Tac-Toe
Files:
  * TTTServer.py
  * TTTClient.py

Run these two files and see AI's play Tic Tac Toe.
You may edit the ports on each file to whatever ports you may prefer.
TTTClient expects a commandline argument of the serverAddress.

These two scripts use an Alpha-Beta probing algorithm, so they always
play a tie, as they are perfect players.

### Ruby Secret Santa
File(s):
  * secret_santa.rb

Script to send out secret santa emails to participants. Keep in mind that
the secret santa pairings get deleted after they are sent, so the user of the script
has no idea who they are.

In the options dictionary, enter your email domain, username and password (for GMAIL
you will have to "unlock" some setting temporarily).

Run the Ruby script, and it will ask for participants name and email.

### Plotting Bundesliga Home Wins against a certain team
File(s):
  * plot_home_wins.py

Using the [de-deutschland](https://github.com/openfootball/de-deutschland) database for Bundesliga matches, plot the last 5
home match results against whatever team.

Example for Nordderby:

![bremen_hsv](https://github.com/hhofner/Scripts/blob/master/img/better_bremen_hsv.png "Nordderby")

### Creating a WordCloud for the comments of a certain Reddit thread
File(s):
  * create_thread_wordcloud.py

A little script which is essentially just the [PRAW Comment Extraction](https://praw.readthedocs.io/en/latest/tutorials/comments.html) and the
[Python Word Cloud package](https://github.com/amueller/word_cloud) tutorials pasted
together. It was a fun little script, but my friend said I had a boring result, so I
lost motivation to do anything better with it. Image below of PSG vs. Real Madrid Reddit
match thread:

![psg_rm](https://github.com/hhofner/Scripts/blob/master/img/psg.png "PSG WordCloud")

### Plotting PPS Data from Nullpomino Application
File(s):
  * plot_pps.py
  
This script plots your previous played games PPS (Piece per Second) data from Nullpomino (A Tetris Desktop game). It's highly tailored to mine (note the "no data available" section), but can perhaps be easily fixed to your liking. The plot:

![pps](https://github.com/hhofner/Scripts/blob/master/pps_record_oct27.png)
