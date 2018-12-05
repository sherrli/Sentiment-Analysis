# Implement the bag of words model for feature extraction, using nltk's countvectorizer package.
# Includes timer for cleaning and training time.

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
import cleaning
import timeit

# You must un-tokenize the words back into phrases before running the model.
def untokenize(texts):
    docs = []
    for doc in texts:
        temp = ""
        for word in doc:
            temp += word + " "
        docs.append(temp)
    return docs

# MAIN -----------------------------------------------

# Get data
phrases = cleaning.read_data("train.csv", "Phrase")
labels = cleaning.read_data("train.csv", "Sentiment")

# Tokenize and clean
start_time_clean = timeit.default_timer()
cleaned = cleaning.tokenize_data(phrases)
# cleaned = stem_data(cleaned)
result = cleaning.filter_data(cleaned)
elapsed_time_clean = timeit.default_timer() - start_time_clean
print("Cleaning finished in " + str(elapsed_time_clean) + " seconds")


# Bag of Words model to extract features.
start_time_extract = timeit.default_timer()
vect = CountVectorizer(min_df=2, ngram_range=(1, 30))
X_train = vect.fit(untokenize(result)).transform(untokenize(result))
elapsed_time_extract = timeit.default_timer() - start_time_extract
print("Feature extracting finished in " + str(elapsed_time_extract) + " seconds")


# Train logistic regression model with built-in K-fold CV.
start_time_train = timeit.default_timer()
param_grid = {'C': [0.001, 0.01, 0.1, 1, 10]}
grid = GridSearchCV(LogisticRegression(), param_grid, cv=5)
grid.fit(X_train, labels)
elapsed_time_train = timeit.default_timer() - start_time_train
print("Training finished in " + str(elapsed_time_train) + " seconds")

# Print Cross Validation estimates and optimal parameters.
print("Best cross-validation score: {:.2f}".format(grid.best_score_))
print("Best parameters: ", grid.best_params_)
print("Best estimator: ", grid.best_estimator_)

# Creates a n by m word matrix of n phrases and m unique words.
# vect = CountVectorizer(max_features=1000)
# X = vect.fit_transform(data).toarray()
# print(X)

# Output: number of times each unique word appears in each phrase
# [[0 1 0 0]
#  [0 0 1 0]
#  [1 0 0 0]
#  [0 0 0 1]]