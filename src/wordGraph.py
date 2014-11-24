from collections import defaultdict
import sqlite3
import networkx as nx
import matplotlib.pyplot as plt
import sys

def text_format(text):
    text = text.replace("&amp;","&")
    text = text.replace("&gt;",">")
    text = text.replace("&lt;","<")
    return text

def correct_position (matrix, wordA, wordB):

    try:
        matrix[wordA][wordB]
        return [wordA, wordB]
    except:
        pass

    try:
        matrix[wordB][wordA]
        return [wordB, wordA]
    except:
        pass
    return None

def create_position (matrix, wordA, wordB):
    matrix [wordA] [wordB] = 0
    return [wordA, wordB]
    
def bound (): 
    c.execute("SELECT count(*) FROM TWEETS")
    result = c.fetchone()
    tweets = result[0]
    return tweets * float(sys.argv[1])

if sys.argv[1] is None:
    print "I need a percentage (number between 0 and 1) as an argument"
    sys.exit()
    

conn = sqlite3.connect('db/tweetBank.db')

c = conn.cursor()

# Creation of the matrix
word_matrix = defaultdict(dict)

c.execute("SELECT ID FROM TWEETS")
tweet_list = [record[0] for record in c.fetchall()]

print "Reading from the database..."

for tweet in tweet_list:
    c.execute ("SELECT WORD FROM WORDS WHERE ID =%i"
               % (tweet))
    words = [text_format(record[0]) for record in c.fetchall()]
    
    for word in words:
        words.remove(word)
        for rest_of_the_words in words:
            correct_positions = correct_position (word_matrix, word, rest_of_the_words)
            if correct_positions is None:
                correct_positions = create_position (word_matrix, word, rest_of_the_words)
            word_matrix [correct_positions[0]] [correct_positions[1]] += 1

print "Creating the graph..."

graph = nx.Graph()
edge_labels = {}

for word in word_matrix:
    for other_word in word_matrix[word]:
        if word_matrix[word][other_word] > bound():
            graph.add_edge(word,other_word)
            graph.node[other_word]['word']=other_word
            edge_labels [(word,other_word)] = word_matrix[word][other_word]
            # print ("%s + %s = %i" %(word, other_word, word_matrix[word][other_word] ))
    try:    
        graph.node[word]['word']=word
    except:
        pass

# Closing the connection
conn.close()

pos=nx.spring_layout(graph)

nx.draw(graph, pos)
nx.draw_networkx_edge_labels(graph,pos,edge_labels=edge_labels)
node_labels = nx.get_node_attributes(graph,'word')
nx.draw_networkx_labels(graph, pos, labels = node_labels)

plt.show()
