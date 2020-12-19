import os
import cryptography.fernet
from typing import Callable


class Crypt:
    remove_original = False
    print_only = False
    key = ""

    def read_file(self, path: str) -> bytes:
        with open(path, "rb") as f:
            file_content = f.read()
        return file_content

    def write_file(self, path: str, data: bytes) -> None:
        with open(path, "wb") as f:
            f.write(data)

    def encrypt_content(self, key: str, data: bytes) -> bytes:
        fernet = cryptography.fernet.Fernet(key)
        return fernet.encrypt(data)

    def decrypt_content(self, key: str, encrypted_data: bytes) -> bytes:
        fernet = cryptography.fernet.Fernet(key)
        return fernet.decrypt(encrypted_data)

    def generate_key(self) -> bytes:
        return cryptography.fernet.Fernet.generate_key()

    def crypt_files(self, path: str, cipher: Callable[[str], None]) -> None:
        if os.path.isdir(path):
            for element in os.listdir(path):
                self.crypt_files(os.path.join(path, element), cipher)
        else:
            cipher(path)

    def _encrypt(self, path: str) -> None:
        print(f"Encrypting {path}...", end=" ")
        if ".encrypted" in path:
            print("the file seems to be encrypted already.")
            return
        try:
            data = self.read_file(path)
        except Exception as exception:
            print(exception)
            return
        encrypted_data = self.encrypt_content(self.key, data)
        new_path = path + ".encrypted"
        try:
            self.write_file(new_path, encrypted_data)
        except Exception as exception:
            print(exception)
            return
        if self.remove_original:
            try:
                os.remove(path)
            except Exception as exception:
                print(exception)
            else:
                print("done.")

    def encrypt(self, file_path: str, key: str, remove: bool = False) -> None:
        self.key = key
        self.remove_original = remove
        self.crypt_files(file_path, self._encrypt)

    def _decrypt(self, path: str) -> None:
        print(f"Decrypting {path}...", end=" ")
        encrypted_data = self.read_file(path)
        try:
            decrypted_data = self.decrypt_content(self.key, encrypted_data)
        except Exception as exception:
            print(exception)
            return
        if self.print_only:
            print("\n" + decrypted_data.decode())
            return
        # without .encrypted
        new_path = path[:-10]
        self.write_file(new_path, decrypted_data)
        try:
            os.remove(path)
        except Exception as exception:
            print(exception)
        else:
            print("done.")

    def decrypt(self, file_path: str, key: str, print_only: bool) -> None:
        self.key = key
        self.print_only = print_only
        self.crypt_files(file_path, self._decrypt)

    def generate(self, output_path: str) -> None:
        key = self.generate_key()
        try:
            self.write_file(f"{output_path}/key.protectme", key)
        except Exception as exception:
            print(exception)
        else:
            print("Key saved.")

    def new(self, content: str, key: str, output_path: str = "") -> None:
        if not output_path:
            output_path = os.getcwd()
        new_path = output_path + ".encrypted"
        encrypted_data = self.encrypt_content(key, content.encode())
        try:
            self.write_file(new_path, encrypted_data)
        except Exception as exception:
            print(exception)
        else:
            print("File has been successfully saved.")
