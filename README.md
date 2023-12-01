# Fake News Detection Network using Blockchain

## Project Overview

This project develops a blockchain-based network for detecting fake news, leveraging NLP based ML model for assisting a consortium of auditors. The public part of the network enables anonymous participation for readers to access & submit news as transactions which are verified by auditors using a combination of PBFT & Proof of Stake consensus

<p align="center">
    <img src="Flowchart Images/ENTER NETWORK-1.jpeg" alt="Alt text" height="400" width="400">
</p>

### Running the Project

#### _Ensure your internet is working_ before proceeding

1. Clone the repository locally.

2. Change working directory into the repository folder
    ```
    cd Blockchain-Based-Fake-News-Detection-Network 
    ```

2. Install dependencies by running the command 
    (you can make a virtual environment if you want (recommended))
    ```
    pip install -r requirements.txt
    ```

3. Run the following command in your command line interface: 

    ```
    streamlit run screens/GUI.py 
    ```

    to start the blockchain project in your default browser.


4. Login/Sign up to continue
     - When signing up, the email should be in the format username@domain.service
     - Valid Certificate will be of the format ABCD****, for this POC.

5. If you receive an import error, kindly reload the page or run the commands in a new terminal. It is a streamlit bug rather than a code problem.

6. When you press "Go to Main", please wait for the server to initialise and connections. It will show a spinner & progress bar & take you to the main page automatically.

7. For viewing transactions in mempool or sent transactions, wait for the progress bar to load.

8. Similarly, please wait for the spinner showing "Please wait.." to finish before pressing buttons.

9. To upload a file, go to upload file page and upload a text file, attaching a transaction fee.

<p align="center">
    <img src="Flowchart Images/UPLOAD NEWS.jpeg" alt="Alt text" height="400" width="400">
</p>


10. To view sent news, go to the sent news page. Similarly for viewing mempool and broadcasted blocks etc. The pages are present in the navbar.

11. The timer for the next block proposer is shown on every screen. Once this counter reaches 0, a new block proposer is chosen which is visible on the VIEW BLOCK STATUS page.

12. If you are chosen as the block proposer, you'll be shown the transactions in mempool on the VIEW BLOCK STATUS page to vote on them as "fake" news or not while showing the sender reputation, ML model score etc.

<p align="center">
    <img src="Flowchart Images/CREATE BLOCK.jpeg" alt="Alt text" height="400" width="400">
</p>



13. You can again view the current confirmations on the block in VIEW BLOCK STATUS.

14. You can view changes to your reputation in the REPUTATION LOG. The reasons for these changes may be broadcasting fake news, not broadcasting a block when chosen as a proposer, etc. (better described in report)



<p align="center">
    <img src="Flowchart Images/VIEW BLOCK STATUS.jpeg" alt="Alt text" height="400" width="400">
</p>


   
### Key Features

- **Machine Learning Model**: Utilizes a model trained on extensive datasets to assign a probability score indicating the likelihood of news being fake.
- **Auditor Participation**: Auditors, verified through a third-party service (e.g., Intel SGX), are responsible for block creation and news validation via voting.
- **Reputation System**: Differentiates between auditors and readers in terms of initial reputation scores, which are adjusted based on activity.
- **Consensus Mechanism**: Uses Proof of Stake (PoS) for secure and efficient consensus.



<p align="center">
    <img src="Flowchart Images/VOTING BLOCK.jpeg" alt="Alt text" height="400" width="400">
</p>




### Network Structure

- **Public Network**: Allows anonymous readers to read and broadcast news, maintaining privacy.
- **Private Network**: Comprises authenticated auditors who can propose blocks and vote on news validity.

### Process Flow

1. **Auditor Joining**: Requires authentication proof for registration.
2. **Bootstrap Nodes**: Developer maintained nodes that are always active and used as entry points to the blockchain. They help discover peers in the network.
3. **Reader Joining**: Simple registration with minimal information.
4. **News Broadcasting**: Users can upload and broadcast news, accompanied by a machine learning model score.
5. **Block Creation and Voting**: Auditors propose and vote on blocks containing news transactions.
6. **Validation and Ledger Addition**: Blocks receiving majority votes are added to the blockchain, making the news visible with associated authenticity metrics.

### Output

News items are displayed with their title, text, ML model score, percentage of fake votes by auditors, and sender reputation, providing a comprehensive view of their credibility.

