from peter_portal import get_courses, get_grades, get_professors
import tweepy
import time

consumer_key = 'xxxx'
consumer_secret  = 'xxxx'
access_token = 'xxxxxxxx'
access_token_secret = 'xxxx'
bearer_token = 'xxxxxxxx'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# test credentaials
try:
    api.verify_credentials()
    print("Authentication Successful")
except:
    print("Authentication Error")

client = tweepy.Client(bearer_token = bearer_token,
                     consumer_key = consumer_key,
                     consumer_secret = consumer_secret,
                     access_token = access_token,
                     access_token_secret = access_token_secret, wait_on_rate_limit=True)

# get user ID
user_id = client.get_user(username = 'tweeter_b0t', user_auth=True).data.id

# store all IDs sceen
# DEV: USE 1500964252013580289 for testing
seen_ids = [1500964252013580289]

def create_tweet():
   # get all mentions of the user since the last since ID
   last_seen_id = seen_ids[-1]
   mentions = api.mentions_timeline(since_id = last_seen_id)
   # mentions = client.get_users_mentions(id = user_id, since_id = last_seen_id, user_auth = True).data
   
   if mentions:
      for mention in mentions:
         # store the last instance of tweet so we know not to use it again
         last_seen_id = mention.id
         seen_ids.append(last_seen_id)
         
         # remove @username from the text
         mention_list = mention.text.split(' ')

         # get the command from the tweet
         command = mention_list[1:][0]

         if command == '!Professors':
            department = mention_list[2:][0]
            course_number = mention_list[2:][1]
            professors = '\n'.join(list(get_professors(department, course_number)))

            try:
               # reply to the tweet
               status = 'Professor(s) teaching this course in 2022 Spring:\n\n' + professors

               api.update_status(status = status, in_reply_to_status_id = mention.id, auto_populate_reply_metadata=True)
               print("Tweet Creation Successful!")
            except:
               # in case it is a duplicate tweet
               print("Retrieving Tweets...")
         elif command == '!Courses':
            first_name = mention_list[2:][0]
            last_name = mention_list[2:][1]
            courses = '\n'.join(get_courses(first_name, last_name))
            
            try:
               # reply to the tweet
               status = 'Course(s) taught by Professor:\n\n' + courses

               # handle the cacse if the tweet exceeds max length
               if len(status) > 280:
                  status = status[0:280]
               
               api.update_status(status = status, in_reply_to_status_id = mention.id, auto_populate_reply_metadata=True)
               print("Tweet Creation Successful!")
            except:
               # in case it is a duplicate tweet
               print("Retrieving Tweets...")
         elif command == '!Grades':
            first_name = mention_list[2:][0]
            last_name = mention_list[2:][1]
            department = mention_list[2:][2]
            course_number = mention_list[2:][3]
            year, quarter, grades = get_grades(first_name + ' ' + last_name, department, course_number)
            
            try:
               # reply to the tweet
               status = 'Grade Distribution for ' + quarter + ' ' + str(year) + ':\n\nAverage GPA: {}\nAs: {}\nBs: {}\nCs: {}\nDs: {}\nFs: {}'.format(grades['average_gpa'], grades['sum_grade_a_count'], grades['sum_grade_b_count'], grades['sum_grade_c_count'], grades['sum_grade_d_count'], grades['sum_grade_f_count'])
               
               api.update_status(status = status, in_reply_to_status_id = mention.id, auto_populate_reply_metadata=True)
               print("Tweet Creation Successful!")
            except:
               # in case it is a duplicate tweet
               print("Retrieving Tweets...")

while True:
   create_tweet()
   time.sleep(5)

   


   



