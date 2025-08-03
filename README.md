🚀 MyTools Web App (**Flask + Mainframe Integration**)
A full-stack web application built using **Flask, z/OSMF, and Mainframe technologies (REXX + COBOL + JCL + DB2)**. It allows users to log in with RACF credentials and perform mainframe-related operations through a web interface such as selecting tools and checking or adding personal information like name and date of birth.

🚀 Features
- User Login: Secure login using **RACF** credentials
•	Tool Selection Page: Choose from available tools after login
•	Info Check Tool: Add or find a person by name, and if not found, add name and DOB (Date of Birth)
•	Modular Codebase: Logic separated into individual modules for scalability
•	Simple session management using Flask’s session
•	Demonstration of **z/OSMF REST services** connecting the Flask app to Mainframe for:
•	JCL submission
•	Mainframe dataset creation
•	Writing data to datasets
•	Retrieving job details from SDSF
•	**REXX** is used to interact with DB2 for selecting/updating data
•	**COBOL + DB2** handles input from the HTML UI for insert/update and error management
•	**JCL** is used to execute **REXX** and **COBOL** programs in batch mode


app2.py              # Main **Flask** application
login_logic.py       # Logic for **RACF** login functionality
mytools_logic.py     # Tool selection logic
infochk_logic.py     # Info check (search/add person, **DOB**)
logging_logic.py     # Logging setup (optional)
templates/           # **HTML** templates (Jinja2)
rexxdb2f.rexx        # **REXX** to connect to **DB2** and fetch data
cbldb2a.rexx         # **REXX** to read UI input and invoke **COBOL** via **ISPF EDIT macro**
cbldb2a.cob          # **COBOL** to insert data into **DB2** via **JCL**
