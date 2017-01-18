import hashlib

class SecurePassword(object):
    def treat(self, password):
        h = hashlib.new('sha256')
        h.update(password)

        return h.hexdigest()
