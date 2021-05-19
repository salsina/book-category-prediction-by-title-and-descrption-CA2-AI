from __future__ import unicode_literals
import pandas as pd
from hazm import *
import math
from itertools import islice
import matplotlib.pyplot as plt

stopword_dict = {sw:0 for sw in stopwords_list()}
stemmer = Stemmer()
lemmatizer = Lemmatizer()
cats = {0:'جامعه‌شناسی',
        1: 'داستان کوتاه',
        2:'داستان کودک و نوجوانان',
        3:'کلیات اسلام',
        4:'رمان',
        5:'مدیریت و کسب و کار'}
words_in_category_jameshenasi = {}
words_in_category_dastankutah = {}
words_in_category_kudaknojavan = {}
words_in_category_koliateslam = {}
words_in_category_roman = {}
words_in_category_kasbokar = {}
num_of_words_in_categories = [0,0,0,0,0,0]

def normalize_train(data):
    print("normalizing train file...")
    lemmitized_descriptions = {}
    i = 0
    
    for index, row in data.iterrows():
        row['description'] += row['title'] * 10
    for row in data['description']:
        tokenized_sentence = word_tokenize(row)
        new_sentence = []
        for word in tokenized_sentence:
            if word in  [':','؟','.',',','«','»','(',')','،','[',']','{','}','-','','؛', '\r', '\n']:
                continue
            if word in stopword_dict:
                continue
            word = stemmer.stem(word)
            lemmitized_word = lemmatizer.lemmatize(word)
            new_sentence.append(lemmitized_word) 
        lemmitized_descriptions[i] = tuple(new_sentence)
        i += 1
        
    return lemmitized_descriptions


def preprocess(lemmitized_descriptions, data):
    print("pre processing...")
    for i in range(len(lemmitized_descriptions)):
        for word in lemmitized_descriptions[i]:
            if data['categories'][i] == "جامعه‌شناسی" :
                num_of_words_in_categories[0] += 1
                if word in words_in_category_jameshenasi:
                    words_in_category_jameshenasi[word] += 1
                else:
                    words_in_category_jameshenasi[word] = 1
            if data['categories'][i] == "داستان کوتاه" :
                num_of_words_in_categories[1] += 1
                if word in words_in_category_dastankutah:
                    words_in_category_dastankutah[word] += 1
                else:
                    words_in_category_dastankutah[word] = 1
            if data['categories'][i] == "داستان کودک و نوجوانان" :
                num_of_words_in_categories[2] += 1
                if word in words_in_category_kudaknojavan:
                    words_in_category_kudaknojavan[word] += 1
                else:
                    words_in_category_kudaknojavan[word] = 1
            if data['categories'][i] == "کلیات اسلام" :
                num_of_words_in_categories[3] += 1
                if word in words_in_category_koliateslam:
                    words_in_category_koliateslam[word] += 1
                else:
                    words_in_category_koliateslam[word] = 1
            if data['categories'][i] == "رمان" :
                num_of_words_in_categories[4] += 1
                if word in words_in_category_roman:
                    words_in_category_roman[word] += 1
                else:
                    words_in_category_roman[word] = 1
            if data['categories'][i] == "مدیریت و کسب و کار" :
                num_of_words_in_categories[5] += 1
                if word in words_in_category_kasbokar:
                    words_in_category_kasbokar[word] += 1
                else:
                    words_in_category_kasbokar[word] = 1
                    
    
def test_datas(test_data):
    answers = []
    print("normalizing test file...")
    print("runing tests...")
    for index, row in test_data.iterrows():
        row['description'] += row['title'] 
    for desc in test_data['description']:
        probabilities = [0,0,0,0,0,0]
        tokenized_sentence = word_tokenize(desc)
        for word in tokenized_sentence:
            if word in [':','؟','.',',','«','»','(',')','،','[',']','{','}','-','','؛', '\r', '\n']:
                continue
            if word in stopword_dict:
                continue

            word = stemmer.stem(word)
            word = lemmatizer.lemmatize(word)
            if word in words_in_category_jameshenasi:
                probabilities[0] += math.log((words_in_category_jameshenasi[word]/num_of_words_in_categories[0]),10)
            else:
                probabilities[0] += math.log((1/num_of_words_in_categories[0]),10)
#                 probabilities[0] += math.log((1/10**9),10)

            if word in words_in_category_dastankutah:
                probabilities[1] += math.log((words_in_category_dastankutah[word]/num_of_words_in_categories[1]),10)
            else:
                probabilities[1] += math.log((1/num_of_words_in_categories[1]),10)
#                 probabilities[1] += math.log((1/10**9),10)

            if word in words_in_category_kudaknojavan:
                probabilities[2] += math.log((words_in_category_kudaknojavan[word]/num_of_words_in_categories[2]),10)
            else:
                probabilities[2] += math.log((1/num_of_words_in_categories[2]),10)
#                 probabilities[2] += math.log((1/10**9),10)

            if word in words_in_category_koliateslam:
                probabilities[3] += math.log((words_in_category_koliateslam[word]/num_of_words_in_categories[3]),10)
            else:
                probabilities[3] += math.log((1/num_of_words_in_categories[3]),10)
#                 probabilities[3] += math.log((1/10**9),10)

            if word in words_in_category_roman:
                probabilities[4] += math.log((words_in_category_roman[word]/num_of_words_in_categories[4]),10)
            else:
                probabilities[4] +=  math.log((1/num_of_words_in_categories[4]),10)
#                 probabilities[4] += math.log((1/10**9),10)

            if word in words_in_category_kasbokar:
                probabilities[5] += math.log((words_in_category_kasbokar[word]/num_of_words_in_categories[5]),10)
            else:
                probabilities[5] += math.log((1/num_of_words_in_categories[5]),10)
#                 probabilities[5] += math.log((1/10**9),10)

        max_num = max(probabilities)
        idx = probabilities.index(max_num)
        answers.append(cats[idx])
    
    return answers
    

def show_plot(category, ylabel):
    sorted_category = {k: v for k, v in sorted(category.items(), key=lambda item: item[1], reverse=True)}
    dict_items = sorted_category.items()
    first_five_sorted_category = list(dict_items)[:5]
    print(first_five_sorted_category)
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    words = [first_five_sorted_category[0][1],first_five_sorted_category[1][1],first_five_sorted_category[2][1],first_five_sorted_category[3][1],first_five_sorted_category[4][1]]
    counts = [first_five_sorted_category[0][0],first_five_sorted_category[1][0],first_five_sorted_category[2][0],first_five_sorted_category[3][0],first_five_sorted_category[4][0]]
    ax.bar(counts, words)
    plt.xlabel(ylabel)
    plt.show()


def show_plots():
    show_plot(words_in_category_jameshenasi, "jame shenasi")
    show_plot(words_in_category_dastankutah, "dastane kootaah")
    show_plot(words_in_category_kudaknojavan, "koodak va nojavaan")
    show_plot(words_in_category_koliateslam, "kolliaate eslaam")
    show_plot(words_in_category_roman, "romaan")
    show_plot(words_in_category_kasbokar, "kasb o kaar")    


def print_accuracy_F1():
    correct = 0
    cats_all = [0,0,0,0,0,0]
    cats_all_found = [0,0,0,0,0,0]
    cats_corrects = [0,0,0,0,0,0]
    wrongs = []
    for i in range(len(test_data)):
        if answers[i] == test_data['categories'][i]:
            correct += 1
            for idx in cats:
                if cats[idx] == test_data['categories'][i]:
                    cats_corrects[idx] += 1
        else:
            wrongs.append(test_data['title'][i])
            
        for idx in cats:
            if cats[idx] == test_data['categories'][i]:
                cats_all[idx] += 1

        for idx in cats:
            if cats[idx] == answers[i]:
                cats_all_found[idx] += 1
    print()
    macro_F1 = 0
    for i in cats:
        precision = cats_corrects[i]/cats_all_found[i]
        recall = cats_corrects[i]/cats_all[i]
        F1 = 2 * (precision * recall)/(precision + recall)
        macro_F1 += F1
        space = ""
        for j in range(22 - len(cats[i])):
            space += " "
        if i == 0:
            space+=" "
        print(cats[i],space, "-> ", "Precision:", "{:.2f}".format(100 * precision),"%,", \
                "  Recall:", "{:.2f}".format(100 * recall),"%,"\
                    "   F1:", "{:.2f}".format(100 * F1),"%")

    print("accuracy: ","{:.2f}".format(100 * correct/len(test_data)),"%")
    print("macro F1: ","{:.2f}".format(100 * macro_F1/6), "%")
    print("some wrong predictions:")
    for w in range(5):
        print(wrongs[w])
    
    
print("reading train file...")
data = pd.read_csv("books_train.csv")
lemmitized_descriptions = normalize_train(data)
preprocess(lemmitized_descriptions, data)
print("training done.")

test_data = pd.read_csv("books_test.csv")
answers = test_datas(test_data)
print("testing done.")

show_plots()
print_accuracy_F1()