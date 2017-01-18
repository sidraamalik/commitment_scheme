from commitmentscheme.api.models.base import BaseModel
from commitmentscheme.api.models.keypair import KeyPairModel
from commitmentscheme.api.utils.password import SecurePassword
from commitmentscheme.api.common.errors import APIError


class UserModel(BaseModel):
    def create(self, username, password, commit=True):
        query = "INSERT INTO user (username, password) VALUES (%s, %s)"
        secure_password = SecurePassword()

        self.db.execute(query, (username, secure_password.treat(password)))
        uid = self.db.get_insert_id()

        if commit is True:
            self.db.commit()
        keypair = KeyPairModel(self.db)

        kpid = keypair.create(uid, False)

        if commit is True:
            self.db.commit()

        return uid

    def read(self, username=None):
        query = (
            "SELECT u.id AS uid, u.username, u.password, kp.id AS kpid, "
            "kp.private_key, kp.public_key "
            "FROM user AS u INNER JOIN keypair AS kp ON "
            "u.id = kp.uid WHERE u.username=%s")

        user = self.db.query(query, (username,))
        if not user:
            raise APIError("User not found!", 404)

        return user.pop()
