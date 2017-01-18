from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

from commitmentscheme.api.models.base import BaseModel
from commitmentscheme.api.models.user import UserModel
from commitmentscheme.api.utils.aes import AESCipher
from commitmentscheme.api.utils.keypair import KeyPair
from commitmentscheme.api.common.errors import APIError


class MessageModel(BaseModel):
    def commit(self, username, message, secret, commit=True):
        if message.strip() == "":
            raise APIError("Need a valid message!", 400)

        cipher = AESCipher(secret)
        encrypted = cipher.encrypt(message)
        user = UserModel(self.db)
        user_data = user.read(username)
        envelop = KeyPair().sign(user_data["private_key"], encrypted)
        query = "INSERT INTO message (uid, message, signature) VALUES(%s, %s, %s)"
        self.db.execute(
            query,
            (user_data["uid"],
             envelop["message"],
             envelop["signature"]))

        mid = self.db.get_insert_id()
        if commit is True:
            self.db.commit()

        return mid

    def reveal(self, username, mid, secret, commit=True):
        user = UserModel(self.db)
        user_data = user.read(username)
        message_data = self.read(mid, MessageType.COMMITMENT)
        envelop = {
            'message': message_data["message"],
            'signature': message_data["signature"]
        }
        verified = KeyPair().verify(user_data["public_key"], envelop)
        if not verified:
            raise APIError("Signature mismatch!", 400)

        cipher = AESCipher(secret)
        decrypted = cipher.decrypt(message_data["message"]).strip()
        if not decrypted:
            raise APIError("Invalid secret!", 400)

        query = "UPDATE message SET message=%s, message_type=%s, signature='' WHERE id=%s"
        self.db.execute(
            query,
            (decrypted,
             MessageType.REVEALATION,
             mid))

        if commit is True:
            self.db.commit()

        return self.read(mid, MessageType.REVEALATION)

    def verify(self, username, mid):
        user = UserModel(self.db)
        user_data = user.read(username)
        message_data = self.read(mid, MessageType.COMMITMENT)
        envelop = {
            'message': message_data["message"],
            'signature': message_data["signature"]
        }
        verified = KeyPair().verify(user_data["public_key"], envelop)
        if not verified:
            raise APIError("Signature mismatch!", 400)

        return True

    def read(self, mid, message_type=None):
        part = ""
        if message_type is not None:
            part = " AND m.message_type={0}".format(message_type)

        query = (
            "SELECT u.id AS uid, u.username, kp.public_key, "
            "m.id AS mid, m.message, m.signature, m.message_type AS 'type' "
            "FROM user AS u INNER JOIN keypair AS kp ON "
            "u.id = kp.uid INNER JOIN message AS m ON u.id=m.uid "
            "WHERE m.id=%s{0}").format(part)

        message = self.db.query(query, (mid,))

        if not message:
            raise APIError("Message id not found!", 404)

        result = message.pop()
        result["type"] = self._map_message(result["type"])

        return result

    def get_all(self):
        # Pagination/limit etc required.
        query = (
            "SELECT u.username AS owner, m.id, m.message_type AS 'type'"
            "FROM user AS u INNER JOIN message AS m "
            "ON u.id=m.uid")

        messages = self.db.query(query)
        for message in messages:
            message["type"] = self._map_message(message["type"])

        return messages

    def _map_message(self, message_type):
        if message_type == MessageType.COMMITMENT:
            result = "COMMITMENT"
        elif message_type == MessageType.REVEALATION:
            result = "REVEALATION"
        else:
            result = message_type
        
        return result


class MessageType(object):
    COMMITMENT = 1
    REVEALATION = 2
