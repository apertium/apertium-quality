# import punkt
import nltk.tokenize.punkt
 
# Make a new Tokenizer
tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()
 
# Read in trainings corpus (one example: Slovene)
import codecs
text = codecs.open("slovene.plain","Ur","iso-8859-2").read()
 
# Train tokenizer
tokenizer.train(text)
 
# Dump pickled tokenizer
import pickle
out = open("slovene.pickle","wb")
pickle.dump(tokenizer, out)
out.close()
