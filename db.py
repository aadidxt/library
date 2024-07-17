
import pymongo 
import datetime

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['aadi']
col1 = db["library"]

def add_book(isbn,bName,Aname):

    now = datetime.datetime.now()

    book = {
        "isbn" : isbn,
        "Book Name" : bName,
        "Author Name" : Aname,
        "Date of Add" : now.strftime("%d-%m-%y"),
        "Time of add" : now.strftime("%H-%M-%S")           

    }

    col1.insert_one(book)
    print(f'Book "{bName}" with isbn "{isbn}" added successfully')



def remove_book(isbn,bName):
    query = {"isbn" : isbn}
    col1.delete_many(query)
    print("deleted")

def view_book():
    books = col1.find()
    print("BOOK\t\tAuthor\t\tisbn")
    for i in books:
        print(f'{i["Book Name"]}\t{i["Author Name"]}\t{i["isbn"]}')

def update_book(isbn,bName=None,Aname=None):
    query = {'isbn' : isbn}
    changes = {}

    if bName:
        changes['Book Name'] = bName
    if Aname:
        changes['Author Name'] = Aname

    if changes:
        col1.update_one(query,{"$set" : changes})
        print('updated succesfully')
    else:
        print('no changes are made')

def find_book(bName,Aname=None):
    query={}
    # if isbn:
    #     query['isbn'] = isbn
    if bName:
        query['Book Name'] = bName
    if Aname:
        query['Author Name'] = Aname

    try: 
        book = col1.find(query)
        book=list(book)
        if book:
            for i in book:
                print(f'{i["isbn"]} - {i["Book Name"]} - {i["Author Name"]}')
        else:
            print('no book found')
    except Exception as e:
        print('some error occured')

    


while True:
    print("""
    Welcome to the Library!

    1. Add Book
    2. Remove Book
    3. Update Book
    4. View Books
    5. Find Book
    0. Exit
    """)

    try:
        choice = int(input("Enter your choice (1-5 or 0 to exit): "))
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 5 or 0 to exit.")
        continue  # Skip to the next iteration of the loop

    match choice:
        case 1:
            try:
                isbn = int(input("Enter ISBN number: "))
                book_name = input("Enter book name: ")
                author_name = input("Enter author name: ")
                add_book(isbn, book_name, author_name)
            except ValueError:
                print("Invalid input for ISBN or book name. Please enter numbers for ISBN and strings for book and author names.")
        case 2:
            try:
                isbn = int(input("Enter ISBN number (or leave blank to search by name): "))
                book_name = input("Enter book name (optional): ")
                remove_book(isbn, book_name)
            except ValueError:
                print("Invalid input for ISBN. Please enter a number.")
        case 3:
            try:
                isbn = int(input("Enter ISBN number: "))
                book_name = input("Enter book name: ")
                update_book(isbn, book_name)
            except ValueError:
                print("Invalid input for ISBN or book name. Please enter numbers for ISBN and strings for book and author names.")
        case 4:
            view_book()
        case 5:
            book_name = input("Enter book name to search: ")
            find_book(book_name)
        case 0:
            print("Exiting the library. Thank you for using our services!")
            break
        case _:
            print("Invalid choice. Please enter a number between 1 and 5 or 0 to exit.")        
