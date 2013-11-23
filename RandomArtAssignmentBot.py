
'''
ART ASSIGNMENT BOT
Jeff Thompson | 2013 | www.jeffreythompson.org

A Twitter bot that generates random art assignments.

Takes the form of:
	{do} {a/an} {media} {verb} {approach} {topic}, due {due_date}.

For example:
	Make a piece exploring the idea of landscape, due Feb 22, 2014.

LOAD OAUTH SETTINGS
Assumes Twitter OAuth settings, saved in a file
called OAuthSettings.py, saved in the following format:
	
	settings = {
		'consumer_key': 'xxxx',
		'consumer_secret': 'xxxx',
		'access_token_key': 'xxxx',
		'access_token_secret': 'xxxx'
	}

REQUIRES
+ dateutil
	- http://labix.org/python-dateutil
+ OAuthlib
	- https://github.com/requests/requests-oauthlib
+ Python Twitter
	- https://github.com/bear/python-twitter

This project is released under a Creative Commons BY-NC-SA
License - feel free to use, but please let me know.

'''

import random, os
from datetime import date													# for date formatting
from dateutil.relativedelta import relativedelta	# more date stuff
from OAuthSettings import settings								# import from settings.py
import twitter																		# for posting
import os																					# for getting current directory
from sys import exit															# for exiting when done posting


# VARIABLES
additional_ofs = 20					# num of additional 'of', essentially weighted random for verbs
chance_approach = 0.2				# chance assignment will include an approach (ie: 'your relationship to'...)


# CLEAR SCREEN
os.system('cls' if os.name=='nt' else 'clear')


# SOURCE LISTS
do_list = [ 'make', 'construct', 'build', 'create', 'produce' ]

media_list = [ 'piece', 'series', 'dangerous project', 'work',
'sculpture', 'assemblage', 'stone carving', 'installation', 'wood carving', 'welded metal sculpture', 'machine', 'clay form', '3d rendering'
'photograph', 'film', 'video', 'website', 'piece of software',
'etching', 'lithograph', 'woodblock print', 'screenprint', 'artist book', 'linocut'
'flipbook',
'performance', 'durational performance', 'event', 'intervention'  ]

verbs = [ 'exploring', 'investigating', 'interrogating', 'experimenting with', 'on', 'about', 'analyzing', 'examining', 'probing', 'researching', 'critiquing', 'examining', 'considering', 'challenging', 'denying', 'refusing' ]

for i in range(additional_ofs):
	verbs.append('of')

approaches = [ 'the idea of', 'your relationship to', 'the exploitation of', 'the history of' ]

topics = [ 'landscape', 'portrait', 'self-portrait', 'still life', 'gender', 'sexuality', 'history', 'food', 'home', 'social media', 'animals', 'self', 'Modernity', 'psycho-sexual self', 'narrative', 'cats on the internet', 'the body', 'sunsets', 'time', 'mortality', 'memory', 'death', 'family', 'space', 'race', 'vulnerability', 'celebration', 'decoration', 'utility', 'pattern', 'childhood', 'the natural world', 'your dream world' ]


# CREATE TWEET FROM RANDOM CHOICES
do = do_list[random.randrange(0, len(do_list))].title()
verb = verbs[random.randrange(0, len(verbs))]
approach = approaches[random.randrange(0, len(approaches))]
topic = topics[random.randrange(0, len(topics))]
media = media_list[random.randrange(0,len(media_list))]
due_date = ''
which_range = random.randrange(0,8)

# minutes
if which_range == 0:
	due_date = 'in ' + str(random.randrange(1,60)) + ' seconds'

# hours
elif which_range == 1:
	due_date = 'in ' + str(random.randrange(1,60)) + ' minutes'

# tomorrow
elif which_range == 2:
	due_date = 'tomorrow'

# one week
elif which_range == 3:
	due_date = 'on ' + (date.today() + relativedelta(weeks = +1)).strftime('%a, %b %d')

# 2-4 weeks
elif which_range == 4:
	due_date = 'on ' + (date.today() + relativedelta(weeks = +random.randrange(2,5))).strftime('%a, %b %w')

# 2-11 months
elif which_range == 5:
		due_date = 'on ' + (date.today() + relativedelta(months = +random.randrange(2,11))).strftime('%a, %b %d, %Y')

# one year
elif which_range == 6:
	due_date = 'on ' + (date.today() + relativedelta(years = +1)).strftime('%a, %b %d, %Y')

# years
else:
		due_date = 'on ' + (date.today() + relativedelta(years = +random.randrange(2,11))).strftime('%a, %b %d, %Y')


# BUILD ASSIGNMENT!
article = 'a'
if media[0] in 'aeiou':
	article = 'an'

if random.random() < chance_approach:
	assignment = do + ' ' + article + ' ' + media + ' ' + verb + ' ' + approach + ' ' + topic + ', due ' + due_date + '.'
else:
	assignment = do + ' ' + article + ' ' + media + ' ' + verb + ' ' + topic + ', due ' + due_date + '.'

# LOAD OAUTH DETAILS FROM FILE TO ACCESS TWITTER
# see notes at top for format
consumer_key = settings['consumer_key']
consumer_secret = settings['consumer_secret']
access_token_key = settings['access_token_key']
access_token_secret = settings['access_token_secret']


# CONNECT TO TWITTER API, POST and PRINT RESULT
# catch any errors and let us know
try:
	api = twitter.Api(consumer_key = consumer_key, consumer_secret = consumer_secret, access_token_key = access_token_key, access_token_secret = access_token_secret)	
	print '\n\n' + assignment + '\n\n'
	print 'posting to Twitter...'
	status = api.PostUpdate(assignment)
	print '  post successful!\n\n'
except twitter.TwitterError:
	print api.message


# SAVE TWEETS TO FILE
# get current directory, prepend to word list paths
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
with open(os.path.join(__location__, 'Tweets.txt'), 'a') as file:
	file.write(assignment + '\n\n')


# ALL DONE!
print ('\n') * 4
exit()