# python
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/19/24 12:30
# @Author  : lzg
# @Site    : 
# @File    : databaseHandler.py
# @Software: PyCharm
import os
import sqlite3

# Define the database and table schema
DB_FILE = "scholar_data.db"
TABLE_NAME = "google_scholar_profiles"


# Function to ensure the SQLite database and table exist

def initialize_database(db_file=DB_FILE):
    """
    Ensure the SQLite database file exists and the required table is created.
    """
    print(f"Initializing database at {os.path.abspath(db_file)} with table {TABLE_NAME}.")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            googlescholar_id TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            href TEXT,
            full_name TEXT,
            position TEXT,
            affiliation TEXT,
            affiliation_link TEXT,
            homepage TEXT,
            keywords TEXT
        )
    """)
    conn.commit()
    conn.close()
    print(f"Database initialized at {db_file} with table {TABLE_NAME}.")

def insert_data(entry, db_file=DB_FILE):
    """
    Insert or update the given data into the SQLite database.

    Parameters:
    - entry: dict of dictionaries representing Google Scholar profiles.
    - db_file: Path to the SQLite database file.
    """

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    googlescholar_id = entry.get('googlescholar_id')
    name = entry.get('name')
    email = entry.get('email')
    href = entry.get('href')
    full_name = entry.get('profile_info', {}).get('full_name') or entry.get('full_name')
    position = entry.get('profile_info', {}).get('position') or entry.get('position')
    affiliation = entry.get('profile_info', {}).get('affiliation') or entry.get('affiliation')
    affiliation_link = entry.get('profile_info', {}).get('affiliation_link') or entry.get('affiliation_link')
    try:
        homepage = entry.get('profile_info', {}).get('homepage', {}).get('href') or entry.get('homepage', {}).get('href')
    except:
        homepage = ''
    keywords = ", ".join(
        keyword.lower().replace(" ", "_")
        for keyword in (
                entry.get('profile_info', {}).get('keywords', []) or entry.get('keywords', [])
        ))

    # Insert or replace into the table
    cursor.execute(f"""
        INSERT OR REPLACE INTO {TABLE_NAME} (
            googlescholar_id, name, email, href, full_name, position,
            affiliation, affiliation_link, homepage, keywords
        ) VALUES (?, ?, ?,?, ?, ?, ?, ?, ?, ?)
    """, (
        googlescholar_id, name,email, href, full_name, position,
        affiliation, affiliation_link, homepage, keywords
    ))

    conn.commit()
    conn.close()
    print(f"Data inserted/updated successfully in {TABLE_NAME}.")




def fetch_scholar_data(googlescholar_id, db_file=DB_FILE):
    """
    Fetch data from the database by googlescholar_id and restore it to the desired structure.

    Parameters:
    - googlescholar_id: The Google Scholar ID to search for.
    - db_file: Path to the SQLite database file.

    Returns:
    - A dictionary in the desired format. or return a default dictionary if no data is found which value is ''.
     return same as FullAuthorInfo structure
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Query the database
    cursor.execute(f"""
        SELECT googlescholar_id, name, href, full_name, position,
               affiliation, affiliation_link, homepage, keywords,email
        FROM {TABLE_NAME}
        WHERE googlescholar_id = ?
    """, (googlescholar_id,))
    row = cursor.fetchone()
    conn.close()

    # Default values if the query returns no result
    if not row:
        return {
            'googlescholar_id': '',
            'href': '',
            'email': '',
            'name': '',
            'full_name': '',
            'position': '',
            'affiliation': '',
            'affiliation_link': '',
            'homepage': {'href': '', 'text': 'N/A'},
            'keywords': []
        }

    # Rebuild the dictionary
    result = {
        'googlescholar_id': row[0] or '',
        'href': row[2] or '',
        'name': row[1] or '',
        'email': row[9] or '',
        'full_name': row[3] or '',
        'position': row[4] or '',
        'affiliation': row[5] or '',
        'affiliation_link': row[6] or '',
        'homepage': {'href': row[7] or '', 'text': 'N/A'},
        'keywords': [{'name': k.strip(), 'href': f'/citations?view_op=search_authors&hl=zh-CN&mauthors=label:{k.strip().replace(" ", "_")}'}
                     for k in (row[8] or '').split(',') if k.strip()]
    }
    return result


