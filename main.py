# import the module
import math
import time
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
followers = api.get_follower_ids(screen_name='shznaqvi')

# Self Rating Calculations
uffCount = max(user.followers_count, 1)
ufrCount = max(user.friends_count, 1)
utCount = max(user.statuses_count, 1)
if uffCount != 0 and ufrCount != 0 and utCount != 0:
    ufRating = math.log10(utCount * (uffCount / ufrCount))
else:
    ufRating = 0

print("Self URating: " + str(ufRating))

# print(api.get_user(screen_name='AnzarFarhala'))
# print(api.get_user(screen_name='AnzarFarhala').followers_count)
# print(api.get_user(screen_name='AnzarFarhala').friends_count)
# print(api.get_user(screen_name='AnzarFarhala').statuses_count)
# print(api.get_user(screen_name='kirillpixel'))
# exit(0)

inactive_friends = []
# print(user.screen_name)
# print(user.followers_count)
# for friend in user.friends():
#    print(friend.status.created_at.date(), date.today())
#    difference_in_years = relativedelta(date.today(), friend.status.created_at.date()).days
#    print(difference_in_years)
#    # print(date.today())
count = 0

today = str(date.today())
# print(date.today())

a_file = open(today + "_inactive_friends.txt", "a")
b_file = open(today + "_lowrating_friends.txt", "a")
c_file = open(today + "_notfollowing_friends.txt", "a")
d_file = open(today + "_unfollowed _friends.txt", "a")
notFollowing = []
notFollower = False
friends = []

for friend in tweepy.Cursor(api.get_friends, screen_name=user.screen_name).items():
    time.sleep(3)
    if not hasattr(friend, 'status'):
        #        print(friend.status)
        print("**************************************** NO STATUS")
        # inactive_friends.append(friend)
        print(friend.screen_name, "--- unfollowed")
        a_file.write(str(friend.screen_name) + " - No Status")
        a_file.write("\n")
        friend.unfollow()
        d_file.write(str(friend.screen_name) + ", , , , , , No Status")
        d_file.write("\n")

        continue
    friends.append(friend)
    notFollowing = [friend for friend in friends if friend.id not in followers]  # note friend.id
    # notFollower = api.exists_friendship(user, friend)

    if friend in notFollowing:
        c_file.write(str(friend.screen_name))
        print("Not following oVVVVVVVVVo ")  # now you can access the User's screen_name

    # notFollowing = []

    # qw followers = api.get_friends(screen_name=friend.screen_name)

    # if user not in followers:
    #     if friend.followers_count < friend.friends_count:
    #         notFollowing.append(friend)
    #         b_file.write(str(friend.screen_name) + " - " + "nonF - Fers: " + str(friend.followers_count) + " - Fings: " + str(friend.friends_count))
    #         b_file.write("\n")
    #     notFollower = True

    ffCount = max(friend.followers_count, 1)
    frCount = max(friend.friends_count, 1)
    tCount = max(friend.statuses_count, 1)
    # if ffCount != 0 and frCount != 0 and tCount != 0:
    fRating = math.log10(tCount * (ffCount / frCount))
    # else:
    #    fRating = 0

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
        print("            > " + str(friend.status.created_at.date()),
              str(difference_in_years) + "(Rating: " + str(fRating) + ")")
        tweets_list = api.user_timeline(screen_name=friend.screen_name, count=1)
        tweet = tweets_list[0]
        delta = date.today() - tweet.created_at.date()
        if delta.days > int(1000):
            print("**************************************************")
            # inactive_friends.append(friend)
            friend.unfollow()
            d_file.write(str(friend.screen_name) + ", "+str(ffCount)+", "+str(frCount)+", "+str(tCount)+", "+str(delta.days)+", "+str(fRating)+", "+str(ufRating)+", Inactive")
            d_file.write("\n")
            a_file.write(str(friend.screen_name) + " - " + str(delta.days) + "(Rating: " + str(fRating) + ")")
            print(friend.screen_name, "--- unfollowed (" + str(delta.days) + " days)")
            # if notFollower:
            #     a_file.write(" < - Not Follower")
            a_file.write("\n")
        if fRating < 5.55:
            print("==================================================")
            # inactive_friends.append(friend)
            b_file.write(str(friend.screen_name) + " - " + str(delta.days) + "(Rating: " + str(fRating) + ")")
            # if notFollower:
            #     a_file.write(" < - Not Follower")
            b_file.write("\n")
            if delta.days > 90:
                print(friend.screen_name, "--- unfollowed (low rating - " + str(delta.days) + " days")
                friend.unfollow()
                d_file.write(str(friend.screen_name) + ", " + str(ffCount) + ", " + str(frCount) + ", " + str(
                    tCount) + ", " + str(delta.days) + ", " + str(fRating) + ", " + str(
                    ufRating) + ", Low Rating+Inactive")
                d_file.write("\n")
            elif friend in notFollowing:
                print(friend.screen_name, "----------------------------------- unfollowed (low rating - not following")
                friend.unfollow()
                d_file.write(str(friend.screen_name) + ", " + str(ffCount) + ", " + str(frCount) + ", " + str(
                    tCount) + ", " + str(delta.days) + ", " + str(fRating) + ", " + str(
                    ufRating) + ", Low Rating+NotFollowing")
                d_file.write("\n")
            else:
                print(friend.screen_name, "--- " + str(delta.days) + " days OR Following")

        if fRating < ufRating / 2:
            print(friend.screen_name, "----------------------------------- unfollowed (following but low rating")
            friend.unfollow()
            d_file.write(str(friend.screen_name) + ", " + str(ffCount) + ", " + str(frCount) + ", " + str(
                tCount) + ", " + str(delta.days) + ", " + str(fRating) + ", " + str(
                ufRating) + ", Low Rating+Following")
            d_file.write("\n")
    else:
        print(friend.screen_name, "--- unfollowed (status 0")
        friend.unfollow()
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
