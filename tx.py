import configobj

config = configobj.ConfigObj('.env')
publicKey = config['publicKey']
privateKey = config['privateKey']
recentTransactions = []


def sendTransaction(w3, to_address):
    nonce = w3.eth.getTransactionCount(publicKey)
    # gasPrice = w3.toWei('50', 'gwei')
    value = w3.toWei(0.1, 'ether')
    tx = {
        'nonce': nonce,
        'to': to_address,
        'value': value,
        'gas': 2000000,
        'gasPrice': 0
    }
    # sign the transaction
    signed_tx = w3.eth.account.sign_transaction(tx, privateKey)
    # send transaction
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_hash = w3.toHex(tx_hash)
    return tx_hash
