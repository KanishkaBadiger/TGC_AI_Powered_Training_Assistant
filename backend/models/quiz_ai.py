import os
import json
import time
import re
import random
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# --- 🛡️ FAIL-SAFE BACKUP DATA (50 QUESTIONS EACH) ---
# If the API fails, these questions will be served instantly.
BACKUP_DB = {
    "Aptitude Round": [
        {"question": "A train running at the speed of 60 km/hr crosses a pole in 9 seconds. What is the length of the train?", "options": ["120 metres", "180 metres", "324 metres", "150 metres"], "correct_option": "150 metres", "explanation": "Speed = 60*(5/18) m/sec = 50/3 m/sec. Length = Speed x Time = (50/3) x 9 = 150 metres."},
        {"question": "Find the missing number in the series: 2, 6, 12, 20, 30, 42, ?", "options": ["56", "54", "50", "62"], "correct_option": "56", "explanation": "The pattern is +4, +6, +8, +10, +12. So next is 42 + 14 = 56."},
        {"question": "Which word does NOT belong with the others?", "options": ["Index", "Glossary", "Chapter", "Book"], "correct_option": "Book", "explanation": "Index, Glossary, and Chapter are parts of a book. Book is the whole."},
        {"question": "A is B's sister. C is B's mother. D is C's father. E is D's mother. Then, how is A related to D?", "options": ["Granddaughter", "Daughter", "Grandmother", "Aunt"], "correct_option": "Granddaughter", "explanation": "A is the daughter of C, and C is the daughter of D. So A is D's granddaughter."},
        {"question": "In a certain code language, COMPUTER is written as RFUVQNPC. How will MEDICINE be written?", "options": ["EOJDJEFM", "EOJDEJFM", "MFEJDJOE", "MFEDJJOE"], "correct_option": "EOJDJEFM", "explanation": "The letters are written in reverse order and then moved +1 or -1 steps alternately."},
        {"question": "If A can do a piece of work in 10 days and B in 15 days, how long will they take together?", "options": ["5 days", "6 days", "8 days", "9 days"], "correct_option": "6 days", "explanation": "1/10 + 1/15 = 5/30 = 1/6. So, 6 days."},
        {"question": "What is the probability of getting a sum of 9 from two throws of a dice?", "options": ["1/6", "1/8", "1/9", "1/12"], "correct_option": "1/9", "explanation": "Combinations: (3,6), (4,5), (5,4), (6,3) = 4 outcomes. Total = 36. 4/36 = 1/9."},
        {"question": "A father is 3 times as old as his son. After 15 years, he will be twice as old. What is the son's current age?", "options": ["10", "15", "20", "25"], "correct_option": "15", "explanation": "Let son=x, father=3x. 3x+15 = 2(x+15) -> 3x+15=2x+30 -> x=15."},
        {"question": "Look at this series: 7, 10, 8, 11, 9, 12, ... What number should come next?", "options": ["7", "10", "12", "13"], "correct_option": "10", "explanation": "Alternating series: 7->8->9->10 and 10->11->12."},
        {"question": "Which number replaces the question mark? 4, 16, 36, 64, ?", "options": ["100", "81", "121", "144"], "correct_option": "100", "explanation": "Squares of even numbers: 2^2, 4^2, 6^2, 8^2, so 10^2 = 100."},
        {"question": "A vendor bought toffees at 6 for a rupee. How many for a rupee must he sell to gain 20%?", "options": ["3", "4", "5", "6"], "correct_option": "5", "explanation": "CP of 6 = 1 Re. SP of 6 = 1.2 Rs. For 1 Re, he sells 6/1.2 = 5."},
        {"question": "Introducing a man, a woman said, 'He is the only son of the mother of my mother.' How is the woman related to the man?", "options": ["Mother", "Sister", "Niece", "Aunt"], "correct_option": "Niece", "explanation": "Mother of my mother = Grandmother. Only son of Grandmother = Maternal Uncle. Woman is Niece."},
        {"question": "Average of 5 numbers is 20. If each number is multiplied by 2, what is the new average?", "options": ["20", "30", "40", "10"], "correct_option": "40", "explanation": "If every observation is multiplied by X, the average is also multiplied by X."},
        {"question": "The ratio of boys and girls in a class is 3:2. If there are 20 girls, how many boys are there?", "options": ["20", "30", "40", "50"], "correct_option": "30", "explanation": "2 parts = 20, so 1 part = 10. Boys = 3 parts = 30."},
        {"question": "If SOUTH-EAST becomes NORTH, NORTH-EAST becomes WEST, what will WEST become?", "options": ["SOUTH-EAST", "SOUTH-WEST", "NORTH-EAST", "NORTH-WEST"], "correct_option": "SOUTH-EAST", "explanation": "Every direction is rotated 135 degrees clockwise."},
        {"question": "Find the odd one out: 3, 5, 7, 12, 13, 17, 19", "options": ["12", "13", "17", "3"], "correct_option": "12", "explanation": "All others are prime numbers."},
        {"question": "A clock shows 3:30. What is the angle between the hands?", "options": ["75 degrees", "90 degrees", "105 degrees", "60 degrees"], "correct_option": "75 degrees", "explanation": "Angle = |30*H - 5.5*M| = |30*3 - 5.5*30| = |90 - 165| = 75."},
        {"question": "Pipe A fills a tank in 4 hours, Pipe B in 6 hours. If opened together, how long to fill?", "options": ["2.4 hrs", "5 hrs", "10 hrs", "2 hrs"], "correct_option": "2.4 hrs", "explanation": "1/4 + 1/6 = 5/12. Time = 12/5 = 2.4 hours."},
        {"question": "What comes next: 1, 1, 2, 3, 5, 8, 13, ?", "options": ["21", "20", "18", "15"], "correct_option": "21", "explanation": "Fibonacci sequence: 8 + 13 = 21."},
        {"question": "A sum of money doubles itself in 10 years at simple interest. What is the rate of interest?", "options": ["10%", "5%", "20%", "15%"], "correct_option": "10%", "explanation": "SI = P. Rate = (100 * SI) / (P * T) = (100 * P) / (P * 10) = 10%."},
        {"question": "In a race of 1000m, A beats B by 100m. In a race of 400m, B beats C by 40m. How much does A beat C by in 500m?", "options": ["95m", "50m", "45m", "60m"], "correct_option": "95m", "explanation": "Ratio based calculation. A:B = 10:9, B:C = 10:9. A:C = 100:81."},
        {"question": "Choose the word synonymous to 'ABANDON'.", "options": ["Try", "Join", "Keep", "Forsake"], "correct_option": "Forsake", "explanation": "Abandon means to leave or give up completely."},
        {"question": "Choose the word opposite to 'OPTIMISTIC'.", "options": ["Pessimistic", "Hopeful", "Confident", "Idealistic"], "correct_option": "Pessimistic", "explanation": "Optimistic looks at the bright side; Pessimistic looks at the dark side."},
        {"question": "Rearrange letters 'R A E H T' to form a meaningful word.", "options": ["HEART", "EARTH", "HATER", "Both A & B"], "correct_option": "Both A & B", "explanation": "HEART and EARTH are both valid English words."},
        {"question": "A man walks 5km South, turns left walks 3km, turns left walks 5km. How far is he from start?", "options": ["3 km", "5 km", "0 km", "13 km"], "correct_option": "3 km", "explanation": "He forms a rectangle. He is 3km East of the starting point."},
        {"question": "If 50% of a number is added to 50, the result is the number itself. The number is?", "options": ["50", "100", "150", "200"], "correct_option": "100", "explanation": "0.5x + 50 = x -> 0.5x = 50 -> x = 100."},
        {"question": "Pointing to a photograph, a man said, 'I have no brother or sister but that man's father is my father's son.' Whose photo is it?", "options": ["His son", "His father", "Himself", "His nephew"], "correct_option": "His son", "explanation": "My father's son (since no siblings) = Me. 'That man's father is Me'. So it is his son."},
        {"question": "The day before yesterday was Saturday. What day will it be the day after tomorrow?", "options": ["Tuesday", "Wednesday", "Thursday", "Friday"], "correct_option": "Wednesday", "explanation": "Today is Monday. Day after tomorrow is Wednesday."},
        {"question": "What is 20% of 30% of 500?", "options": ["30", "50", "20", "15"], "correct_option": "30", "explanation": "20/100 * 30/100 * 500 = 0.2 * 150 = 30."},
        {"question": "Find the next term: A, C, F, J, O, ?", "options": ["U", "T", "S", "V"], "correct_option": "U", "explanation": "Skip 1, 2, 3, 4 letters. Next skip 5. O -> PQRST -> U."},
        {"question": "A boat goes 10 km upstream and 20 km downstream in 5 hours. Speed of stream?", "options": ["Cannot determine", "2 kmph", "3 kmph", "4 kmph"], "correct_option": "Cannot determine", "explanation": "Need more data to find exact speed of stream vs boat."},
        {"question": "Cost price of 20 articles is equal to Selling price of X articles. If profit is 25%, find X.", "options": ["15", "16", "18", "25"], "correct_option": "16", "explanation": "Profit % = (Difference/SP)*100. 25 = ((20-X)/X)*100 -> X=16."},
        {"question": "Which is the largest fraction?", "options": ["3/4", "5/6", "7/8", "2/3"], "correct_option": "7/8", "explanation": "3/4=0.75, 5/6=0.83, 7/8=0.875, 2/3=0.66."},
        {"question": "HCF of 24, 36, 60 is:", "options": ["12", "6", "24", "18"], "correct_option": "12", "explanation": "12 divides all three numbers perfectly."},
        {"question": "Sum of first 10 natural numbers?", "options": ["55", "50", "45", "60"], "correct_option": "55", "explanation": "n(n+1)/2 = 10*11/2 = 55."},
        {"question": "If 1st Jan 2004 is Thursday, what is 1st Jan 2005?", "options": ["Friday", "Saturday", "Sunday", "Monday"], "correct_option": "Saturday", "explanation": "2004 is a leap year. So +2 odd days. Thursday + 2 = Saturday."},
        {"question": "A student multiplied a number by 3/5 instead of 5/3. % Error?", "options": ["44%", "34%", "64%", "54%"], "correct_option": "64%", "explanation": "Let number = 15. Correct=25, Wrong=9. Error=16. (16/25)*100 = 64%."},
        {"question": "Seats in a cinema are increased by 25%. Price increased by 10%. % Increase in revenue?", "options": ["35%", "37.5%", "40%", "45%"], "correct_option": "37.5%", "explanation": "1.25 * 1.10 = 1.375 -> 37.5% increase."},
        {"question": "A coin is tossed 3 times. Probability of getting at least one head?", "options": ["7/8", "1/8", "1/2", "3/8"], "correct_option": "7/8", "explanation": "Total outcomes=8. Only TTT has no head. So 1 - 1/8 = 7/8."},
        {"question": "Speed of a boat in still water is 15 kmph. Current is 3 kmph. Time for 12 km downstream?", "options": ["30 min", "40 min", "45 min", "20 min"], "correct_option": "40 min", "explanation": "Speed Downstream = 15+3=18. Time = 12/18 hr = 2/3 hr = 40 min."},
        {"question": "How many seconds are there in x weeks x days x hours x minutes x seconds?", "options": ["Too difficult", "Use formula", "Varies", "Depends on x"], "correct_option": "Use formula", "explanation": "It requires converting each unit to seconds and summing up."},
        {"question": "Two numbers are in ratio 3:5. If 9 is subtracted from each, ratio is 12:23. The numbers are?", "options": ["33, 55", "30, 50", "36, 60", "39, 65"], "correct_option": "33, 55", "explanation": "(3x-9)/(5x-9) = 12/23. Solving gives x=11. Numbers 33, 55."},
        {"question": "A clock strikes once at 1, twice at 2, and so on. How many times in 24 hours?", "options": ["78", "156", "144", "136"], "correct_option": "156", "explanation": "Sum of 1 to 12 = 78. In 24 hours, 78 * 2 = 156."},
        {"question": "If 'PARK' is coded as '5394', 'SHIRT' is '17698' and 'PANDIT' is '532068', how is 'NISHAR' written?", "options": ["261739", "261738", "201739", "201738"], "correct_option": "261739", "explanation": "Direct letter to number mapping from given words."},
        {"question": "Length of a rectangle is increased by 20% and breadth decreased by 20%. Area change?", "options": ["0%", "4% decrease", "4% increase", "1% decrease"], "correct_option": "4% decrease", "explanation": "x + y + xy/100 -> 20 - 20 - 400/100 = -4%."},
        {"question": "A man buys a cycle for 1400 and sells it at loss of 15%. SP?", "options": ["1190", "1160", "1200", "1000"], "correct_option": "1190", "explanation": "1400 * 0.85 = 1190."},
        {"question": "Find the next number: 8, 24, 12, 36, 18, 54, ?", "options": ["27", "72", "68", "24"], "correct_option": "27", "explanation": "*3, /2, *3, /2 pattern. 54 / 2 = 27."},
        {"question": "If 60% of A = 3/4 of B, then A:B is?", "options": ["9:20", "20:9", "4:5", "5:4"], "correct_option": "5:4", "explanation": "3/5 A = 3/4 B -> A/B = 5/4."},
        {"question": "Odd one out: Curd, Butter, Oil, Cheese", "options": ["Curd", "Butter", "Oil", "Cheese"], "correct_option": "Oil", "explanation": "Others are milk products."},
        {"question": "In how many ways can letters of 'LEADER' be arranged?", "options": ["720", "360", "144", "72"], "correct_option": "360", "explanation": "6 letters, 2 E's. 6! / 2! = 720 / 2 = 360."}
    ],
    "Technical Round": [
        {"question": "What is the time complexity of binary search?", "options": ["O(n)", "O(log n)", "O(n^2)", "O(1)"], "correct_option": "O(log n)", "explanation": "Binary search divides the search interval in half repeatedly."},
        {"question": "Which of the following is NOT a characteristic of Object-Oriented Programming?", "options": ["Encapsulation", "Polymorphism", "Compilation", "Inheritance"], "correct_option": "Compilation", "explanation": "Compilation is a process of converting code, not an OOP concept."},
        {"question": "In Python, which keyword is used to start a function?", "options": ["function", "def", "fun", "define"], "correct_option": "def", "explanation": "The 'def' keyword is standard syntax for defining functions in Python."},
        {"question": "Which data structure is best for LIFO (Last In First Out) operations?", "options": ["Queue", "Stack", "Array", "Linked List"], "correct_option": "Stack", "explanation": "A Stack strictly follows the LIFO principle."},
        {"question": "What is the primary key in a SQL table?", "options": ["A unique identifier for each record", "The first column", "Any numeric column", "A foreign key"], "correct_option": "A unique identifier for each record", "explanation": "Primary keys must be unique and cannot be NULL."},
        {"question": "Which symbol is used for single-line comments in Python?", "options": ["//", "/*", "#", "--"], "correct_option": "#", "explanation": "Python uses # for comments."},
        {"question": "What does HTML stand for?", "options": ["Hyper Text Markup Language", "High Tech Modern Language", "Hyperlink Text Mode Language", "Home Tool Markup Language"], "correct_option": "Hyper Text Markup Language", "explanation": "Standard markup language for creating web pages."},
        {"question": "Which sorting algorithm has the best average case time complexity?", "options": ["Bubble Sort", "Insertion Sort", "Merge Sort", "Selection Sort"], "correct_option": "Merge Sort", "explanation": "Merge Sort is O(n log n), others listed are O(n^2) on average."},
        {"question": "In Java, 'static' variables belong to:", "options": ["The Class", "The Object", "The Method", "The Package"], "correct_option": "The Class", "explanation": "Static members are shared across all instances of a class."},
        {"question": "Which SQL command is used to remove a table completely?", "options": ["DELETE", "REMOVE", "DROP", "TRUNCATE"], "correct_option": "DROP", "explanation": "DROP TABLE deletes the table structure and data."},
        {"question": "What is the output of 2**3 in Python?", "options": ["6", "5", "8", "9"], "correct_option": "8", "explanation": "** is the exponentiation operator (2 to the power of 3)."},
        {"question": "Which data structure uses FIFO (First In First Out)?", "options": ["Stack", "Queue", "Tree", "Graph"], "correct_option": "Queue", "explanation": "Queue is FIFO (like a line of people)."},
        {"question": "In C++, what is a pointer?", "options": ["A variable that stores an address", "A keyword", "A data type", "A class"], "correct_option": "A variable that stores an address", "explanation": "Pointers hold the memory address of another variable."},
        {"question": "Which HTTP method is used to UPDATE a resource?", "options": ["GET", "POST", "PUT", "DELETE"], "correct_option": "PUT", "explanation": "PUT (or PATCH) is used for updates."},
        {"question": "What is a 'Tuple' in Python?", "options": ["Mutable list", "Immutable list", "Dictionary", "Set"], "correct_option": "Immutable list", "explanation": "Tuples cannot be changed after creation."},
        {"question": "Which concept allows a class to derive properties from another class?", "options": ["Polymorphism", "Inheritance", "Encapsulation", "Abstraction"], "correct_option": "Inheritance", "explanation": "Inheritance allows child classes to inherit fields/methods."},
        {"question": "What does CSS stand for?", "options": ["Computer Style Sheets", "Cascading Style Sheets", "Creative Style Sheets", "Colorful Style Sheets"], "correct_option": "Cascading Style Sheets", "explanation": "CSS describes how HTML elements are displayed."},
        {"question": "Which is NOT a valid variable name in Python?", "options": ["my_var", "_var", "2var", "var2"], "correct_option": "2var", "explanation": "Variable names cannot start with a number."},
        {"question": "What is the complexity of accessing an array element by index?", "options": ["O(1)", "O(n)", "O(log n)", "O(n^2)"], "correct_option": "O(1)", "explanation": "Arrays provide constant time access."},
        {"question": "What is 'Polymorphism'?", "options": ["Hiding data", "Many forms", "Creating objects", "Linking tables"], "correct_option": "Many forms", "explanation": "Polymorphism allows methods to do different things based on the object."},
        {"question": "Which command initializes a git repository?", "options": ["git start", "git new", "git init", "git create"], "correct_option": "git init", "explanation": "git init creates a new local repository."},
        {"question": "What is the purpose of 'Foreign Key'?", "options": ["Unique ID", "Link two tables", "Speed up queries", "Encrypt data"], "correct_option": "Link two tables", "explanation": "Foreign keys enforce referential integrity between tables."},
        {"question": "In React, what is used to pass data to components?", "options": ["State", "Props", "Render", "Hooks"], "correct_option": "Props", "explanation": "Props (properties) are read-only inputs passed to components."},
        {"question": "Which layer ensures reliable transmission of data?", "options": ["Transport", "Network", "Session", "Physical"], "correct_option": "Transport", "explanation": "TCP at the Transport layer ensures reliability."},
        {"question": "What is a 'deadlock'?", "options": ["Memory leak", "Infinite loop", "Two processes waiting for each other", "System crash"], "correct_option": "Two processes waiting for each other", "explanation": "A standstill where neither process can proceed."},
        {"question": "Which is a NoSQL database?", "options": ["MySQL", "PostgreSQL", "MongoDB", "Oracle"], "correct_option": "MongoDB", "explanation": "MongoDB is a document-oriented NoSQL database."},
        {"question": "What does JSON stand for?", "options": ["JavaScript Object Notation", "Java Standard Output Network", "JavaScript Online Node", "Java Source Object Network"], "correct_option": "JavaScript Object Notation", "explanation": "Lightweight data interchange format."},
        {"question": "Which operator is used for string concatenation in Python?", "options": [".", "+", "&", "concat()"], "correct_option": "+", "explanation": "'Hello' + 'World' combines the strings."},
        {"question": "What is the default port for HTTP?", "options": ["21", "22", "80", "443"], "correct_option": "80", "explanation": "Port 80 is standard for unsecured web traffic."},
        {"question": "Which loop is best when the number of iterations is known?", "options": ["While", "Do-While", "For", "Until"], "correct_option": "For", "explanation": "For loops are designed for iterating a specific number of times."},
        {"question": "What is 'Recursion'?", "options": ["A loop", "A function calling itself", "A database query", "A sorting method"], "correct_option": "A function calling itself", "explanation": "Recursion solves problems by breaking them into smaller instances."},
        {"question": "What does API stand for?", "options": ["Application Programming Interface", "Advanced Program Integration", "Automated Process Interaction", "Apple Pie Ingredients"], "correct_option": "Application Programming Interface", "explanation": "APIs allow different software to talk to each other."},
        {"question": "Which of these is a mutable data type in Python?", "options": ["Tuple", "String", "List", "Integer"], "correct_option": "List", "explanation": "Lists can be modified after creation."},
        {"question": "What is the purpose of 'Constructor'?", "options": ["Delete object", "Initialize object", "Copy object", "Print object"], "correct_option": "Initialize object", "explanation": "Constructors set up the initial state of an object."},
        {"question": "In SQL, which clause is used to filter records?", "options": ["GROUP BY", "ORDER BY", "WHERE", "SELECT"], "correct_option": "WHERE", "explanation": "The WHERE clause filters records that fulfill a specified condition."},
        {"question": "What does GUI stand for?", "options": ["Graphical User Interface", "Global User Interface", "Game User Interaction", "General Unit Interface"], "correct_option": "Graphical User Interface", "explanation": "GUI allows users to interact with electronic devices through icons."},
        {"question": "Which one is NOT a cloud platform?", "options": ["AWS", "Azure", "GCP", "Hadoop"], "correct_option": "Hadoop", "explanation": "Hadoop is a framework for distributed storage, not a cloud service provider."},
        {"question": "What is 'Encapsulation' in OOP?", "options": ["Hiding implementation details", "Creating many forms", "Inheriting classes", "Writing loops"], "correct_option": "Hiding implementation details", "explanation": "Encapsulation restricts direct access to some of an object's components."},
        {"question": "Which tag is used for line break in HTML?", "options": ["<lb>", "<br>", "<break>", "<newline>"], "correct_option": "<br>", "explanation": "<br> inserts a single line break."},
        {"question": "What is 1024 bytes equal to?", "options": ["1 KB", "1 MB", "1 GB", "1 Bit"], "correct_option": "1 KB", "explanation": "1024 Bytes = 1 Kilobyte."},
        {"question": "Which keyword is used to inherit a class in Java?", "options": ["inherits", "extends", "implements", "uses"], "correct_option": "extends", "explanation": "Java uses 'extends' for class inheritance."},
        {"question": "What is the difference between == and === in JavaScript?", "options": ["No difference", "== checks value, === checks value and type", "== checks type", "=== is assignment"], "correct_option": "== checks value, === checks value and type", "explanation": "=== is the strict equality operator."},
        {"question": "What is 'Git'?", "options": ["A programming language", "A version control system", "A database", "A server"], "correct_option": "A version control system", "explanation": "Git tracks changes in source code."},
        {"question": "Which command is used to run a Python script?", "options": ["run script.py", "python script.py", "execute script.py", "go script.py"], "correct_option": "python script.py", "explanation": "Standard command to execute a python file."},
        {"question": "What is an 'Array'?", "options": ["A collection of items of same type", "A linked list", "A database", "A single variable"], "correct_option": "A collection of items of same type", "explanation": "Arrays store multiple values of the same type in contiguous memory."},
        {"question": "What does DNS stand for?", "options": ["Data Network System", "Domain Name System", "Digital Name Server", "Domain Network Service"], "correct_option": "Domain Name System", "explanation": "DNS translates domain names to IP addresses."},
        {"question": "Which of these is a valid boolean in Java?", "options": ["True", "true", "TRUE", "yes"], "correct_option": "true", "explanation": "Java uses lowercase 'true' and 'false'."},
        {"question": "What is a 'Bug'?", "options": ["A feature", "An error in code", "A virus", "A hardware fault"], "correct_option": "An error in code", "explanation": "A bug is a flaw producing incorrect or unexpected results."},
        {"question": "Which protocol sends email?", "options": ["POP3", "SMTP", "IMAP", "HTTP"], "correct_option": "SMTP", "explanation": "Simple Mail Transfer Protocol is used for sending emails."},
        {"question": "What is 'Agile'?", "options": ["A coding language", "A software development methodology", "A database", "A hardware component"], "correct_option": "A software development methodology", "explanation": "Agile focuses on iterative development and collaboration."}
    ],
    "Core Subjects": [
        {"question": "Which of the following is a volatile memory?", "options": ["ROM", "HDD", "RAM", "SSD"], "correct_option": "RAM", "explanation": "RAM loses its data when the power is turned off."},
        {"question": "What is the main function of an Operating System?", "options": ["Manage hardware and software resources", "Compile code", "Design websites", "Protect against viruses"], "correct_option": "Manage hardware and software resources", "explanation": "The OS acts as an intermediary between the user and computer hardware."},
        {"question": "In DBMS, what does ACID stand for?", "options": ["Atomicity, Consistency, Isolation, Durability", "Automated, Consistent, Isolated, Database", "Atomicity, Complex, Isolation, Data", "None of the above"], "correct_option": "Atomicity, Consistency, Isolation, Durability", "explanation": "ACID properties ensure reliable processing of database transactions."},
        {"question": "Which layer of the OSI model is responsible for routing?", "options": ["Physical", "Data Link", "Network", "Transport"], "correct_option": "Network", "explanation": "The Network layer handles logical addressing (IP) and routing."},
        {"question": "What is 'Deadlock' in OS?", "options": ["A system shutdown", "A situation where processes block each other indefinitely", "A memory leak", "A type of virus"], "correct_option": "A situation where processes block each other indefinitely", "explanation": "Deadlock occurs when two processes are each waiting for the other to release a resource."},
        {"question": "Which scheduling algorithm is non-preemptive?", "options": ["Round Robin", "FCFS", "SRTF", "Priority (Preemptive)"], "correct_option": "FCFS", "explanation": "First-Come-First-Serve runs a process until it finishes."},
        {"question": "What is 'Normalization' in DBMS?", "options": ["Increasing redundancy", "Organizing data to reduce redundancy", "Deleting tables", "Creating backups"], "correct_option": "Organizing data to reduce redundancy", "explanation": "Normalization minimizes data duplication."},
        {"question": "What is the full form of TCP?", "options": ["Transmission Control Protocol", "Transfer Control Protocol", "Transmission Central Protocol", "Total Control Protocol"], "correct_option": "Transmission Control Protocol", "explanation": "TCP is a core protocol of the Internet Protocol Suite."},
        {"question": "Which data structure is used for recursion?", "options": ["Queue", "Stack", "Tree", "Graph"], "correct_option": "Stack", "explanation": "The system call stack stores function calls."},
        {"question": "What is 'Paging' in OS?", "options": ["Memory management scheme", "Disk formatting", "Process scheduling", "Input/Output"], "correct_option": "Memory management scheme", "explanation": "Paging retrieves data from secondary storage in same-size blocks."},
        {"question": "What does SQL stand for?", "options": ["Structured Query Language", "Simple Query Language", "Standard Query Link", "System Question Language"], "correct_option": "Structured Query Language", "explanation": "SQL is standard for relational databases."},
        {"question": "What is a 'Kernel'?", "options": ["Core of the OS", "A hardware chip", "A user application", "A type of memory"], "correct_option": "Core of the OS", "explanation": "The kernel has complete control over everything in the system."},
        {"question": "Which join returns all records when there is a match in either left or right table?", "options": ["Inner Join", "Left Join", "Right Join", "Full Outer Join"], "correct_option": "Full Outer Join", "explanation": "Full Join combines Left and Right joins."},
        {"question": "What is 'Throughput'?", "options": ["Number of processes completed per unit time", "CPU speed", "Memory size", "Disk space"], "correct_option": "Number of processes completed per unit time", "explanation": "Throughput is a measure of system performance."},
        {"question": "Which protocol is stateless?", "options": ["FTP", "HTTP", "TCP", "SMTP"], "correct_option": "HTTP", "explanation": "HTTP does not retain information about previous requests."},
        {"question": "What is a 'Semaphore'?", "options": ["A signaling mechanism", "A hardware device", "A virus", "A network cable"], "correct_option": "A signaling mechanism", "explanation": "Semaphores control access to common resources by multiple processes."},
        {"question": "What is 'Virtual Memory'?", "options": ["Cloud storage", "Illusion of large main memory", "Graphics memory", "Cache"], "correct_option": "Illusion of large main memory", "explanation": "It uses hardware and software to allow a computer to compensate for physical memory shortages."},
        {"question": "Which is NOT a type of OS?", "options": ["Batch", "Time-sharing", "Real-time", "Flowchart"], "correct_option": "Flowchart", "explanation": "Flowchart is a diagram, not an OS."},
        {"question": "What is 'Index' in DBMS?", "options": ["A data structure to speed up retrieval", "A list of tables", "A type of query", "A backup"], "correct_option": "A data structure to speed up retrieval", "explanation": "Indexes improve the speed of data retrieval operations."},
        {"question": "What is the 'Ping' command used for?", "options": ["Test connectivity", "Delete files", "Format disk", "Compile code"], "correct_option": "Test connectivity", "explanation": "Ping checks reachability of a host on an IP network."},
        {"question": "What is 'Context Switching'?", "options": ["Changing CPU from one process to another", "Switching power", "Changing users", "Moving files"], "correct_option": "Changing CPU from one process to another", "explanation": "Storing state of active process and loading state of next process."},
        {"question": "What is 'IPV4' address length?", "options": ["32 bits", "64 bits", "128 bits", "16 bits"], "correct_option": "32 bits", "explanation": "IPv4 uses 32-bit addresses."},
        {"question": "Which topology requires a central hub?", "options": ["Bus", "Ring", "Star", "Mesh"], "correct_option": "Star", "explanation": "In Star topology, all nodes connect to a central device."},
        {"question": "What is 'Thrashing'?", "options": ["Excessive paging", "Hard disk failure", "CPU overheating", "Network congestion"], "correct_option": "Excessive paging", "explanation": "When the OS spends more time paging than executing."},
        {"question": "What is a 'Transaction' in DBMS?", "options": ["A unit of work", "A table", "A query", "A database"], "correct_option": "A unit of work", "explanation": "A sequence of operations treated as a single logical unit."},
        {"question": "Which is a DDL command?", "options": ["SELECT", "INSERT", "CREATE", "UPDATE"], "correct_option": "CREATE", "explanation": "Data Definition Language commands define structure (CREATE, DROP)."},
        {"question": "What is 'Latency'?", "options": ["Time delay", "Bandwidth", "Speed", "Volume"], "correct_option": "Time delay", "explanation": "Latency is the time interval between stimulation and response."},
        {"question": "What does 'MAC' address stand for?", "options": ["Media Access Control", "Memory Access Code", "Main Area Control", "Mobile Access Center"], "correct_option": "Media Access Control", "explanation": "Unique identifier assigned to a network interface controller."},
        {"question": "What is 'Mutex'?", "options": ["Mutual Exclusion Object", "Multi-User Text", "Memory Extension", "Micro Exchange"], "correct_option": "Mutual Exclusion Object", "explanation": "Ensures only one thread accesses a resource at a time."},
        {"question": "Which key uniquely identifies a row in a table?", "options": ["Foreign Key", "Primary Key", "Super Key", "Candidate Key"], "correct_option": "Primary Key", "explanation": "Primary Key is unique and not null."},
        {"question": "What is 'Booting'?", "options": ["Starting the computer", "Formatting", "Installing OS", "Running a program"], "correct_option": "Starting the computer", "explanation": "Process of loading the OS into memory."},
        {"question": "What is 'Spooling'?", "options": ["Simultaneous Peripheral Operations On-Line", "System Processing Offline", "Simple Program Logic", "Speedy Operation"], "correct_option": "Simultaneous Peripheral Operations On-Line", "explanation": "Used for buffering data for I/O devices (like printers)."},
        {"question": "Which layer provides encryption?", "options": ["Application", "Presentation", "Session", "Transport"], "correct_option": "Presentation", "explanation": "The Presentation layer handles encryption and decryption."},
        {"question": "What is 'Fragmentation'?", "options": ["Wasted memory space", "Disk cleaning", "File compression", "Data recovery"], "correct_option": "Wasted memory space", "explanation": "Storage space used inefficiently, reducing capacity."},
        {"question": "What is 'Shell'?", "options": ["Interface between user and kernel", "Hardware component", "A virus", "Antivirus"], "correct_option": "Interface between user and kernel", "explanation": "Command line interpreter."},
        {"question": "What is 'View' in SQL?", "options": ["Virtual table", "Real table", "Index", "Key"], "correct_option": "Virtual table", "explanation": "A view is a virtual table based on the result-set of an SQL statement."},
        {"question": "What is 'Cache Memory'?", "options": ["High speed memory", "Slow memory", "Secondary storage", "Cloud storage"], "correct_option": "High speed memory", "explanation": "Stores frequently used instructions/data."},
        {"question": "What is 'Firewall'?", "options": ["Network security system", "Hardware cooler", "Antivirus software", "Operating system"], "correct_option": "Network security system", "explanation": "Monitors and controls incoming and outgoing network traffic."},
        {"question": "What is 'UDP'?", "options": ["User Datagram Protocol", "Universal Data Protocol", "Unified Data Process", "User Data Protection"], "correct_option": "User Datagram Protocol", "explanation": "Connectionless protocol, faster but less reliable than TCP."},
        {"question": "What is 'Denormalization'?", "options": ["Adding redundancy to optimize performance", "Removing redundancy", "Deleting data", "Creating keys"], "correct_option": "Adding redundancy to optimize performance", "explanation": "Strategy used on a normalized database to increase read performance."},
        {"question": "What is 'Race Condition'?", "options": ["Output depends on timing of threads", "Fast CPU", "Network speed", "Disk error"], "correct_option": "Output depends on timing of threads", "explanation": "Occurs when multiple threads access shared data concurrently."},
        {"question": "What is 'Interrupt'?", "options": ["Signal to CPU to stop current task", "System crash", "Power failure", "User input"], "correct_option": "Signal to CPU to stop current task", "explanation": "Signal to the processor emitted by hardware or software."},
        {"question": "Which is a DML command?", "options": ["CREATE", "ALTER", "INSERT", "DROP"], "correct_option": "INSERT", "explanation": "Data Manipulation Language (INSERT, UPDATE, DELETE)."},
        {"question": "What is 'Schema'?", "options": ["Structure of database", "Data inside table", "User account", "Query"], "correct_option": "Structure of database", "explanation": "Logical configuration of all or part of a relational database."},
        {"question": "What is 'Turnaround Time'?", "options": ["Time from submission to completion", "Waiting time", "Execution time", "Response time"], "correct_option": "Time from submission to completion", "explanation": "Total time taken for a process to complete."},
        {"question": "What is 'Kernel Mode'?", "options": ["Privileged mode", "User mode", "Safe mode", "Sleep mode"], "correct_option": "Privileged mode", "explanation": "Mode where code has unrestricted access to hardware."},
        {"question": "What is 'Socket'?", "options": ["Endpoint for communication", "Electric plug", "CPU slot", "Memory type"], "correct_option": "Endpoint for communication", "explanation": "Combination of IP address and port number."},
        {"question": "What is 'Broadcasting'?", "options": ["Sending data to all nodes", "Sending to one node", "Receiving data", "Storing data"], "correct_option": "Sending data to all nodes", "explanation": "Transmitting a packet that will be received by every device on the network."},
        {"question": "What is 'Alias' in SQL?", "options": ["Temporary name for table/column", "Permanent name", "Password", "User ID"], "correct_option": "Temporary name for table/column", "explanation": "Used to give a table, or a column in a table, a temporary name."},
        {"question": "What is 'Starvation'?", "options": ["Process waits indefinitely", "Low memory", "No power", "Disk full"], "correct_option": "Process waits indefinitely", "explanation": "Low priority processes may never execute."}
    ]
}

def clean_json_response(raw_text):
    """Robust cleaner to extract JSON from messy AI output"""
    try:
        # 1. Try direct parse
        return json.loads(raw_text)
    except:
        # 2. Extract from markdown blocks
        match = re.search(r"```json\s*(\{.*?\})\s*```", raw_text, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        # 3. Find first { and last }
        start = raw_text.find("{")
        end = raw_text.rfind("}") + 1
        if start != -1 and end != -1:
            try:
                return json.loads(raw_text[start:end])
            except:
                return None
        return None

def generate_quiz_questions(category, sub_category, difficulty, num_questions):
    api_key = os.getenv("GROQ_API_KEY")
    
    # --- 1. SETUP CLIENT ---
    if not api_key:
        print("⚠️ API Key Missing. Using Backup.")
        return BACKUP_DB.get(category, BACKUP_DB["Technical Round"])[:num_questions]

    client = Groq(api_key=api_key)

    system_prompt = f"""
    You are a Technical Interviewer. Generate {num_questions} questions for {sub_category} ({category}).
    Level: {difficulty}.
    Output STRICT JSON only: {{ "quiz": [ {{ "question": "...", "options": ["A","B","C","D"], "correct_option": "A", "explanation": "..." }} ] }}
    """

    # --- 2. RETRY LOOP (Try 3 times) ---
    for attempt in range(3):
        try:
            print(f"📡 Attempt {attempt+1}/3 calling Groq...")
            
            # Using the fast model to avoid "Service Busy"
            completion = client.chat.completions.create(
                messages=[{"role": "system", "content": system_prompt}],
                model="llama3-8b-8192", 
                response_format={"type": "json_object"},
                temperature=0.5,
                timeout=10 # Short timeout so we fail fast to backup
            )
            
            data = clean_json_response(completion.choices[0].message.content)
            
            if data and "quiz" in data and len(data["quiz"]) > 0:
                print("✅ Success!")
                return data["quiz"]
            
        except Exception as e:
            print(f"⚠️ Error on attempt {attempt+1}: {e}")
            time.sleep(1) # Wait 1 second before retry

    # --- 3. ULTIMATE FAIL-SAFE ---
    # If we reach here, the API failed 3 times. Return backup data silently.
    print("🚨 All API attempts failed. Serving Backup Data.")
    
    # Return questions based on category, or default to Technical
    fallback = BACKUP_DB.get(category)
    if not fallback:
        fallback = BACKUP_DB["Technical Round"]
    
    # Return random selection so it doesn't look static
    # If user wants more than we have, return all
    if num_questions > len(fallback):
        return fallback
    
    return random.sample(fallback, num_questions)