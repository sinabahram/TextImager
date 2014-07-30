#!/usr/bin/env python
# Date Created: Tue Jul 29 21:22:43 EDT 2014
# Description: Generate a series of relevant images from a sentence.

# Standard libraries
import simplejson
import sys
import urllib2

# External libraries
# NOTE: To install these on Linux or OS X, make sure
# that you have Pip (https://pip.pypa.io/en/latest/installing.html)
# and then try "sudo pip install --upgrade nltk"
import nltk # 2.0.4

class TextImager(object):
    """Class to convert text to a series of relevant images."""

    # Constants
    RETRIEVE = True # Retrieve images from Google?
    SEARCH_PRE = "https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q="

    @staticmethod
    def showUsage():
        """Show command-line usage of this class."""
        print "Usage:", sys.argv[0], "TEXT_PHRASE"

    def __init__(this):
        """Configure the NLP tools."""
        this.parser = nltk.RegexpParser("NP: {<JJ.*|PDT|VBG|VBN|RB.*>*(<CD|PRP|NN.*>)+}")

    def getImageURL(this, words):
        """Retrieve the most relevant image for the given keywords.

        Args:
            words: (listof(word)) List of words as strings 

        Returns:
            Image URL as a string
        """
        # Initialize a default image (250x250, white on white)
        retURL = "http://placehold.it/250/ffffff/ffffff"

        # Short-circuit if we're just testing
        if not this.RETRIEVE:
            return retURL

        # Create our query string
        query = urllib2.quote(" ".join(words))

        # Send it and parse the JSON response
        response = urllib2.urlopen(this.SEARCH_PRE + query)
        json = simplejson.load(response)
        
        # Use our top image, if we have one
        try:
            return json["responseData"]["results"][0]["unescapedUrl"]
        except: # Use our default image
            return retURL

    def getPhrases(this, text):
        """Parse out the interesting phrases from the given text.

        Args:
            text: (string) Raw text sentence or utterance

        Returns:
            List of phrases as word (string) lists
        """
        # Use our parser to label noun phrases (NP)
        words = nltk.word_tokenize(text.lower()) # Parsers often use case!
        tagged = nltk.pos_tag(words)
        tree = this.parser.parse(tagged)

        # Parse out just the NP chunks
        retList = []
        for branch in tree.subtrees():
            if branch.node == "NP":

                # Get the node values (i.e. the words)
                retList.append([x[0] for x in branch.leaves()])

        return retList
    
if __name__ == "__main__":

    # Check for required input: prog + text
    if len(sys.argv) < 2:
        TextImager.showUsage()
        sys.exit(1)

    # Combine the text arguments
    text = " ".join(sys.argv[1:])

    # Initialize the imager
    engine = TextImager()

    # Retrieve the list of phrases
    phrases = engine.getPhrases(text)

    # DEBUG: Show the phrases!
    print phrases

    # Retrieve the list of images
    images = [engine.getImageURL(phrase) for phrase in phrases]

    # Show the URLs
    print text + ":"
    print "\n".join(images)
