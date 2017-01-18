import base64
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


class KeyPair(object):
    def generate(self):
        key = RSA.generate(2048)
        public_key = key.publickey().exportKey()
        private_key = key.exportKey()

        return {
            'public': public_key,
            'private': private_key
        }

    def sign(self, private_key, message):
        key = RSA.importKey(private_key)
        signer = PKCS1_v1_5.new(key)

        digest = SHA256.new()
        digest.update(message)

        signature = signer.sign(digest)

        return {
            'message': message,
            'signature': base64.b64encode(signature)
        }

    def verify(self, public_key, envelop):
        key = RSA.importKey(public_key)
        signer = PKCS1_v1_5.new(key)
        digest = SHA256.new()
        digest.update(envelop["message"])

        if signer.verify(digest, base64.b64decode(envelop["signature"])):
            return True

        return False
