import pandas as pd

print(pd.__version__)

data = [
  {
    "author": "Robert Greene",
    "book_available": 2,
    "book_name": "48 Laws of Power",
    "category": "Psychology",
    "created_at": "2023-11-11",
    "description": "The 48 Laws of Power,\u201d best-selling author Robert Greene argues that if you manage to seduce, charm, and deceive your opponents, you will attain the ultimate power.",
    "edition": "First",
    "id": 1234,
    "quantity": 2,
    "status": "AVAILABLE"
  },
  {
    "author": "Robert Greene",
    "book_available": 3,
    "book_name": "48 Laws of Power",
    "category": "Psychology",
    "created_at": "2023-11-11",
    "description": "The 48 Laws of Power,\u201d best-selling author Robert Greene argues that if you manage to seduce, charm, and deceive your opponents, you will attain the ultimate power.",
    "edition": "Second",
    "id": 1235,
    "quantity": 3,
    "status": "AVAILABLE"
  },
  {
    "author": "J. D. Salinger",
    "book_available": 0,
    "book_name": "The Catcher in the Rye",
    "category": "Novel",
    "created_at": "2023-11-11",
    "description": "The Catcher in the Rye, novel by J.D. Salinger published in 1951. The novel details two days in the life of 16-year-old Holden Caulfield after he has been expelled from prep school. Confused and disillusioned, Holden searches for truth and rails against the \u201cphoniness\u201d of the adult world.",
    "edition": "2001",
    "id": 1237,
    "quantity": 1,
    "status": "NOT AVAILABLE"
  },
  {
    "author": "F. Scott Fitzgerald.",
    "book_available": 4,
    "book_name": "The Great Gatsby",
    "category": "Novel",
    "created_at": "2023-11-11",
    "description": "The Great Gatsby, Third novel by American author F. Scott Fitzgerald, published in 1925. Set in Jazz Age New York, it tells the tragic story of Jay Gatsby, a self-made millionaire, and his pursuit of Daisy Buchanan, a wealthy young woman whom he loved in his youth.",
    "edition": "1925",
    "id": 1238,
    "quantity": 5,
    "status": "AVAILABLE"
  },
  {
    "author": "Jane Austen",
    "book_available": 2,
    "book_name": "Pride and Prejudice",
    "category": "Novel",
    "created_at": "2023-11-12",
    "description": "Pride and Prejudice follows the turbulent relationship between Elizabeth Bennet, the daughter of a country gentleman, and Fitzwilliam Darcy, a rich aristocratic landowner. They must overcome the titular sins of pride and prejudice in order to fall in love and marry.",
    "edition": "1995",
    "id": 1240,
    "quantity": 2,
    "status": "AVAILABLE"
  },
  {
    "author": "Author",
    "book_available": 2,
    "book_name": "New Book",
    "category": "Demo",
    "created_at": "2023-11-20",
    "description": "This is demo book",
    "edition": "2023",
    "id": 1242,
    "quantity": 2,
    "status": "AVAILABLE"
  },
  {
    "author": "Author",
    "book_available": 1,
    "book_name": "New Book",
    "category": "Demo",
    "created_at": "2023-11-20",
    "description": "",
    "edition": "2022",
    "id": 1243,
    "quantity": 1,
    "status": "AVAILABLE"
  },
  {
    "author": "Author",
    "book_available": 1,
    "book_name": "New Book",
    "category": "Demo",
    "created_at": "2023-11-20",
    "description": "",
    "edition": "2021",
    "id": 1244,
    "quantity": 1,
    "status": "AVAILABLE"
  }
]

df = pd.DataFrame(data)

print(df)

print(df[['book_name', 'created_at', 'description']])