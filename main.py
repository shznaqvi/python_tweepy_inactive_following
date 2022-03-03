# import the module
from datetime import date, datetime

import tweepy
from dateutil.relativedelta import relativedelta

# assign the values accordingly

consumer_key = "2hufFB9UhE0hbKwh3VddigSg7"
consumer_secret = "b8YIdcMztRB1RXKkgbBPmQuGcQMTuyzsiRuCvx4ZyjpuBuQutT"
access_token = "31712631-aDw2HQboqqvuWRTKflRwJiUvvV3rYd78nHWFQcIuN"
access_token_secret = "DvX8ARhBP7bxnaBVmI2K9cqyft0hawNCG7Z1Bjlx3qnx7"

# authorization of consumer key and consumer secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# set access to user's access key and access secret
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

user = api.get_user(screen_name='shznaqvi')
# print(api.get_user(screen_name='AnzarFarhala'))
# print(api.get_user(screen_name='kirillpixel'))


inactive_friends = []
# print(user.screen_name)
# print(user.followers_count)
# for friend in user.friends():
#    print(friend.status.created_at.date(), date.today())
#    difference_in_years = relativedelta(date.today(), friend.status.created_at.date()).days
#    print(difference_in_years)
#    # print(date.today())
count = 0
a_file = open("inactive_friends.txt", "a")
b_file = open("notFollowing_friends.txt", "a")
notFollowing = []
notFollower = False

for friend in tweepy.Cursor(api.get_friends, screen_name=user.screen_name).items():
    notFollower = False

    # qw followers = api.get_friends(screen_name=friend.screen_name)

    # if user not in followers:
    #     if friend.followers_count < friend.friends_count:
    #         notFollowing.append(friend)
    #         b_file.write(str(friend.screen_name) + " - " + "nonF - Fers: " + str(friend.followers_count) + " - Fings: " + str(friend.friends_count))
    #         b_file.write("\n")
    #     notFollower = True

    count += 1
    if friend.statuses_count > 0:
        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        ##
        #
        #       LOG10(tweets*(followers/following))  < 3.33
        #
        ##
        # time.strftime("%H:%M", time_obj)
        print("%04d" % (count,), current_time, friend.screen_name, friend.statuses_count)
        difference_in_years = relativedelta(date.today(), friend.status.created_at.date()).days
        print("            > " + str(friend.status.created_at.date()), str(difference_in_years))
        tweets_list = api.user_timeline(screen_name=friend.screen_name, count=1)
        tweet = tweets_list[0]
        delta = date.today() - tweet.created_at.date()
        if delta.days > int(365):
            print("**************************************************")
            inactive_friends.append(friend)
            a_file.write(str(friend.screen_name) + " - " + str(delta.days))
            # if notFollower:
            #     a_file.write(" < - Not Follower")
            a_file.write("\n")
    else:
        print(friend.screen_name, "---")
        a_file.write(str(friend.screen_name) + " - " + "No Tweets")
        a_file.write("\n")
    # if count % 179 == 0:
    #     for i in xrange(60*15, 0, -1):
    #         sys.stdout.write(str(i) + ' ')
    #         sys.stdout.flush()
    #         time.sleep(1)

print(inactive_friends)

a_file.close()
# last status of this friend (tweepy.models.Status)
