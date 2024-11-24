#import pytest library
import pytest

#import matplotlib library for graph
import matplotlib.pyplot as plt

#import StringIO for mock file objects
from io import StringIO

#import classes from project3 for testing
from project3 import Scraper, Analyzer, Graph

#testing to make sure urls are able to be fetched
def test_get_urls(monkeypatch):
    #create a fake function to replace open and avoid file writes
    def mock_open(filepath, mode, encoding=None):
        #return a mock file object
        mock_file = StringIO("http://example.com\nhttp://ebay.com\n")
        return mock_file

    #makes it so open is replaced with mock_open
    monkeypatch.setattr("builtins.open", mock_open)

    #creating file, creating instance of Scrapper, and calling get_urls()
    test_urls_file = "test_urls.txt"
    scraper = Scraper(test_urls_file)
    urls = scraper.get_urls()
    
    #check to make sure actual output meets expected output
    assert urls == ["http://example.com\n", "http://ebay.com\n"]

#checking that ollama is able to give a positive response
def test_positive_analyze_comments(monkeypatch):
    #create a fake function to replace open and avoid file writes
    def mock_open(filepath, mode, encoding=None):
        #return a mock file object
        mock_file = StringIO()
        return mock_file

    #makes it so open is replaced with mock_open
    monkeypatch.setattr("builtins.open", mock_open)

    #creating instance of Analyzer and calling analyze_comments()
    analyzer = Analyzer()
    result = analyzer.analyze_comments("very happy!", "pos_test")

    #check to make sure actual output meets expected output
    assert result == "positive"

#checking that ollama is able to give a negative response
def test_negative_analyze_comments(monkeypatch):
    #create a fake function to replace open and avoid file writes
    def mock_open(filepath, mode, encoding=None):
        #return a mock file object (you can return a StringIO object, for example)
        mock_file = StringIO()
        return mock_file

    #makes it so open is replaced with mock_open
    monkeypatch.setattr("builtins.open", mock_open)
    
    #creating instance of Analyzer and calling analyze_comments()
    analyzer = Analyzer()
    result = analyzer.analyze_comments("very mad", "neg_test")

    #check to make sure actual output meets expected output
    assert result == "negative"

#checking that ollama is able to give a neutral response
def test_neutral_analyze_comments(monkeypatch):
    #create a fake function to replace open and avoid file writes
    def mock_open(filepath, mode, encoding=None):
        #return a mock file object (you can return a StringIO object, for example)
        mock_file = StringIO()
        return mock_file

    #makes it so open is replaced with mock_open
    monkeypatch.setattr("builtins.open", mock_open)
    
    #creating instance of Analyzer and calling analyze_comments()
    analyzer = Analyzer()
    result = analyzer.analyze_comments("could be better could be worse", "neutral_test")

    #check to make sure actual output meets expected output
    assert result == "neutral"

#testing to make sure it is able to create a graph
def test_plot():
    #creates insantce of graph and initialize test values for categories, pos_values, neg_value, and neutral_values
    graph = Graph()
    categories = ["1", "2", "3", "4"]
    pos_values = [2, 6, 7, 9]
    neg_values = [4, 1, 8, 4]
    neutral_values = [9, 2, 5, 7]

    #call plot()
    graph.plot(categories, pos_values, neg_values, neutral_values)

    #check the number of bars drawn (3 bars per category)
    bars = plt.gca().patches  #all bars are stored in patches

    #check to make sure actual output meets expected output
    assert len(bars) == 12  #3 bars for each sentiment (positive, negative, neutral)