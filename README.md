# Healthcare AI Blockchain

Healthcare prediction demo with a FastAPI backend and a React frontend. The current flow lets a user submit patient details, receive an AI risk assessment, and prepares the project for later blockchain storage.

## Project Structure

- `backend/` FastAPI API and prediction logic
- `frontend/` React + Vite user interface
- `blockchain/` Hardhat smart contract project
- `ai/` earlier experimental blockchain and anomaly-detection files

## Run the Backend

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r backend/requirements.txt
```

3. Start the API from the project root:

```bash
uvicorn backend.main:app --reload
```

4. Open `http://127.0.0.1:8000/docs` to test the API.

## Run the Frontend

1. Move into the frontend folder:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm run dev
```

4. Open the local URL shown in the terminal, usually `http://localhost:5173`.

## Run the Blockchain Integration

1. Move into the blockchain folder:

```bash
cd blockchain
```

2. Install dependencies:

```bash
npm install
```

3. Start a local Hardhat chain:

```bash
npm run node
```

4. In a new terminal, deploy the contract:

```bash
npm run deploy
```

5. Copy `backend/.env.example` to `backend/.env` and fill in:

```bash
BLOCKCHAIN_RPC_URL=http://127.0.0.1:8545
BLOCKCHAIN_CHAIN_ID=31337
BLOCKCHAIN_CONTRACT_ADDRESS=your_deployed_contract_address
BLOCKCHAIN_PRIVATE_KEY=one_of_the_private_keys_printed_by_hardhat
```

6. Restart the FastAPI backend. Every `/predict` call will then attempt to store the prediction on chain.

## Frontend Configuration

The frontend calls the backend using `VITE_API_BASE_URL`. By default it uses `http://127.0.0.1:8000`.

To override it, create a `frontend/.env` file:

```bash
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## Current Status

- AI Logic: done
- Backend API: done
- Frontend UI: done
- Blockchain integration: done
- Final end-to-end blockchain flow: backend + frontend + blockchain ready for local testing
