[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/AHFn7Vbn)
# Superjoin Hiring Assignment

### Welcome to Superjoin's hiring assignment! 🚀

### Objective
Build a solution that enables real-time synchronization of data between a Google Sheet and a specified database (e.g., MySQL, PostgreSQL). The solution should detect changes in the Google Sheet and update the database accordingly, and vice versa.

### Problem Statement
Many businesses use Google Sheets for collaborative data management and databases for more robust and scalable data storage. However, keeping the data synchronised between Google Sheets and databases is often a manual and error-prone process. Your task is to develop a solution that automates this synchronisation, ensuring that changes in one are reflected in the other in real-time.

### Requirements:
1. Real-time Synchronisation
  - Implement a system that detects changes in Google Sheets and updates the database accordingly.
   - Similarly, detect changes in the database and update the Google Sheet.
  2.	CRUD Operations
   - Ensure the system supports Create, Read, Update, and Delete operations for both Google Sheets and the database.
   - Maintain data consistency across both platforms.
   
### Optional Challenges (This is not mandatory):
1. Conflict Handling
- Develop a strategy to handle conflicts that may arise when changes are made simultaneously in both Google Sheets and the database.
- Provide options for conflict resolution (e.g., last write wins, user-defined rules).
    
2. Scalability: 	
- Ensure the solution can handle large datasets and high-frequency updates without performance degradation.
- Optimize for scalability and efficiency.

## Submission ⏰
The timeline for this submission is: **Next 2 days**

Some things you might want to take care of:
- Make use of git and commit your steps!
- Use good coding practices.
- Write beautiful and readable code. Well-written code is nothing less than a work of art.
- Use semantic variable naming.
- Your code should be organized well in files and folders which is easy to figure out.
- If there is something happening in your code that is not very intuitive, add some comments.
- Add to this README at the bottom explaining your approach (brownie points 😋)
- Use ChatGPT4o/o1/Github Co-pilot, anything that accelerates how you work 💪🏽. 

Make sure you finish the assignment a little earlier than this so you have time to make any final changes.

Once you're done, make sure you **record a video** showing your project working. The video should **NOT** be longer than 120 seconds. While you record the video, tell us about your biggest blocker, and how you overcame it! Don't be shy, talk us through, we'd love that.

We have a checklist at the bottom of this README file, which you should update as your progress with your assignment. It will help us evaluate your project.

- [x] My code's working just fine! 🥳
- [x] I have recorded a video showing it working and embedded it in the README ▶️
- [x] I have tested all the normal working cases 😎
- [x] I have even solved some edge cases (brownie points) 💪
- [x] I added my very planned-out approach to the problem at the end of this README 📜

## Got Questions❓
Feel free to check the discussions tab, you might get some help there. Check out that tab before reaching out to us. Also, did you know, the internet is a great place to explore? 😛

We're available at techhiring@superjoin.ai for all queries. 

All the best ✨.

## Developer's Section
### Features
- Automated Bi-directional Sync: Changes in the MySQL database or Google Sheets are automatically detected and reflected in the other platform every 20 seconds.
- CRUD Functionality: Easily add, update, and delete records from either platform. Changes are instantly synchronized.
- Manual Sync Option: A manual sync button is available to trigger synchronization on demand.
- Conflict Handling: The system uses a last-write-wins strategy to resolve any conflicts (optional feature, can be enhanced for user-defined conflict resolution).

### Technologies Used
- Flask: Backend web framework for creating APIs and handling CRUD operations.
- Google Sheets API: To interact with Google Sheets, fetch and update data.
- MySQL: For robust data storage and retrieval.
- Python threading: To enable continuous polling for real-time synchronization.
- Google API Client: For communicating with Google Sheets.

### Architecture
![Architecture](https://github.com/StackItHQ/pes-vaibhavprashanth/blob/main/static/Architecture_nobg_darkmode.png?)

This system follows a bi-directional polling and synchronization model:
1. Database to Google Sheets Sync:
- The system polls the MySQL database at regular intervals (every 20 seconds).
- If there are any new updates, inserts, or deletions in the database, those changes are pushed to Google Sheets.
2. Google Sheets to Database Sync:
- Similarly, the system polls the Google Sheets at regular intervals.
- Any new data or modifications are updated in the MySQL database.
3. Manual Sync:
- In addition to automated sync, users can trigger synchronization manually via a "Sync Data" button on the web interface.

### Conflict Handling
In case of simultaneous updates in both Google Sheets and MySQL, the system resolves conflicts using a last-write-wins approach. The more recent change (based on the last_updated timestamp) is applied across both platforms. You can enhance this by adding more complex conflict resolution logic, such as user-defined rules.

### Scalability and Performance
- The polling interval for synchronization is set to 20 seconds by default. You can modify this interval depending on your requirements for more frequent or less frequent sync.
- For handling larger datasets, consider optimizing database queries and using batch processing for updates to Google Sheets.




