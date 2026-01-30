import hashlib
import os
import csv

class HashManager:
    def __init__(self):
        self.algorithms = ["MD5", "SHA256", "SHA512"]
        self.filename = "test_hashes.csv"

    def hash_password(self, plain_password, algorithm="SHA256"):
        """
        Hashes a single password using the specified algorithm.
        """
        algo = algorithm.upper()
        if algo == "MD5":
            return hashlib.md5(plain_password.encode()).hexdigest()
        elif algo == "SHA256":
            return hashlib.sha256(plain_password.encode()).hexdigest()
        elif algo == "SHA512":
            return hashlib.sha512(plain_password.encode()).hexdigest()
        else:
            return None

    def generate_hash_list(self, passwords, algorithm="SHA256"):
        """
        Takes a list of passwords and returns a list of (password, hash) tuples.
        """
        results = []
        for pwd in passwords:
            h = self.hash_password(pwd.strip(), algorithm)
            results.append((pwd.strip(), h))
        return results

    def save_hashes(self, hash_list, algorithm):
        """
        Appends generated hashes to a CSV file (Password, Hash, Algo).
        Simulates a 'shadow' file or database dump.
        """
        file_exists = os.path.isfile(self.filename)
        mode = 'a' if file_exists else 'w'
        
        try:
            with open(self.filename, mode, newline='') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["Plain_Password", "Hash_Value", "Algorithm"])
                
                for _, h_val in hash_list:
                    # In a real scenario we wouldn't save plain password in the same file obviously,
                    # but for this lab tool, we might want to keep track or just save the hash.
                    # Per requirements: "Store hashes in a test file"
                    # We will store just the hash and algo to simulate a target file for cracking.
                    writer.writerow(["***", h_val, algorithm])
            return self.filename
        except Exception as e:
            raise e

    def load_wordlist(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError("Wordlist file not found.")
        with open(filepath, 'r') as f:
            return [line.strip() for line in f.readlines() if line.strip()]
