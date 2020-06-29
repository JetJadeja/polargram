#Database
import firebase_admin
from firebase_admin import credentials, firestore

#misc
from os import path
import json
import re


#Initialize
cred = credentials.Certificate(path.expanduser('UserFeed/Config/FireBaseConfig.json'))
firebase_admin.initialize_app(cred)
db = firestore.client()

words = []
#List of Words


def append_to_line(file):
    lines = []
    with open(file, 'r+') as text_file:
        for line in text_file:
            lines.append(line.strip('\n'))

    return lines

def no_special_chars(text):
    text = re.sub("[^a-zA-Z0-9]+", "",text)
    return text

def correct_list(original_list): #returns list with only keywords
    new_list = original_list.copy()
    #Opens our text file
    words = append_to_line(path.expanduser('UserFeed/dontinclude.txt')) #Creates a list with all the words        
    for word in new_list:
        if word in words:
            original_list.remove(word)

        else:
            original_list[original_list.index(word)] = no_special_chars(word)

    return correct_words(original_list)

def correct_words(list_edit):
    for word in list_edit:
        word_list = list(word)

        for char in word:
            if str(char).isalpha() != True:
                word_list.remove(char)
        list_edit[list_edit.index(word)] = ''.join(word_list)

    return list_edit

def findKeywords(): #Write CSV File
    dict_storage = {}
    for user in db.collection(u'users').stream():#Iterate over users
        for post in db.collection(u'users').document(user.id).collection('posts').stream():
            post_dict = {}
            postID = post.id #Iterate over the documents
            post_to_dict = post.to_dict() #Making the post a dictionary

            postTitle = post_to_dict['title'] #Store Post Title
            postTitle = postTitle.split(' ') #Split Post Title by spaces

            for word in postTitle: #Make all words lowercase
                postTitle[postTitle.index(word)] = word.lower()

            postTitle = correct_list(postTitle) #Removes unneeded words
            post_dict['keywords'] = postTitle
            post_dict['author'] = user.id
            post_dict['post_id'] = post.id
            dict_storage[post.id] = post_dict

        with open('UserFeed/Data/posts.json') as jpf:
            jpf.truncate(0)
            json.dump(dict_storage, jpf)

    return dict_storage

def findIntersections(list_one, list_two):
    return len(set(list_one) & set(list_two))

def find_sim(keywords):
    sim_dict = {}
    file = 'UserFeed/Data/posts.json'
    with open(json_file) as file:
        posts_dict = json.load(file)

    for post in posts_dict:
        posts_keyword = posts_dict[post]['keywords']

        similarities = findIntersections(keywords, posts_keyword)
        if similarities >= 1:
            sim_dict[post] = similarities


    return sim_dict



def get_following_posts(user):
    for user in db.collection(u'users').document(user):
        pass


    





def to_lower(edit_list):
    for word in edit_list:
        edit_list[edit_list.index(word)] = word.lower()
    edit_list = list(dict.fromkeys(edit_list))

    return edit_list




def find_favorite_keywords():
    final_dict = {}
    posts = read_json('UserFeed/Data/posts.json')
    for user in db.collection(u'users').stream():#Iterate over users
        user_keywords = []

        for post in db.collection(u'users').document(user.id).collection('posts').stream():
            post = post.to_dict() #Making the post a dictionary

            postTitle = post['title'] #Store Post Title
            postTitle = postTitle.split(' ') #Split Post Title by spaces

            

        user_dict = user.to_dict()
        liked_posts = user_dict['shaken_posts']

        for post in liked_posts:
            liked_post = posts[post]
            keywords = liked_post['keywords']

            for word in keywords:
                user_keywords.append(word)

        user_keywords = correct_list(user_keywords)

        final_dict[user.id] = to_lower(user_keywords)


    return final_dict

def dict_to_json(dictionary):
    with open(path.expanduser('UserFeed/Data/users.json', 'w')) as fp:
        fp.truncate(0)
        json.dump(dictionary, fp)


def read_json(json_file):
    with open(json_file) as file:
        json.load(file)


dict_to_json(find_favorite_keywords())









            

