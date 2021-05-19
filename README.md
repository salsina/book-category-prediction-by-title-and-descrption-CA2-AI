# book-category-prediction-by-title-and-descrption-CA2-AI
using bayes rule to guess in which category a book is 

in this project there is a book dataset which includes 2550 books each with its title and description and the category in which it is.

The goal is to predict the categories of books in book_test.csv by their titles and descriptions.

first of all the train data must be normalized by removing the stop words and lemmatiziation and stemming. I have done this using a library named "hazm"

which is specificly for persian language.

after data normalization we must keep the words and their occuring frequency in each category.

so after that we will be able to read the data from test file and predict the category of each book.

Finally there are two methods for accuracy evaluation. one is the normal accuracy in which we calculate number of true predictions divided by all the data. The second method is 

macro-F1 for more information please check this website "https://towardsdatascience.com/multi-class-metrics-made-simple-part-ii-the-f1-score-ebe8b2c2ca1"
