from __future__ import print_function
 
import codecs
import re
import operator
############################################################################
## load the dataset
 
text = codecs.open('./wiki-600', encoding='utf-8').read()
starts = [match.span()[0] for match in re.finditer('\n = [^=]', text)]
 
articles = list()
for ii, start in enumerate(starts):
    end = starts[ii+1] if ii+1 < len(starts) else len(text)
    articles.append(text[start:end])
    
snippets = [' '.join(article[:200].split()) for article in articles]
 
#for snippet in snippets[:20]:
#    print(snippet)

articles = ["this car got the excellence award",\
         "good car gives good mileage",\
         "this car is very expensive",\
         "the company is growing with very high production",\
         "this company is financially good",
         "this company needs good management",
         "this company is reeling under losses"]   
from sklearn.feature_extraction.text import TfidfVectorizer
vocabulary = set()
for doc in articles:
    vocabulary.update(doc.split())
    
vocabulary = list(vocabulary)
tfidf = TfidfVectorizer(vocabulary=vocabulary)


tfidf.fit(articles)
tfidf.transform(articles)

final = {}
for doc in articles:
    score={}
#    print (doc)
    # Transform a document into TfIdf coordinates
    X = tfidf.transform([doc])
    for word in doc.split():
        score[word] = X[0, tfidf.vocabulary_[word]]
    sortedscore = sorted(score.items(), key=operator.itemgetter(1), reverse=True)
#    print ("\t", sortedscore)
    final[doc] = dict(sortedscore)


word = "company"
keys = []
for x in final.keys():
    if word in x:
        keys.append(x)

result = []
for x in keys:
    result.append((x,final[x][word]))
result = dict(result)
result = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
result = dict(result)
print (list(result.keys()))
