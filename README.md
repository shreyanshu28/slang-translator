# README
# slang-translator

### Team members:

Anu Reddy : anu.fan5@gmail.com \
Mani Smaran Nair : manismarann@gmail.com \
Shreyansu Vyas : rk305@stud.uni-heidelberg.de \
Yanxin Jia : jiayx@hotmail.com


### Existing code fragments:

for meaning extraction of phrases, we might be using:

https://github.com/thatbrguy/Reverse-Dictionary

for emoji association, we draw insight from:

https://github.com/fabriceyhc/emoji_translate

https://github.com/anaulin/emoji-translator


### Utilized libraries:

For data processing&storage: Pandas, Elasticsearch

For language processing: nltk, gensim, spacy

See requirements.txt for further information.

### Project log (alphabetical order)

Contribution By AnuReddy:

Implementing python codes to process .json file and save into elasticsearch.
In the next stage : development of api to communicate with frontend and backend.

Contribution By Mani Smaran Nair:

Data visualization
In the next stage : Implementing the front interface and using the api developed by anureddy.

Contribution By Shreyansu Vyas:

Combining multiple datasets into one comprehensive file. (data cleaning)
In the next stage : Implementing the scraping of twitter data into the elasticsearch dataset.

Contribution By Yanxin Jia:

Written the project proposal, explored various methods for data utilization.
In the next stage : further model&algorithm implementation.

### Datasets Used (or will be utilizing):

https://github.com/muan/emojilib

https://www.kaggle.com/datasets/daphnakeidar/slangvolution?select=slang_2020_tweets.csv

https://www.kaggle.com/datasets/gowrishankarp/chat-slang-abbreviations-acronyms

https://www.kaggle.com/datasets/eliasdabbas/emoji-data-descriptions-codepoints

https://7esl.com/texting-abbreviations/

https://www.kaggle.com/datasets/therohk/urban-dictionary-words-dataset

Twitter data (API obtained, will be crawling data)

### APIs that would be in use:

Twitter, ReverseDictionary.


## Project State

We have completed the initial steps of data collection and drafted possible approaches based on the existing form of our corpus. 

### Planning State

We now have all the data&API required for the project and as they mostly require little preprocessing (except the tweets), it's ready for use. For preprocessing&word2vec training, see word2vec_model_formulation.py. The training dataset will be renewed after crawling from twitter API.

The framework of the project is thought of and partially implemented, thus it should not take much time to finish what I mention in "future planning".

### Future Planning

Quickly recall our task: to translate a formal input sentence into an informal Internet one possibility with emoji. Translation without bulky seq2seq models is difficult, but not impossible. The process of such a translation, on the other hand, would be heavily reliant on the quality and structure of our data. The datasets we now have can be described as 2 parts: 

One major part of the data is raw twitter text data that would be used for word2vec training. Based on such a training, we would be able to build associations via vector distance among similar words in the Internet context. By utilizing these connections, one would be able to perform a meaning-reliant association for words that would fit into the input context by first extracting noun/verbs from the input sentence and then perform model.wv.most_similar with them. After obtaining associated words, we would perform ES query based on the obtained word list in the emoji dataset, which has multiple keywords for one single emoji, enabling association in a broader context. Append the associated emoji to (or substitute with) the original text, then the job of an emoji translation is done.

The other part of the datasets are mostly slang-related. We already have abbreviations and their original forms (see https://www.kaggle.com/datasets/gowrishankarp/chat-slang-abbreviations-acronyms), and slangs with their meanings explained (see https://www.kaggle.com/datasets/therohk/urban-dictionary-words-dataset). Based on the above data, for a translation into slang we might: 

1. perform ES query with all possible k-shingle of the text and substitute some certain k-shingle with the corresponding (available) slang phrase. This is the easiest possible thing to implement, and since we already have the data ready, the query part would take little time. The remaining question is how to ensure accuracy of such queries, since the k-shingle and the explanation&translations we have for slangs can be phrased differently. The calculation of meaning similarity could be done using spacy built-ins, but its performance remains to be seen.

2. perform association for noun phrases in input sentence using ReverseDictionary (which would translate phrases into relevant single words), and perform queries with the obtained word list. Assign weights to these queries according to the relevancy of it (can be calculated with spacy) with the original phrase, and apply queried slangs with possibility calculated through weight value. This method can also be useful when it comes to emoji association.

Another major difference between informal&formal language is the grammar. There are large-scaled tools like grammarly for auto grammar correction. This would come into use if we are going to translate from informal text into formal ones, while parsing sentence structure according to grammar can also be applicable if we would want to for example remove the subject ("I am studying hard"->"am studying hard") to add some informal flavor when translating formal language into Internet language.

Implement the above mentioned pipeline should not take more than a week, and I would propose that the group finish a basic version of the project (with a functioning UI) before end of the year which is 12.31. While implementing there could also be timeline and stategy shifts due to precision of the proposed method.

### Architecture Description

We shall be splitting the functions drafted in translation_framework_draft.ipynb into multiple .py files which would function as the middle part between UI and ES. The aforementioned part would be stored in folder "middleware" while ES related codes would be stored separately in "Connection". We have not been tackling the UI part for now. The processing of data such as tokenization is implemented&commented alongside.

### Initial Experiments

We trained a basic word2vec model based on obtained twitter data (source: https://www.kaggle.com/datasets/daphnakeidar/slangvolution?select=slang_2020_tweets.csv) and tested its performance on multiple words.  The results display obvious twitter bias due to the small size of the corpus, as it's "most_similar" include "Kanye" with "ghost" and "god" with "coward". But the first one of the most similar words extracted have displayed generally good accuracy. By increasing dataset size, we reasonably expect higher precision. See Test_word2vec.ipynb for details.

I have described in "future planning" how the (partial) translation should function based on current utilities. The process is drafted in translation_framework_draft.ipynb. It is not formed&tested and is only a frame for further implementation up to now.

### Data Analysis

Data sources: see dataset&API part of this documentation.

Preprocessing: the twitter data requires much cleaning before usage. See word2vec_model_formulation for details. The steps include: 

1. removing hashtags and @s. This is done by converting string to list (with tokenization) and removing the word after # or @.
2. removing symbols that would not be useful for further processing. List the symbols and delete them from the tokenized list.
3. lowercase all words to decrease dimension of the data and validate the training.
4. extract emojis that cannot be correctly tokenized and tokenize them separately. Done with python library "emoji".

The input data to be translated should also require preprocessing for keyword extraction. There are two ways to extract keywords, one is to use spacy nlp().noun_chunks along with structure of verb phrases to extract all grammatical entity, another is to analyze the sentence structure with token.dep_. Both are feasible.

Basic statistics: see DataVisualization.ipynb.

Examples: see DataVisualization.ipynb.

