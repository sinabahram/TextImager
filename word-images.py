from stat_parser import Parser
from nltk.tree import *
import urllib2
import simplejson
from collections import OrderedDict

RETRIEVE_IMAGES = False

def extractPhrases(myTree, phrase):
    myPhrases = []
    if (myTree.node == phrase):
        myPhrases.append( myTree.copy(True) )
    for child in myTree:
        if (type(child) is Tree):
            list_of_phrases = extractPhrases(child, phrase)
            if (len(list_of_phrases) > 0):
                myPhrases.extend(list_of_phrases)
    return myPhrases

def buildImageURLs(searchTerm):
 if not RETRIEVE_IMAGES:
  return []

 urls = []
 searchTerm = searchTerm.replace(' ','%20')
 url = ('https://ajax.googleapis.com/ajax/services/search/images?' + 'v=1.0&q='+searchTerm)
 response = urllib2.urlopen(url)
 results = simplejson.load(response)
 data = results['responseData']
 dataInfo = data['results']

 for myUrl in dataInfo:
  urls.append(myUrl['unescapedUrl'])

 return urls

def buildImagesDict(phrases):
 images = OrderedDict()

 for phrase in phrases:
   images[phrase] = buildImageURLs(phrase)

 return images

def main():
 text = "The circuit design could increase efficiency by 50%."
 parser = Parser()
 tree = parser.parse(text)
 print tree
 phrasesTree = extractPhrases(tree, 'NP')
 print phrasesTree
 phrases = []
 for phrase in phrasesTree:
  phrases.append(" ".join(phrase.leaves()))

 imagesDict = buildImagesDict(phrases)
 for phrase, images in imagesDict.iteritems():
  print phrase
  print "\n".join([image for image in images])
  print

main()
