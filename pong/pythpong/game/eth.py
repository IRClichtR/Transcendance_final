from web3 import Web3, AsyncWeb3
from django.conf import settings
import json
from game.models import Game, Tournament
from asgiref.sync import sync_to_async

def get_web3_instance():
    alchemy_url = settings.ALCHEMY_PROVIDER_URL
    w3 = Web3(Web3.HTTPProvider(alchemy_url))
    if w3.is_connected():
        return w3
    else:
        raise ConnectionError("Unable to connect to provider(Alchemy)")

def get_contract_instance(w3):
    contract_address = settings.CONTRACT_ADDRESS
    with open(settings.CONTRACT_ABI_PATH, 'r') as abi_file:
        contract_abi = json.load(abi_file)['abi']
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    return contract

def store_game_sync(contract, w3, params):
    account_address = settings.OWNER_ADDRESS
    private_key = settings.OWNER_PRIVATE_KEY
    nonce = w3.eth.get_transaction_count(account_address)
    function_call = contract.functions.storeGame(
        params['semifinal1_start_time'],
        params['semifinal1_player1'],
        params['semifinal1_player1_id'],
        params['semifinal1_player2'],
        params['semifinal1_player2_id'],
        params['semifinal1_score1'],
        params['semifinal1_score2'],
        params['semifinal2_start_time'],
        params['semifinal2_player1'],
        params['semifinal2_player1_id'],
        params['semifinal2_player2'],
        params['semifinal2_player2_id'],
        params['semifinal2_score1'],
        params['semifinal2_score2'],
        params['final_start_time'],
        params['final_player1'],
        params['final_player2'],
        params['final_score1'],
        params['final_score2']
    ).build_transaction({
        "from": account_address,
        "nonce": nonce,
    })
    gas_estimate = w3.eth.estimate_gas(function_call)
    gas_price = w3.to_wei('100', 'gwei')

    unsent_tx = {
        "from": account_address,
        "nonce": nonce,
        "gas": gas_estimate,
        "gasPrice": gas_price,
        "to": settings.CONTRACT_ADDRESS,
        "data": function_call['data'],
    }

    try:
        signed_tx = w3.eth.account.sign_transaction(unsent_tx, private_key).raw_transaction
        tx_hash = w3.eth.send_raw_transaction(signed_tx)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt
    except ValueError as e:
        if 'replacement transaction underpriced' in str(e):
            gas_price = int(gas_price * 1.1)
            unsent_tx['gasPrice'] = gas_price
            signed_tx = w3.eth.account.sign_transaction(unsent_tx, private_key).raw_transaction
            tx_hash = w3.eth.send_raw_transaction(signed_tx)
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            return receipt
        else:
            raise e

def store_game(params):
    try:
        w3 = get_web3_instance()
    except Exception as e:
        print(f"Error while get_w3_instance: {e}")
    try:
        contract = get_contract_instance(w3)
    except Exception as e:
        print(f"Error while get_contract_instance: {e}")
    try:
        receipt = store_game_sync(contract, w3, params)
        return receipt
    except Exception as e:
        print(f"Error while store_game_sync: {e}")

def store_data(tournament):
    params = {
        'semifinal1_start_time': tournament.semifinal1.start_time,
        'semifinal1_player1': tournament.semifinal1.player_names[0],
        'semifinal1_player1_id' : int(tournament.semifinal1.player_ids[0]),
        'semifinal1_player2': tournament.semifinal1.player_names[1],
        'semifinal1_player2_id' : int(tournament.semifinal1.player_ids[1]),
        'semifinal1_score1': tournament.semifinal1.points[0],
        'semifinal1_score2': tournament.semifinal1.points[1],
        'semifinal2_start_time': tournament.semifinal2.start_time,
        'semifinal2_player1': tournament.semifinal2.player_names[0],
        'semifinal2_player1_id' : int(tournament.semifinal2.player_ids[0]),
        'semifinal2_player2': tournament.semifinal2.player_names[1],
        'semifinal2_player2_id' : int(tournament.semifinal2.player_ids[1]),
        'semifinal2_score1': tournament.semifinal2.points[0],
        'semifinal2_score2': tournament.semifinal2.points[1],
        'final_start_time': tournament.final.start_time,
        'final_player1': tournament.final.player_names[0],
        'final_player2': tournament.final.player_names[1],
        'final_score1': tournament.final.points[0],
        'final_score2': tournament.final.points[1]
    }

    receipt = store_game(params)
    print(f"Data stored successfully: {receipt}")

def get_all_tournament_games():
    try:
        w3 = get_web3_instance()
    except Exception as e:
        print(f"Error while get_w3_instance: {e}")
    try:
        contract = get_contract_instance(w3)
    except Exception as e:
        print(f"Error while get_contract_instance: {e}")
    try:
        data = contract.functions.getPongGames().call()
        return {
            "data" : data
        }
    except Exception as e:
        print(f"Error while calling contract function: {e}")
        return None
