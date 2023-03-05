import os
import sqlite3

# Define the function to parse filenames from files
def parse_filenames_from_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
        lines = content.splitlines()
        return [(os.path.splitext(line)[0], os.path.splitext(line)[1]) for line in lines]

# Define the function to parse PDF filenames from nested files
def parse_pdf_filenames(directory_path):
    pdf_files = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    return pdf_files

# Open a connection to the database
conn = sqlite3.connect('database_name.db')
c = conn.cursor()

# Create a table to store the PDF files
c.execute('''CREATE TABLE pdfs
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              filename TEXT,
              data BLOB)''')

# Parse filenames from files and insert into the database
file_path = '/path/to/filename_file.txt'
filenames = parse_filenames_from_file(file_path)
for filename in filenames:
    c.execute("INSERT INTO filenames (filename, extension) VALUES (?, ?)", filename)
    conn.commit()

# Parse PDF filenames from nested files and store in the database
directory_path = '/path/to/pdf_files_directory'
pdf_filenames = parse_pdf_filenames(directory_path)
for pdf_filename in pdf_filenames:
    with open(pdf_filename, 'rb') as f:
        pdf_data = f.read()
        c.execute("INSERT INTO pdfs (filename, data) VALUES (?, ?)", (os.path.basename(pdf_filename), pdf_data))
        conn.commit()

# Close the connection to the database
conn.close()
