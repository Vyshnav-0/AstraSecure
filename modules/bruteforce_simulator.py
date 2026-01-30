import hashlib
import itertools
import string
import time
import threading

class BruteForceSimulator:
    def __init__(self):
        self.running = False
        self.found = False
        
    def get_charset(self, use_lower=True, use_upper=False, use_nums=False, use_syms=False):
        charset = ""
        if use_lower: charset += string.ascii_lowercase
        if use_upper: charset += string.ascii_uppercase
        if use_nums:  charset += string.digits
        if use_syms:  charset += string.punctuation
        return charset

    def hash_attempt(self, attempt, algo):
        if algo == "MD5":
            return hashlib.md5(attempt.encode()).hexdigest()
        elif algo == "SHA256":
            return hashlib.sha256(attempt.encode()).hexdigest()
        elif algo == "SHA512":
            return hashlib.sha512(attempt.encode()).hexdigest()
        return None

    def attack(self, target_hash, algorithm, charset, max_length, callback_status=None, callback_success=None):
        self.running = True
        self.found = False
        start_time = time.time()
        attempts = 0
        
        try:
            for length in range(1, max_length + 1):
                if not self.running: break
                
                # itertools.product generates all cartesian products of input iterable
                # repeat=length means length of the generated tuple
                for guess_tuple in itertools.product(charset, repeat=length):
                    if not self.running: break
                    
                    guess = "".join(guess_tuple)
                    attempts += 1
                    
                    # Check hash
                    guess_hash = self.hash_attempt(guess, algorithm)
                    
                    if guess_hash == target_hash:
                        self.found = True
                        self.running = False
                        end_time = time.time()
                        if callback_success:
                            callback_success(guess, attempts, end_time - start_time)
                        return
                    
                    # Update status every 1000 attempts to avoid UI lag
                    if attempts % 2000 == 0:
                        if callback_status:
                            elapsed = time.time() - start_time
                            # Avoid div by zero
                            speed = attempts / elapsed if elapsed > 0 else 0
                            callback_status(guess, attempts, speed)

            if not self.found and self.running:
                # Finished loops without finding
                end_time = time.time()
                if callback_success: # Sending None indicates failure to find
                    callback_success(None, attempts, end_time - start_time)

        except Exception as e:
            print(f"Error in brute force: {e}")
            self.running = False

    def stop(self):
        self.running = False
