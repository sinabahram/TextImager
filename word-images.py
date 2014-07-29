from stat_parser import Parser
from nltk.tree import *
import urllib2
import simplejson
from collections import OrderedDict

# This flag simply toggles whether to go out and do the Google image search or not
# It's False now so as to allow for testing of NLP stuff first
RETRIEVE_IMAGES = True

# This function came from http://www.monlp.com/2012/01/20/extracting-noun-phrases-from-parsed-trees/
# I modified it a bit for readability
# I'm just using it to extract the noun phrases from the parse tree
def extractTaggedPhrases(tree, tag):
 phrases = []
 if (tree.node == tag):
  phrases.append( tree.copy())
 for child in tree:
  if (type(child) is Tree):
   listOfPhrases = extractTaggedPhrases(child, tag)
   if (len(listOfPhrases) > 0):
    phrases.extend(listOfPhrases)
 return phrases

# This function takes in a search term and returns four Google image URLs for it
def buildImageURLs(searchTerm):
# Just return an empty array if we don't need to bother retrieving images. This insures code that depends on this function continues to work.
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

# This function takes in an array of phrases and calls buildImageURLs on each one, returning the results in a OrderedDict with the phrase as the key
def buildImagesDict(phrases):
 images = OrderedDict()

 for phrase in phrases:
   images[phrase] = buildImageURLs(phrase)

 return images

# I've stuffed everything else in here for the time being
def main():
 text = "Smoking Mothers May Alter the DNA of Their Children."
 parser = Parser()
 tree = parser.parse(text)
 print "Parse Tree:\n"+str(tree)+"\n"
 phrasesTree = extractTaggedPhrases(tree, 'NP')
 print "Extracted Phrases:\n"+str(phrasesTree)+"\n"
 phrases = []
 for phrase in phrasesTree:
  phrases.append(" ".join(phrase.leaves()))

 imagesDict = buildImagesDict(phrases)
 for phrase, images in imagesDict.iteritems():
  print phrase+":"
  print "\n".join([image for image in images])
  print

if __name__ == "__main__":
 main()
