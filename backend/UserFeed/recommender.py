#Keywords
from nltk.corpus import wordnet

#Storage
import json

from Data import dict_to_json, find_sim, findKeywords

def findSynonyms(names):
    finalSynoyms = []
    for each in names:
        finalSynoyms.append(each.lower())
        word = wordnet.synsets(each)

        for syn in word:
            for synonym in syn.lemmas():
                finalSynoyms.append(synonym.name().lower())

    return finalSynoyms

def splitWords(change_list):
    new_list = change_list.copy()
    for word in change_list:

        x = word.split('-')
        if len(x) > 1:
            for i in x:
                new_list.append(i)

        x = word.split('_')
        if len(x) > 1:
            for i in x:
                new_list.append(i)

    return list(dict.fromkeys(new_list))

def findIntersections(list_one, list_two):
    return len(set(list_one) & set(list_two))


def find_similar_keywords(dictionary):
    for user in dictionary:
        user_keywords = dictionary[user]
        changed_keywords = user_keywords.copy()


        for word in user_keywords:
            for synonym in findSynonyms(word):

                changed_keywords.append(synonym)
        dictionary[user] = changed_keywords

    return dictionary

def read_json(json_file):
    with open(json_file) as file:
        return json.load(file)



def recommender(user):
    reccomended_posts = []
    users = read_json('UserFeed/Data/users.json')
    target_user_keywords = users[user]
    similar_posts = find_sim(target_user_keywords)

    for post in similar_posts:
        reccomended_posts.append(post)

    reccomended_posts = sorted(reccomended_posts, key=similar_posts.get)

    return reccomended_posts



dict_to_json(find_similar_keywords(read_json('UserFeed/Data/users.json')))
findKeywords()
print(recommender('cLINlzZvtGfSdSRiepccihurFQ72'))



