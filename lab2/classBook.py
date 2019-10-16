"""
book 
• Author
• Title
• publication year
• Identifier

"""


class book(object):
    def __init__(self,author=None,title=None,publication_year=None,ID=None):
        self.author = author
        self.title = title
        self.year = publication_year
        self.identifier = ID 
    def test(self):
        new = book("hey ", "dsa ", 1221, 1223)
        print(new.author)


