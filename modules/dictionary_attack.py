import hashlib
import csv
import os

class DictionaryAttacker:
    def __init__(self):
        self.running = False

    def load_targets(self, hash_file_path):
        """
        Loads hashes from a CSV file.
        Expected format: Plain(opt), Hash, Algo
        Returns a dictionary: {hash_val: algo} or just a set of hashes if algo is fixed.
        """
        targets = set()
        count = 0
        try:
            with open(hash_file_path, 'r') as f:
                reader = csv.reader(f)
                next(reader, None) # Skip header
                for row in reader:
                    if len(row) >= 2:
                        # Assuming index 1 is hash. Adjust based on HashManager output.
                        # HashManager saves: [Plain, Hash, Algo]
                        h_val = row[1].strip()
                        targets.add(h_val)
                        count += 1
            return targets, count
        except Exception as e:
            raise e

    def attack(self, target_hashes, dictionary_path, algorithm, callback_status=None):
        self.running = True
        cracked = []
        attempts = 0
        
        try:
            with open(dictionary_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    if not self.running: break
                    
                    word = line.strip()
                    attempts += 1
                    
                    # Compute Hash
                    if algorithm == "MD5":
                        h = hashlib.md5(word.encode()).hexdigest()
                    elif algorithm == "SHA256":
                        h = hashlib.sha256(word.encode()).hexdigest()
                    elif algorithm == "SHA512":
                        h = hashlib.sha512(word.encode()).hexdigest()
                    else:
                        continue # Unknown algo
                    
                    # Check match
                    if h in target_hashes:
                        cracked.append((word, h))
                        # Optional: Remove from targets if you only expect unique hits?
                        # target_hashes.remove(h) 
                    
                    if attempts % 5000 == 0 and callback_status:
                        callback_status(attempts, len(cracked))
                        
            return cracked
        except Exception as e:
            raise e
        finally:
            self.running = False

    def stop(self):
        self.running = False
