#!/usr/bin/env python
# coding: utf-8

# In[32]:


from twython import Twython
import sys
import pickle
import time
import numpy as np


np.set_printoptions(threshold=sys.maxsize)


# In[2]:


# Nagarjunas Tokens
consumer_key= 'DpQhqq12yOEXh2DRi5AfZJW5f'
consumer_secret= 'ks4mAmk7ejlpcK3UvbSWYmP0mSzrzxyHGIvzdenwZSCwnQFfkF'
access_token= '137288204-7oBGRLFjvFoAdzVHaBOoW9YkO01qvCXpeqqhOPjn'
access_token_secret= 'AZ1eG5IuXKyeO94hJh3Bi2fgsmcP6Pg0kPfIvaWuDAHPp'

# Creating a twython client
twitter = Twython(consumer_key, consumer_secret, access_token, access_token_secret)

# Triloks Tokens
consumer_key = 'svbyu0x88Q8TU8l9MowQ6Fuhx'
consumer_secret = 'h2MsLzoJ0Bj89cgHYxKSCX677e5jnAxzgH2pyzdI2KlyLlnCd1'
access_token = '392509074-iR4JUv7ve1N5t9p7YhjD6IM2dPLBYrlrTTP0YVoL'
access_token_secret = 'oU63APmXJ0RtHcxXYQkuEII7mVTvuHuYEHhRhH427D7nD'

# Creating a twython client
twitter_trilok = Twython(consumer_key, consumer_secret, access_token, access_token_secret)


twitter_list = {twitter:0, twitter_trilok:0}


# In[3]:


# Players to scrape followers from
players = ['imVkohli', 'sachin_rt', 'msdhoni', 'henrygayle', 'ImRo45'] #, 'BrianLara']

# List of all followers for the players
followers_list = {}

# All the followers
master_list = []


# In[4]:


players_ids = {'imVkohli': 71201743,
 'sachin_rt': 135421739,
 'msdhoni': 92708272,
 'henrygayle': 45452226,
 'ImRo45': 121046433,
 'BrianLara': 861083240 }


# In[5]:


# Creating the players followers list
for player, playerid in players_ids.items():
    followers_list[playerid] = twitter_trilok.get_followers_ids(screen_name=player, count=40)
    time.sleep(2)


# In[6]:


file2 = open('players_followers.obj', 'wb') 
pickle.dump(followers_list, file2)
file2.close()


# In[7]:


# All the followers append to a master list
for player in followers_list:
    master_list.extend(set(followers_list[player]['ids']))

# Look at only unique followers (drop of 600->511, which is good)
master_list = list(set(master_list))+list(players_ids.values())


# In[14]:


# Check each follower's following 
#master_list[0]

#randomk = {}
count = 0
users_not_done = []
twit = twitter

for user in master_list:
    count += 1

    try:
        randomk[user] = twit.get_friends_ids(id=user)['ids']
    except:
        if(list(twitter_list.values())==[1 for i in twitter_list]):
            print("All of them are overused.")
            print("Rate Limit Done - Sleeping for 12 minutes.")
            for i in twitter_list:
                twitter_list[i] = 0
            time.sleep(800)
        
        twitter_list[twit] = 1
        
        if(twit==twitter):
            twit = twitter_trilok
            print("Nags Account Failed. Changing to trilok's account")
        elif(twit==twitter_trilok):
            twit = twitter
            print("Trilok's Account Failed. Changing to Nags's account")
            
        users_not_done.append(user)
    
    time.sleep(10)

    print("{}/{}".format(count,len(master_list)))


# In[15]:


len(randomk)


# In[23]:


# For fun : which players are following which other players
for i,j in players_ids.items():
    print(i, adj_dict[j])


# In[16]:


# Saving this as an object
file1 = open('followinglist.obj', 'wb') 
pickle.dump(randomk, file1)
file1.close()


# In[18]:


total_nodes = len(randomk)
adjacency = np.zeros((total_nodes, total_nodes), dtype=int)


# In[19]:


# Creating an adjacency dictionary
adj_dict = {i:[] for i in randomk}

for user,vals in randomk.items():
    for following in vals:
        if(following in master_list):
            adj_dict[user].append(following)


# In[34]:


# Dumping the adjacency matrix on disk
file1 = open('adjacency_matrix.obj', 'wb') 
pickle.dump(adj_dict, file1)
file1.close()

