# Fake News Detection Network using Blockchain

## Project Overview

This project develops a blockchain-based network for detecting fake news, leveraging NLP bases ML models and a consortium of auditors. The system operates on a consortium blockchain, enabling anonymous participation for readers to access news and submit news items as transactions.

## Running the Project

#### _Ensure your internet is working_ before proceeding

1. Clone the repository locally.

2. Change working directory into the repository folder
    ```
    cd BlockchainProject2
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


   
### Key Features

- **Machine Learning Model**: Utilizes a model trained on extensive datasets to assign a probability score indicating the likelihood of news being fake.
- **Auditor Participation**: Auditors, verified through a third-party service (e.g., Intel SGX), are responsible for block creation and news validation via voting.
- **Reputation System**: Differentiates between auditors and readers in terms of initial reputation scores, which are adjusted based on activity.
- **Consensus Mechanism**: Uses Proof of Stake (PoS) for secure and efficient consensus.

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

