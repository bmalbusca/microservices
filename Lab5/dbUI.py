#!/usr/bin/env python


class dbUI:
        def __init__(self, db):
                self.db = db
        def menu(self):

	
                exit = False
                while not exit:
                        l = input("add show listall listauthor listyear quit?")
                        l = l.split()
                
                        if len(l)==1:
                                command = l[0].upper()
                                if command=='QUIT':
                                        exit = True
                                elif command == 'ADD':
                                        l = input('Insert author title and date separated by # :\n')
                                        processed_line = l.split('#')
                                        if len(processed_line) ==3:
                                                print ('%s %s %s'% (processed_line[0], processed_line[1], processed_line[2]))
                                                self.db.addBook(processed_line[0], processed_line[1], int(processed_line[2]))
                                elif command == 'SHOW':
                                        l = input('Insert id :\n')
                                        processed_line = l.split()
                                        print (processed_line[0])
                                        if len(processed_line) ==1:
                                                b = self.db.showBook(int(processed_line[0]))
                                                print (b)
                                elif command == 'LISTALL':
                                        b_list = self.db.listAllBooks()
                                        for b in b_list:
                                                print(b)
                                elif command == 'LISTAUTHOR':
                                        l = input('Insert name :\n')
                                        processed_line = l.split()
                                        print (processed_line[0])
                                        if len(processed_line) ==1:
                                                b_list = self.db.listBooksAuthor(processed_line[0])
                                                for b in b_list:
                                                        print(b)
                                elif command == 'LISTYEAR':
                                        l = input('Insert year :\n')
                                        processed_line = l.split()
                                        print (processed_line[0])
                                        if len(processed_line) ==1:
                                                b_list = self.db.listBooksYear(int(processed_line[0]))
                                                for b in b_list:
                                                        print(b)
                                elif command == 'LISTYEAR':
                                        exit = True
                        
    

if __name__=="__main__":
    main() 
