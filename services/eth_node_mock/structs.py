
ETH_EMBED_TRANSACTION = {
    'hash': 'default_hash',
    'nonce': int("300", 16),
    'blockHash': 'default_block_hash',
    'blockNumber': int("300", 16),
    'transactionIndex': int("300", 16),
    'from': 'default_from',
    'to': 'default_to',
    'gas': int("300", 16),
    'gasPrice': int("300", 16),
    'input': 'default_input'
}

ETH_ROOT_TRANSACTION = {
    "number": "0x1b4", # 436
    "block_hash": "default_block_hash",
    "parentHash": "0x9646252be9520f6e71339a8df9c55e4d7619deeb018d2a3f2d21fc165dde5eb5",
    "nonce": "0xe04d296d2460cfb8472af2c5fd05b5a214109c25688d3704aed5484f9a7792f2",
    "sha3Uncles": "0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347",
    "logsBloom": "0xe670ec64341771606e55d6b4ca35a1a6b75ee3d5145a99d05921026d1527331",
    "transactionsRoot": "0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421",
    "stateRoot": "0xd5855eb08b3387c0af375e9cdb6acfc05eb8f519e419b874b6ff2ffda7ed1dff",
    "miner": "0x4e65fda2159562a496f9f3522f89122a3088497a",
    "difficulty": "0x027f07", # 163591
    "totalDifficulty": "0x027f07", # 163591
    "extraData": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "size": "0x027f07", # 163591
    "gasLimit": "0x9f759", # 653145
    "gasUsed": "0x9f759", # 653145
    "timestamp": "0x54e34e8e", # 1424182926
    "transactions": [ETH_EMBED_TRANSACTION],
    "uncles": ["0x1606e5...", "0xd5145a9..."],
}