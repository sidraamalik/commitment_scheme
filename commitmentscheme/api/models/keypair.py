from commitmentscheme.api.utils.keypair import KeyPair
from commitmentscheme.api.models.base import BaseModel



class KeyPairModel(BaseModel):
    def create(self, uid, commit=True):
        on_duplicate = "ON DUPLICATE KEY UPDATE private_key=%s, public_key=%s"
        query = "INSERT INTO keypair (uid, private_key, public_key) VALUES (%s, %s, %s)"

        pair = KeyPair().generate()

        self.db.execute(
            "{0} {1}".format(query, on_duplicate), 
            (uid,  pair["private"], pair["public"], pair["private"], pair["public"]))

        kp_id = self.db.get_insert_id()

        if commit is True:
            self.db.commit()

        return kp_id
