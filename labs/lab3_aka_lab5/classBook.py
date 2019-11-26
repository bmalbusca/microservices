import Pyro4
"""
book 
• Author
• Title
• publication year
• Identifier

"""
@Pyro4.expose
@Pyro4.behavior(instance_mode="single")

class book(object):
    def __init__(self,author=None,title=None,publication_year=None,ID=None):
        self.author = author
        self.title = title
        self.year = publication_year
        self.identifier = ID 
    def print(self, newbook):
            print(newbook.author)
    def test(self):
        return self.author

