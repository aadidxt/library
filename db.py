import time
import pymongo
import datetime

# Establish a connection to the MongoDB database
client = pymongo.MongoClient('mongodb+srv://dixitabhay52:aditya@cluster0.an2xlfa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['aadi']
col1 = db["Available books"]
col2 = db['issued books Books']

def add_book(id, bName, Aname):
    """
    Add a book to the library.
    
    Parameters:
    id (int): The ID of the book.
    bName (str): The name of the book.
    Aname (str): The name of the author.
    """
    query = {"_id": id}
    book = col1.count_documents(query)

    if book > 0:
        print(f'Book with ID {id} is already in the library')
    else:
        now = datetime.datetime.now()
        book = {
            "_id": id,
            "Book Name": bName,
            "Author Name": Aname,
            "Date of Add": now.strftime("%d-%m-%y"),
            "Time of add": now.strftime("%H-%M-%S")
        }
        col1.insert_one(book)
        print(f'Book "{bName}" with id "{id}" added successfully to the library')

def remove_book(id, bName):
    """
    Remove a book from the library.
    
    Parameters:
    id (int): The ID of the book.
    bName (str): The name of the book.
    """
    query = {"_id": id}
    book = col1.count_documents(query)
    if book > 0:
        col1.delete_one(query)
        print("Deleted")
    else:
        print('There is no book with this ID in this library')

def view_book():
    """
    View all books available in the library.
    """
    books = col1.find()
    print("ID\tBook\t\tAuthor")
    for i in books:
        print(f'{i["_id"]}\t{i["Book Name"]}\t{i["Author Name"]}')
    book_count = col1.find()
    book_count = len(list(book_count))
    print("\n\n")
    print(f'Total books in the library available - {book_count}')

def update_book(id, bName=None, Aname=None):
    """
    Update details of a book in the library.
    
    Parameters:
    id (int): The ID of the book.
    bName (str): The new name of the book (optional).
    Aname (str): The new name of the author (optional).
    """
    query = {'_id': id}
    changes = {}

    if bName:
        changes['Book Name'] = bName
    if Aname:
        changes['Author Name'] = Aname

    if changes:
        col1.update_one(query, {"$set": changes})
        print('Updated successfully')
    else:
        print('No changes were made')

def find_book(bName, Aname=None):
    """
    Find a book in the library by name and optionally by author.
    
    Parameters:
    bName (str): The name of the book.
    Aname (str): The name of the author (optional).
    """
    query = {}
   
    if bName:
        query['Book Name'] = bName
    if Aname:
        query['Author Name'] = Aname

    try:
        book = col1.find(query)
        book = list(book)
        if book:
            for i in book:
                print(f'{i["_id"]} - {i["Book Name"]} - {i["Author Name"]}')
        else:
            print('No book found')
    except Exception as e:
        print('Some error occurred')

def issue_book(id, bName, Aname):
    """
    Issue a book to a student.
    
    Parameters:
    id (int): The ID of the book.
    bName (str): The name of the book.
    Aname (str): The name of the author.
    """
    query = {
        "_id": id,
        "Book Name": bName,
        "Author Name": Aname
    }

    book_count = col1.count_documents(query)

    if book_count > 0:
        print('Book found')

        col1.delete_one(query)
    
        now = datetime.datetime.now()
        try:
            stdid = input("Enter student ID: ")
            stdname = input('Enter your name: ')
            course = input('Enter your course: ')
            phn = int(input('Enter your contact number: '))
        except Exception:
            print('Fill all fields')
        
        query1 = {
            "_id": id,
            "Book Name": bName,
            "Author Name": Aname,
            "Student ID": stdid,
            "Student Name": stdname,
            "Course": course,
            "Contact no.": phn,
            "Date": now.strftime("%d-%m-%y"),
            "Time": now.strftime("%H-%M-%S")
        }

        col2.insert_one(query1)
        print(f'Book issued successfully to {stdname} of {course} with Student ID {stdid}')
    else:
        print('Sorry, the book you want is not available')

def view_issued_books():
    """
    View all issued books.
    """
    books = col2.find()
    print("id\tBook Name\tAuthor Name\tStudent ID\t\tStudent Name\t\tCourse\t\tTime\t\tDate\t\tContact No.")
    for book in books:
        print(f"{book['_id']}\t{book['Book Name']}\t{book['Author Name']}\t{book['Student ID']}\t\t{book['Student Name']}\t\t{book['Course']}\t{book['Date']}\t{book['Time']}\t{book['Contact no.']}")
    book_count = col2.find()
    book_count = len(list(book_count))
    print("\n\n")
    print(f'Total issued books - {book_count}')

def return_book(id, bName, Aname):
    """
    Return a book to the library.
    
    Parameters:
    id (int): The ID of the book.
    bName (str): The name of the book.
    Aname (str): The name of the author.
    """
    query = {
        "_id": id,
        "Book Name": bName,
        "Author Name": Aname
    }

    book_count = col2.count_documents(query)

    if book_count > 0:
        add_book(id, bName, Aname)
        col2.delete_one(query)
    else:
        print('Sorry, this book is not in our list of issued books')

def check_issued_books_by_std(stdid):
    """
    Check books issued by a specific student.
    
    Parameters:
    stdid (str): The ID of the student.
    """
    query = {"Student ID": stdid}
    book_count = col2.find()
    book_count = list(book_count)
    if book_count:
        books = col2.find(query)
        print(f'Student ID - {stdid}\nStudent Name - {book_count[0]["Student Name"]}\nCourse - {book_count[0]["Course"]}')
        print('ID\tBook Name\tAuthor Name')
        for book in books:
            print(f'{book["_id"]}\t{book["Book Name"]}\t{book["Author Name"]}')

# Main loop to handle user interaction
while True:
    print("""
    Welcome to the Library!

    1. Add Book to the library
    2. Remove Book from the library
    3. Update Book
    4. View Books
    5. Find Book
    6. Issue Book
    7. Return Book
    8. View issued Books
    9. Find book by Student ID
    0. Exit
    """)

    try:
        choice = int(input("Enter your choice (1-9 or 0 to exit): "))
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 9 or 0 to exit.")
        continue  # Skip to the next iteration of the loop

    match choice:
        case 1:
            try:
                id = int(input("Enter ID number: "))
                book_name = input("Enter book name: ")
                author_name = input("Enter author name: ")
                add_book(id, book_name, author_name)
            except ValueError:
                print("Invalid input for ID or book name. Please enter numbers for ID and strings for book and author names.")
        case 2:
            try:
                id = int(input("Enter ID number: "))
                book_name = input("Enter book name (optional): ")
                remove_book(id, book_name)
            except ValueError:
                print("Invalid input for ID. Please enter a number.")
        case 3:
            try:
                id = int(input("Enter ID number: "))
                book_name = input("Enter book name: ")
                author_name = input("Enter author name: ")
                update_book(id, book_name, author_name)
            except ValueError:
                print("Invalid input for ID or book name. Please enter numbers for ID and strings for book and author names.")
        case 4:
            view_book()
        case 5:
            book_name = input("Enter book name to search: ")
            find_book(book_name)
        case 6:
            id = int(input('Enter ID of book: '))
            book_name = input('Enter book name: ')
            author_name = input('Enter author name: ')
            issue_book(id, book_name, author_name)
        case 7:
            id = int(input('Enter ID of book: '))
            book_name = input('Enter book name: ')
            author_name = input('Enter author name: ')
            return_book(id, book_name, author_name)
        case 8:
            view_issued_books()
        case 9:
            stdid = input('Enter the student ID: ')
            check_issued_books_by_std(stdid)
        case 0:
            print("Exiting the library. Thank you for using our services!")
            break
        case _:
            print("Invalid choice. Please enter a number between 1 and 9 or 0 to exit.")
    time.sleep(2)
