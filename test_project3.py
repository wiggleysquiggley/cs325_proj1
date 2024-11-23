import pytest

import matplotlib.pyplot as plt

from io import StringIO

from project3 import Scraper, Analyzer, Graph

def test_get_urls(monkeypatch):
    # Create a fake function to replace open and avoid file writes
    def mock_open(filepath, mode, encoding=None):
        # Return a mock file object (you can return a StringIO object, for example)
        mock_file = StringIO("http://example.com\nhttp://ebay.com\n")
        return mock_file

    monkeypatch.setattr("builtins.open", mock_open)

    test_urls_file = "test_urls.txt"
    scraper = Scraper(test_urls_file)
    urls = scraper.get_urls()
    
    assert urls == ["http://example.com\n", "http://ebay.com\n"]

def test_positive_analyze_comments(monkeypatch):
    def mock_open(filepath, mode, encoding=None):
        # Return a mock file object (you can return a StringIO object, for example)
        mock_file = StringIO()
        return mock_file

    monkeypatch.setattr("builtins.open", mock_open)

    analyzer = Analyzer()
    result = analyzer.analyze_comments("very happy!", "pos_test")

    assert result == "positive"

def test_negative_analyze_comments(monkeypatch):
    def mock_open(filepath, mode, encoding=None):
        # Return a mock file object (you can return a StringIO object, for example)
        mock_file = StringIO()
        return mock_file

    monkeypatch.setattr("builtins.open", mock_open)
    
    analyzer = Analyzer()
    result = analyzer.analyze_comments("very mad", "neg_test")

    assert result == "negative"

def test_neutral_analyze_comments(monkeypatch):
    def mock_open(filepath, mode, encoding=None):
        # Return a mock file object (you can return a StringIO object, for example)
        mock_file = StringIO()
        return mock_file

    monkeypatch.setattr("builtins.open", mock_open)
    
    analyzer = Analyzer()
    result = analyzer.analyze_comments("could be better could be worse", "neutral_test")

    assert result == "neutral"

def test_plot():
    graph = Graph()
    categories = ["1", "2", "3", "4"]
    pos_values = [2, 6, 7, 9]
    neg_values = [4, 1, 8, 4]
    neutral_values = [9, 2, 5, 7]

    graph.plot(categories, pos_values, neg_values, neutral_values)

    # Check the number of bars drawn (3 bars per category)
    bars = plt.gca().patches  # All bars are stored in patches
    assert len(bars) == 12  # 3 bars for each sentiment (positive, negative, neutral)