# Lock-the-vote--Blockchain (E-Voting System Using Blockchain)


E-voting is an electronic approach to casting and counting votes that significantly reduces organizational costs and increases voter participation. However, traditional e-voting systems often suffer from a **single point of failure**, where even a minor manipulation can impact the entire election process.

This project enhances the reliability of e-voting by integrating **blockchain technology**, ensuring **transparency, immutability, and trust** in the voting workflow. Votes are recorded in a distributed manner, making the system resistant to tampering and unauthorized modifications.

<br/>

## Key Features
- Secure voter authentication and authorization
- One-person-one-vote enforcement
- Detection and prevention of duplicate voting
- Blockchain-based vote recording for tamper resistance
- Distributed node synchronization for transparency
- Real-time vote counting
- RESTful APIs for system interaction


<br/>

## System Architecture & Workflow
The system follows the workflow illustrated in the project flowchart:

1. **Candidate & Voter Registration**
   - Candidate and voter information is stored in a MySQL database.
2. **Blockchain Network Initialization**
   - All nodes are connected to maintain distributed transparency.
3. **Vote Casting**
   - Voters submit credentials (username and password).
   - Validation checks:
     - Unauthorized voter → *“Not authorized for voting”*
     - Duplicate vote → *“Already voted”*
4. **Vote Processing**
   - Valid votes are saved.
   - Vote count is incremented for the selected candidate.
5. **Block Creation**
   - After every 5 successful votes:
     - Votes are broadcast to all nodes
     - Votes are registered as a blockchain transaction
6. **Result Generation**
   - Final election results are generated after voting completion.

<br/>

## Tech Stack
- **Backend:** Python (Flask)
- **Database:** MySQL
- **Blockchain:** Custom blockchain implementation
- **API Testing:** Postman
- **Architecture:** RESTful API-based system

<br/>



## API Usage
The application exposes multiple REST APIs using Flask:
- `GET` APIs for fetching system data
- `POST` APIs for voter actions and vote casting

All APIs were tested and validated using **Postman**.

## How to Run the Project

### Step 1: Start the Server
```bash
python app.py
```

Step 2: Access the Local Server

http://127.0.0.1:5000
<br/>

Step 3: Call APIs Using Postman

Use the following format: <br>
http://127.0.0.1:5000/{method_name} <br>
Select the appropriate request type (GET or POST).



Sample POST Request:
{
  "voters": "A",
  "candidates": "Z"
}

<br/>

## Project Highlights

* Demonstrates real-world use of blockchain for secure voting
* Implements distributed data integrity and transparency
* Showcases backend development using Flask and MySQL
* Follows clean API design and system workflow principles



## Future Improvements

* Implement cryptographic hashing for enhanced block security
* Add voter anonymity using public-private key encryption
* Deploy smart contracts for automated vote validation
* Build a frontend UI for better usability
* Deploy the system on cloud infrastructure


