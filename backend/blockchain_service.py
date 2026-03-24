import hashlib
import os
from typing import Any
from pathlib import Path

from dotenv import load_dotenv
from web3 import Web3

load_dotenv(Path(__file__).with_name(".env"))

CONTRACT_ABI = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "string", "name": "patientHash", "type": "string"},
            {"indexed": False, "internalType": "uint256", "name": "age", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "bloodPressure", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "sugarLevel", "type": "uint256"},
            {"indexed": False, "internalType": "string", "name": "riskLevel", "type": "string"},
            {"indexed": False, "internalType": "uint256", "name": "timestamp", "type": "uint256"},
        ],
        "name": "PredictionStored",
        "type": "event",
    },
    {
        "inputs": [
            {"internalType": "string", "name": "patientHash", "type": "string"},
            {"internalType": "uint256", "name": "age", "type": "uint256"},
            {"internalType": "uint256", "name": "bloodPressure", "type": "uint256"},
            {"internalType": "uint256", "name": "sugarLevel", "type": "uint256"},
            {"internalType": "string", "name": "riskLevel", "type": "string"},
        ],
        "name": "storePrediction",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "string", "name": "patientHash", "type": "string"},
            {"internalType": "uint256", "name": "index", "type": "uint256"},
        ],
        "name": "getPrediction",
        "outputs": [
            {"internalType": "string", "name": "", "type": "string"},
            {"internalType": "uint256", "name": "", "type": "uint256"},
            {"internalType": "uint256", "name": "", "type": "uint256"},
            {"internalType": "uint256", "name": "", "type": "uint256"},
            {"internalType": "string", "name": "", "type": "string"},
            {"internalType": "uint256", "name": "", "type": "uint256"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "string", "name": "patientHash", "type": "string"}],
        "name": "getPredictionCount",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
]


def _hash_patient(name: str) -> str:
    return hashlib.sha256(name.strip().lower().encode("utf-8")).hexdigest()


def _get_config() -> dict[str, str]:
    return {
        "rpc_url": os.getenv("BLOCKCHAIN_RPC_URL", ""),
        "contract_address": os.getenv("BLOCKCHAIN_CONTRACT_ADDRESS", ""),
        "private_key": os.getenv("BLOCKCHAIN_PRIVATE_KEY", ""),
        "chain_id": os.getenv("BLOCKCHAIN_CHAIN_ID", "1337"),
    }


def _is_enabled(config: dict[str, str]) -> bool:
    return all(
        [
            config["rpc_url"],
            config["contract_address"],
            config["private_key"],
        ]
    )


def store_prediction(
    name: str,
    age: int,
    bp: int,
    sugar: int,
    risk_level: str,
) -> dict[str, Any]:
    config = _get_config()

    if not _is_enabled(config):
        return {
            "enabled": False,
            "status": "skipped",
            "message": "Blockchain env vars are not configured.",
        }

    try:
        web3 = Web3(Web3.HTTPProvider(config["rpc_url"]))
        if not web3.is_connected():
            return {
                "enabled": True,
                "status": "error",
                "message": "Could not connect to the blockchain RPC endpoint.",
            }

        account = web3.eth.account.from_key(config["private_key"])
        contract = web3.eth.contract(
            address=Web3.to_checksum_address(config["contract_address"]),
            abi=CONTRACT_ABI,
        )
        patient_hash = _hash_patient(name)
        nonce = web3.eth.get_transaction_count(account.address)
        gas_price = web3.eth.gas_price

        transaction = contract.functions.storePrediction(
            patient_hash,
            age,
            bp,
            sugar,
            risk_level,
        ).build_transaction(
            {
                "from": account.address,
                "nonce": nonce,
                "chainId": int(config["chain_id"]),
                "gas": 300000,
                "gasPrice": gas_price,
            }
        )

        signed_transaction = account.sign_transaction(transaction)
        tx_hash = web3.eth.send_raw_transaction(signed_transaction.raw_transaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        return {
            "enabled": True,
            "status": "stored",
            "message": "Prediction stored on blockchain.",
            "transaction_hash": receipt.transactionHash.hex(),
            "patient_hash": patient_hash,
            "block_number": receipt.blockNumber,
        }
    except Exception as error:
        return {
            "enabled": True,
            "status": "error",
            "message": str(error),
        }
