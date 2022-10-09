#for calc hash 
import hashlib

PREFIX = '00000'
class Hash:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def create_block_hash(data:str, prev_hash:str = '', nonce_from = 0, nonce_to = 0):
        nonce = 0
        hash_str = 'FFFFFFFF'

        if(nonce_from == 0 and nonce_to == 0):
            nonce = 0
            while(hash_str[:len(PREFIX)] != PREFIX):
                # mine initial block
                block_data = data + prev_hash + str(nonce)
                hash_str = hashlib.sha1(str.encode(block_data)).hexdigest()
                nonce += 1
            return nonce - 1, hash_str
        else:
            # only mine with fixed range nonce
            nonce = nonce_from
            while(nonce < nonce_to):
                block_data = data + prev_hash + str(nonce)
                hash_str = hashlib.sha1(str.encode(block_data)).hexdigest()
                if hash_str[:len(PREFIX)] == PREFIX:
                    return nonce, hash_str 
                nonce += 1
            return None