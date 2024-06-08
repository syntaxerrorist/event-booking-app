#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item for QUT's teaching unit
#  IFB104, "Building IT Systems", Semester 1, 2022.  By submitting
#  this code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
student_number = 10893997 # put your student number here as an integer
student_name   = 'Alfonso Avenido' # put your name here as a character string
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  All files submitted will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Assignment Description-----------------------------------------#
#
#  Tickets, Please!
#
#  In this assignment you will combine your knowledge of HTMl/CSS
#  mark-up languages with your skills in Python scripting, pattern
#  matching, databases and Graphical User Interface design to produce
#  a robust, interactive application that allows its user to view
#  and save data from multiple online sources.
#
#  See the client's briefings accompanying this file for full
#  details.
#
#--------------------------------------------------------------------#



#-----Initialisation Steps-------------------------------------------#
#

# Import standard Python 3 modules needed to complete this assignment.
# You should not need to use any modules other than those provided
# in a standard Python 3 installation for your solution.
#
# In particular, you may NOT use any Python modules that need to be
# downloaded and installed separately, such as "Beautiful Soup" or
# "Pillow", because the markers will not have access to such modules
# and will not be able to run your code.  Only modules that are part
# of a standard Python 3 installation may be used.

# A function for exiting the program immediately (renamed
# because "exit" is already a standard Python function).
from cProfile import label
from sys import exit as abort
from unicodedata import name
from urllib.error import HTTPError, URLError

# A function for opening a web document given its URL.
# [You WILL need to use this function in your solution,
# either directly or via the "download" function below.]
from urllib.request import urlopen

# Some standard Tkinter functions.  [You WILL need to use
# SOME of these functions in your solution.]  You may also
# import other widgets from the "tkinter" module, provided they
# are standard ones and don't need to be downloaded and installed
# separately.  (NB: Although you can import individual widgets
# from the "tkinter.tkk" module, DON'T import ALL of them
# using a "*" wildcard because the "tkinter.tkk" module
# includes alternative versions of standard widgets
# like "Label" which leads to confusion.)
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

# Functions for finding occurrences of a pattern defined
# via a regular expression.  [You do not necessarily need to
# use these functions in your solution, because the problem
# can be solved with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.]
from re import *

# A function for displaying a web document in the host
# operating system's default web browser (renamed to
# distinguish it from the built-in "open" function for
# opening local files).  [You WILL need to use this function
# in your solution.]
from webbrowser import open as urldisplay

# All the standard SQLite functions.
from sqlite3 import *
import webbrowser

# Confirm that the student has declared their authorship.
# You must NOT change any of the code below.
if not isinstance(student_number, int):
    print('\nUnable to run: No student number supplied',
          '(must be an integer)\n')
    abort()
if not isinstance(student_name, str):
    print('\nUnable to run: No student name supplied',
          '(must be a character string)\n')
    abort()

#
#--------------------------------------------------------------------#



#-----Supplied Function----------------------------------------------#
#
# Below is a function you can use in your solution if you find it
# helpful.  (You are not required to use this function, but it may
# save you some effort.)
#

# A function to download and save a web document.  The function
# returns the downloaded document as a character string and
# optionally saves it as a local file.  If the attempted download
# fails, an error message is written to the shell window and the
# special value None is returned.
#
# Parameters:
# * url - The address of the web page you want to download.
# * target_filename - Name of the file to be saved (if any).
# * filename_extension - Extension for the target file, usually
#      "html" for an HTML document or "xhtml" for an XML
#      document.
# * save_file - A file is saved only if this is True. WARNING:
#      The function will silently overwrite the target file
#      if it already exists!
# * char_set - The character set used by the web page, which is
#      usually Unicode UTF-8, although some web pages use other
#      character sets.
# * incognito - If this parameter is True the Python program will
#      try to hide its identity from the web server. This can
#      sometimes be used to prevent the server from blocking access
#      to Python programs. However we discourage using this
#      option as it is both unreliable and unethical to
#      override the wishes of the web document provider!
#
def download(url = 'http://www.wikipedia.org/',
             target_filename = 'downloaded_document',
             filename_extension = 'html',
             save_file = True,
             char_set = 'UTF-8',
             incognito = False):

    # Import the function for opening online documents and
    # the class for creating requests
    from urllib.request import urlopen, Request

    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    # Import an exception raised when a web document cannot
    # be downloaded
    from urllib.error import URLError

    # Open the web document for reading
    try:
        if incognito:
            # Pretend to be a web browser instead of
            # a Python script (NOT RELIABLE OR RECOMMENDED!)
            request = Request(url)
            request.add_header('User-Agent',
                               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                               'AppleWebKit/537.36 (KHTML, like Gecko) ' +
                               'Chrome/42.0.2311.135 Safari/537.36 Edge/12.246')
            print("Warning - Request does not reveal client's true identity.")
            print("          This is both unreliable and unethical!")
            print("          Proceed at your own risk!\n")
        else:
            # Behave ethically
            request = url
        web_page = urlopen(request)
    except ValueError:
        print("Download error - Cannot find document at URL '" + url + "'\n")
        return None
    except HTTPError:
        print("Download error - Access denied to document at URL '" + url + "'\n")
        return None
    except URLError:
        print("Download error - Cannot access URL '" + url + "'\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to download " + \
              "the document at URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Read the contents as a character string
    try:
        web_page_contents = web_page.read().decode(char_set)
    except UnicodeDecodeError:
        print("Download error - Unable to decode document from URL '" + \
              url + "' as '" + char_set + "' characters\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to decode " + \
              "the document from URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Optionally write the contents to a local text file
    # (overwriting the file if it already exists!)
    if save_file:
        try:
            text_file = open(target_filename + '.' + filename_extension,
                             'w', encoding = char_set)
            text_file.write(web_page_contents)
            text_file.close()
        except Exception as message:
            print("Download error - Unable to write to file '" + \
                  target_filename + "'")
            print("Error message was:", message, "\n")

    # Return the downloaded document to the caller
    return web_page_contents

#
#--------------------------------------------------------------------#



#-----Student's Solution---------------------------------------------#
#
# Put your solution at the end of this file.
#

# To make it easy for the marker to find, use this filename
# for your ticket in Task 2B
ticket_file = 'your_ticket.html'

# Your code goes here

#HTML - This template is used to generate event tickets
html_template = """<!DOCTYPE HTML>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Event Ticket</title>
        <style>
            table {width: 450px; margin-left: auto; margin-right: auto}
            ul {width: 450px; margin-left: auto; margin-right: auto}
            td {padding: 15px}
            img {border: 2px; width: 60%; height: 5}
        </style>
   
    </head>
   
    <body>
        <table border="2">
            <tr>
                <td align="center">
                    <strong style="font-size: 35px;">Admit One</strong>
                    <br> This is your ticket courtesy of
                    <br><em>Ticker Master</em>
                </td>
            </tr>
            <tr height=450px>
                <td align="center">
                    <strong style="font-size: 25px;">***Event Name***</strong>
                    <br>
                    <br>
                    <br><img src=***photo_source*** alt="No Image Found">
                    <br>
                    <br><strong style="font-size: 25px;">***Venue***</strong>
                    <br>
                    <br>***Date***
                    <br><a href="insert_website_here"><em>***URL***</em></a>
                </td>
            </tr>
        </table>
    <script>
   
    </script>
    </body>
</html>
"""
# Set variable name for master window
app = Tk()

# Configuring title and window size
app.title('Ticker Master')
app.geometry('930x325')
app['bg'] = 'cadetblue1'

# Import image to place inside frame
logo = PhotoImage(file = 'tickermaster.png')
Label(app, image = logo).grid(row = 0, column = 0, padx = 5, pady=5)

# Assigning frame text and frame content font style and size
frame_text_font = ('Arial', 16)
text_font = ('Arial', 14)

# Setting IntVar so not all radiobuttons are selected at once
label_venue = IntVar()

# Setting venue frame and placing with grid geometry method
venue_frame = LabelFrame(app, text = 'Choose Venue',
                         font = frame_text_font,
                         bg = app['bg'],
                         fg=['grey'],
                         padx = 25)
venue_frame.grid(row=0, column=1, sticky=N, padx=15)

# Updates the default text inside the Text frame after scanning the regex
def update_text(name, date):
    info.configure(state='normal') # Changes the state to 'normal' so editing is enabled
    info.delete('1.0', END) # Deletes default message
    info.insert(END, 'Event: ' + name + '\n' + 'Date: ' + date + line_breaks) # Replaces empty Text frame with event information
    info.configure(state='disabled') # Changes the state back to 'disabled' so that frame prevents user input/ editing

# Updates the default text inside the Text frame to a specific error message if the application
# cannot retrieve the required content from the web documents
def error_text(message):
    info.configure(state='normal')
    info.delete('1.0', END)
    info.insert(END, message + line_breaks)
    info.configure(state='disabled')
 
# Creating a dictionary with keys containing their regular experessions to search for each variable
config = {
    "suncorp": {
        "url": "https://suncorpstadium.com.au/what-s-on.aspx",
        "event_name_regex": '<h6 class=\"event-title\">(.*)<\/h6>',
        "event_date_regex": '<h7 class=\"event-date\ text-uppercase\">(.*)<\/h7>',
        "event_photo_regex": '\<img src=\"(.*)" class=\"cover\-img\-top position\-absolute\">',
    },
    "accorstadium": {
        "url": "https://accorstadium.com.au/whats-on/",
        "event_name_regex": "<h4 class\=\"split\">(.*)",
        "event_date_regex": '<span class\=\"sub-title date\">\n(.*)\n',
        "event_photo_regex": "src\=\"(.*)\" alt\=",
    },
    "commbankstadium": {
        "url": "https://commbankstadium.com.au/whats-on/",
        "event_name_regex": "<span class\=\"eventname\"\>(.*)\<\/span>",
        "event_date_regex": "<span class\=\"eventdate\"\>(.*)\<\/span>",
        "event_photo_regex": "<img width\=\"460\" height\=\"480\" src\=\"(.*)\" class\=",
    }
}

# Passes the keys as arguments from the config dictionaries to scan the latest event information
# ** This is used by the show_event() function **
# This function only looks for the latest EVENT TITLE and its DATE
# The **kwargs parameter allows the dictionary being passed to contain as many keys
# even if the function doesn't require it to be passed
def get_event_data(url, event_name_regex, event_date_regex, **kwargs):
   
    # Try to open URL, read and decode using unicode then continue to execute the code
    # unless there are errors, then it is handled by the except statement
    try:
        web_page = urlopen(url)
        web_page_bytes = web_page.read().decode('UTF-8')
        web_page.close()

        # Search for name of the event
        event_name = findall(event_name_regex, web_page_bytes)
        for name in event_name[0:1]: # Only extracting the string inside the HTML tag containing the latest event name
            event_title = name
            
        # Search for date of the event
        event_date = findall(event_date_regex, web_page_bytes)
        for date in event_date[0:1]: # Only extracting the string inside the HTML tag containing the latest event date
            date = date.strip() # Strips any whitespaces

        # Updates default text with a new string containing the retrieved data
        update_text(name, date)

    # Except statements to catch different types of errors
    # and outputs a message to the text box accordingly by using the error_text function
    except ValueError:
        err_msg = "Download Error - Cannot find document at URL {} \n".format(url)
        error_text(err_msg)

    except HTTPError:
        err_msg = "Download Error - Access denied to document at URL " + url + "\n"
        error_text(err_msg)

    except URLError:
        err_msg = "Download Error - Cannot access URL " + url + "\n"
        error_text(err_msg)

    except Exception as message:
        err_msg = "Download error - Something went wrong when trying to download the document at URL {}".format(url)
        error_text(err_msg)      

# Website URLs
accor_website = 'https://accorstadium.com.au'
suncorp_website = 'https://suncorpstadium.com.au'
commbank_website = 'https://commbankstadium.com.au/whats-on/'

# Passes the keys as arguments from the config dictionaries to scan the latest event information
# ** This is used by the print_ticket() function **
# This function only looks for the latest EVENT TITLE, DATE and EVENT IMAGE SOURCE
def get_ticket_data(url, event_name_regex, event_date_regex, event_photo_regex, **kwargs):

    # Tries to execute this block of code except when errors appear

    # Opens a webpage, reads and decodes it using Unicode and then closes it
    try:
        web_page = urlopen(url)
        web_page_bytes = web_page.read().decode('UTF-8')
        web_page.close()

        # Search for the event name
        event_name = findall(event_name_regex, web_page_bytes)
        for name in event_name[0:1]:
            event_title = name

        # Search for the event date
        event_date = findall(event_date_regex, web_page_bytes)
        for date in event_date[0:1]:
            date = date.strip()

        # SUNCORP - Image source
        suncorp_image_source = findall(event_photo_regex, web_page_bytes)
        for image in suncorp_image_source:
            image = suncorp_image_source[0]
            suncorp_image = '"' + suncorp_website + image + '"'
   
        # ACCOR - Image Source
        accor_image_source = findall(event_photo_regex, web_page_bytes)
        for image in accor_image_source:
            image = accor_image_source[1]
            accor_image = '"' + accor_website + image + '"'

        # COMMBANK - Image Source
        commbank_image_source = findall(event_photo_regex, web_page_bytes)
        for image in commbank_image_source:
            image = commbank_image_source[0]
            commbank_image = '"' + image + '"' #  CommBank source image already includes its domain name

    # Except statement
    except:
        err_msg = 'Ticket Data Not Found'
        event_title = 'No Data Found'
        date = 'No Data Found'
        suncorp_image = 'None'
        accor_image = 'None'
        commbank_image = 'None'

        # Used for debugging purposes
        #print('Ticket data search attempted: ' + err_msg)
   
    # Passes the Suncorp key if label.venue = 1
    if label_venue.get() == 1:
        html_code = html_template.replace('***Event Name***', event_title)
        html_code = html_code.replace('***Date***', date)
        html_code = html_code.replace('***URL***', url)
        html_code = html_code.replace('***Venue***', venue_one['text'])
        html_code = html_code.replace('***photo_source***', suncorp_image)

    # Passes the Accor key if label.venue = 2
    if label_venue.get() == 2:
        html_code = html_template.replace('***Event Name***', event_title)
        html_code = html_code.replace('***Date***', date)
        html_code = html_code.replace('***URL***', url)
        html_code = html_code.replace('***Venue***', venue_two['text'])
        html_code = html_code.replace('***photo_source***', accor_image)

    # Passes the CommBank key if label.venue = 3
    if label_venue.get() == 3:
        html_code = html_template.replace('***Event Name***', event_title)
        html_code = html_code.replace('***Date***', date)
        html_code = html_code.replace('***URL***', url)
        html_code = html_code.replace('***Venue***', venue_three['text'])
        html_code = html_code.replace('***photo_source***', commbank_image)
   
   # Opens an HTML file and replaces the existing strings
    html_file = open(ticket_file, 'w', encoding='UTF-8')
    html_file.write(html_code)
    html_file.close()


# Prints a ticket to an HTML document after pressing the 'Print Ticket' button
# Certain tickets will be printed depending on which Radiobutton is selected
# This unlocks the 'Save Booking' button
def print_ticket():

    # Unlocks the 'Save Booking' option
    save_booking_option['state']='normal'
   
    if label_venue.get() == 1:
        suncorp_data = config["suncorp"]
        get_ticket_data(**suncorp_data)

    if label_venue.get() == 2:
        accorstadium_data = config['accorstadium']
        get_ticket_data(**accorstadium_data)

    if label_venue.get() == 3:
        commbankstadium_data = config['commbankstadium']
        get_ticket_data(**commbankstadium_data)

# Prints out the event name and date details onto the GUI Textbox when 'Show Event' option is selected
# Output will depend upon which Radiobutton is selected
def show_event():

    if label_venue.get() == 1:
        suncorp_data = config["suncorp"]
        get_event_data(**suncorp_data)

    if label_venue.get() == 2:
        accorstadium_data = config["accorstadium"]
        get_event_data(**accorstadium_data)

    if label_venue.get() == 3:
        commbankstadium_data = config["commbankstadium"]
        get_event_data(**commbankstadium_data)

# Opens up the default web browser and loads up the the website when 'Display Details' is pressed
# Browser will load up the website of the selected venue
def display_details():
    if label_venue.get() == 1:
        webbrowser.open(config["suncorp"]["url"])
   
    if label_venue.get() == 2:
        webbrowser.open(config["accorstadium"]["url"])

    if label_venue.get() == 3:
        webbrowser.open(config["commbankstadium"]["url"])

# Passes the keys as arguments from the config dictionary to scan the latest event information
# ** This is used by the save_booking() function **
# This function looks for the EVENT TITLE, DATE nd URL of the latest event
# and replaces inserts the values as a row into the bookings.db database
def get_booking_data(url, event_name_regex, event_date_regex, **kwargs):

    try:

        web_page = urlopen(url)
        web_page_bytes = web_page.read().decode('UTF-8')
        web_page.close()

        event_name = findall(event_name_regex, web_page_bytes)
        for name in event_name[0:1]:
            event_title = name
            event_title = event_title

        event_date = findall(event_date_regex, web_page_bytes)
        for date in event_date[0:1]:
            date = date.strip()
            date = date

    # Only event title and date will output an error message if data cannot be successfully retrieved
    except Exception as err_msg:
        err_msg = 'No Data Found'
        event_title = err_msg
        date = err_msg

    # Initiate connection to the database
    connection = connect(database = 'bookings.db')
    bookings_db = connection.cursor()
   
    # Using the sqllite3 module to insert the values as a new row inside the database
    template = "INSERT INTO tickets_bought VALUES ('EVENT', 'DATE', 'VENUE', 'URL')"
    sql_statement = template.replace('EVENT', event_title).replace('DATE', date).replace('URL', url) # Venue
    bookings_db.execute(sql_statement)
    # Used for debugging purposes
    #print('Number of rows affected', bookings_db.rowcount)

    # Commit the changes and terminates the connection to the database
    connection.commit()
    bookings_db.close()
    connection.close()

# Saves the booking into the 'bookings.db' database when the 'Save Booking' option is selected
# Passes the keys as arguments from the config dictionary to retrieve the latest event title and date
# Venue and URL will depend on what the user has selected on the GUI
def save_booking():

    # Suncorp Stadium
    if label_venue.get() == 1:
        event_venue = 'Suncorp Stadium'
        suncorp_data = config["suncorp"]
        get_booking_data(**suncorp_data)

    # Accor Stadium
    if label_venue.get() == 2:
        event_venue = 'Accor Stadium'
        accorstadium_data = config['accorstadium']
        get_booking_data(**accorstadium_data)
   
    # CommBank Stadium
    if label_venue.get() == 3:
        event_venue = 'CommBank Stadium'
        commbankstadium_data = config['commbankstadium']
        get_booking_data(**commbankstadium_data)
   
    # Initiate connection to the database
    connection = connect(database = 'bookings.db')
    bookings_db = connection.cursor()
   
    # Updates the existing row inside the database by changing the default venue name to the
    # name of the selected venue
    template = "UPDATE tickets_bought SET venue = 'NEWNAME' WHERE venue = 'VENUE'"
    sql_statement = template.replace('NEWNAME', event_venue)
    bookings_db.execute(sql_statement)

    # Used for debugging purposes
    #print('Number of rows affected', bookings_db.rowcount)

    # Commit changes to the database and terminates the connection
    connection.commit()
    bookings_db.close()
    connection.close()
   
    # Disables the 'Save Booking' button after it is pressed since it requires the user to
    # print another ticket before any booking is allowed to be saved
    save_booking_option['state'] = 'disabled'

# When the program is initialized, all the Options are disabled until a venue is selected
# This is to implement a simple user-friendly feature to ensure that using the product is
# intuitive and straightforward
def venue_select(label_venue):

    if label_venue == 1:
        show_event_option['state']='normal'
        display_details_option['state']='normal'
        print_ticket_option['state']='normal'
        save_booking_option['state']='disabled' # The 'Save Booking' option is only enabled when a user prints a ticket
       
    elif label_venue == 2:
        show_event_option['state']='normal'
        display_details_option['state']='normal'
        print_ticket_option['state']='normal'
        save_booking_option['state']='disabled'
       
    elif label_venue == 3:
        show_event_option['state']='normal'
        display_details_option['state']='normal'
        print_ticket_option['state']='normal'
        save_booking_option['state']='disabled'     

# Creating Radiobuttons and placing with grid geometry

# Suncorp Stadium
venue_one = Radiobutton(venue_frame, text='Suncorp Stadium',
                        font=text_font,
                        variable = label_venue,
                        value=1,
                        bg=app['bg'],
                        activebackground = app['bg'],
                        activeforeground = 'red',
                        command=lambda:venue_select(label_venue.get()))

# Accor Stadium
venue_two = Radiobutton(venue_frame, text='Accor Stadium',
                        font=text_font,
                        variable=label_venue,
                        value=2,
                        bg=app['bg'],
                        activebackground = app['bg'],
                        activeforeground = 'red',
                        command=lambda:venue_select(label_venue.get()))

# CommBank Stadium
venue_three = Radiobutton(venue_frame, text='CommBank Stadium',
                        font=text_font,
                        variable=label_venue,
                        value=3,
                        bg=app['bg'],
                        activebackground = app['bg'],
                        activeforeground = 'red',
                        command=lambda:venue_select(label_venue.get()))  

# Placing each radiobuttons with grid geometry and sticking them to the west end of their relevant border                                              
venue_one.grid(sticky=W)
venue_two.grid(sticky=W)
venue_three.grid(sticky=W)


# Options Selection

# Setting frame for Options selection
option_frame = LabelFrame(app, font=frame_text_font,
                         text='Options',
                         bg = app['bg'],
                         fg=['grey'],
                         padx = 10,
                         pady = 5)
option_frame.grid(row=0, column = 2, sticky = NE)

# Creating push buttons for various options

# Show Event
show_event_option = Button(option_frame, font=text_font,
                        text='Show event',
                        activeforeground=['red'], state='disabled',
                        command=show_event)
# Display Details
display_details_option = Button(option_frame, font=text_font,
                        text='Display details',
                        activeforeground=['red'],
                        state='disabled',
                        command=display_details)
# Print Ticket
print_ticket_option = Button(option_frame, font=text_font,
                        text='Print ticket',
                        activeforeground=['red'],
                        state='disabled',
                        command=print_ticket)
# Save Booking
save_booking_option = Button(option_frame, font=text_font,
                        text='Save booking',
                        activeforeground=['red'],
                        state='disabled',
                        command=save_booking)                                                                        

# Placing with grid geometry
show_event_option.grid(sticky=W, pady=3)
display_details_option.grid(sticky=W, pady=3)
print_ticket_option.grid(sticky=W, pady=3)
save_booking_option.grid(sticky=W, pady=3)

# Using text box and adding multiple lines to make it scrollable
# This part will produce outputs in Task 2B
box_frame = LabelFrame(app, text='Chosen Event',
                       font=frame_text_font,
                       bg=app['bg'],
                       fg=['grey'])
box_frame.grid(row=0, column =1, sticky=SW, padx=15, pady=15)

event_name = 'Event name will appear here'
event_date = 'Event date(s) will appear here'
line_breaks = '\n' + '\n' + '\n' + '\n' + '\n'

info = Text(box_frame, wrap=WORD, width=35, height=4, font=text_font, bg=app['bg'])
info.grid(row=0, column=0, rowspan=2, pady=5, padx=5)
info.insert(END,
            event_name + '\n' +
            event_date +
            line_breaks)
info.configure(state='disabled') # Update state so that Textbox cannot be altered


app.mainloop()