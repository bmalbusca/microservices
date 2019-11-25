class book:
    def __init__(self, author, title, year, b_id):
        self.author = author
        self.title = title
        self.year = year
        self.id = b_id

    def __str__(self):
        return "%d - %s - %s - %s" % (self.id, self.author, self.title, self.year)

