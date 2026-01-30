import itertools
from datetime import datetime

class DictionaryGenerator:
    def __init__(self):
        # Expanded Leet Map
        self.leet_map = {
            'a': ['@', '4'], 'b': ['8'], 'e': ['3'], 'g': ['9', '6'], 
            'i': ['1', '!'], 'l': ['1', '7'], 'o': ['0'], 's': ['$', '5'], 
            't': ['7', '+'], 'z': ['2']
        }
        self.common_passwords = ["password", "admin", "root", "login", "welcome", "qwerty", "123456"]
        self.common_numbers = ["1", "123", "1234", "12345", "123456", "01", "10", "11", "69", "420", "007"]
        self.common_symbols = ["!", "@", "#", "$", "?", "*", ".", "_", "-"]
        
        # Dynamic Years: 5 years back, 2 years forward
        current_year = datetime.now().year
        self.common_years = [str(y) for y in range(current_year - 5, current_year + 3)]

    def generate_custom_list(self, base_inputs, include_dob=False, dob_year="", use_leet=False, use_case=False, use_nums=False, use_symbols=False):
        # Initialize
        seeds = set([w.strip() for w in base_inputs if w.strip()])
        if not seeds:
            return []
            
        final_wordlist = set(seeds)

        # 1. Date Mutations (High Priority)
        # Add years to seeds immediately if relevant (e.g. "john2024")
        if include_dob and dob_year:
            date_variations = self._generate_date_variations(seeds, dob_year)
            final_wordlist.update(date_variations)
            # Add date-appended words to seeds so they get case/leet mutations too
            seeds.update(date_variations)

        # 2. Case Mutations
        if use_case:
            cased = self._mutate_case(final_wordlist)
            final_wordlist.update(cased)
        
        # 3. Leet Mutations
        if use_leet:
            leeted = self._mutate_leet(final_wordlist)
            final_wordlist.update(leeted)

        # 4. Hybrid Combinations (Word + Word)
        # Use a smaller subset for hybrid to avoid explosion
        # We perform this BEFORE affixes to keep the base manageable
        hybrid_seeds = set(itertools.islice(final_wordlist, 100)) # Limit to top 100
        hybrid = self._mutate_hybrid(hybrid_seeds)
        final_wordlist.update(hybrid)
        
        # 5. Affixes (Numbers & Symbols)
        # This is where we do "word + 123" or "word + !"
        # We apply this to ALL words generated so far (careful with size)
        
        # Filter for affixing: Don't affix everything if list is huge
        targets_for_affix = list(final_wordlist)
        if len(targets_for_affix) > 2000:
             targets_for_affix = targets_for_affix[:2000] # Cap for performance
        
        affixed = set()
        
        numbers_to_use = []
        if use_nums:
            numbers_to_use = self.common_numbers + self.common_years
            # Add small range 0-21
            numbers_to_use.extend([str(i) for i in range(22)])
            
        symbols_to_use = []
        if use_symbols:
            symbols_to_use = self.common_symbols
            
        # Apply Logic:
        # P1: Word + Num
        # P2: Word + Sym
        # P3: Word + Sym + Num (Strong)
        # P4: Num + Word
        
        for w in targets_for_affix:
            # Num Suffix/Prefix
            for n in numbers_to_use:
                affixed.add(f"{w}{n}")
                affixed.add(f"{n}{w}")
            
            # Sym Suffix/Prefix
            for s in symbols_to_use:
                affixed.add(f"{w}{s}")
                affixed.add(f"{s}{w}")
                
            # Complex: Word + Sym + Num
            if use_nums and use_symbols:
                for s in symbols_to_use:
                    for n in numbers_to_use[:15]: # Limit combo to top 15 numbers (common ones)
                        affixed.add(f"{w}{s}{n}") # pattern!1
                        affixed.add(f"{w}{n}{s}") # pattern1!

        final_wordlist.update(affixed)
        
        return sorted(list(final_wordlist))

    def _mutate_case(self, words):
        res = set()
        for w in words:
            res.add(w.lower())
            res.add(w.upper())
            res.add(w.capitalize())
            res.add(w.title())
            # Inversion case: "aDMIN"
            if len(w) > 1:
                res.add(w[0].lower() + w[1:].upper())
        return res

    def _mutate_leet(self, words):
        res = set()
        for w in words:
            # Simple single-pass leet
            # 1. All chars replaced
            w_all = ""
            for c in w:
                w_all += self.leet_map.get(c.lower(), [c])[0]
            res.add(w_all)
            
            # 2. Partial replacement (common vowels)
            w_part = ""
            for c in w:
                if c.lower() in ['a', 'e', 'i', 'o']:
                    w_part += self.leet_map.get(c.lower(), [c])[0]
                else:
                    w_part += c
            res.add(w_part)
        return res

    def _generate_date_variations(self, seeds, year):
        res = set()
        # Formats: YYYY, YY
        y_variants = {year, year[-2:]}
        for w in seeds:
            for y in y_variants:
                res.add(f"{w}{y}") # name1990
                res.add(f"{y}{w}") # 1990name
                res.add(f"{w}_{y}") # name_1990
                res.add(f"{w}@{y}") # name@1990
        return res

    def _mutate_hybrid(self, seeds):
        res = set()
        separators = ["", ".", "_", "-", "@"]
        # Limit seeds
        seeds_list = list(seeds)
        # Avoid huge loops: Only combine if list is small, otherwise sample
        if len(seeds_list) > 20:
             seeds_list = seeds_list[:20]

        for i, w1 in enumerate(seeds_list):
            for w2 in seeds_list:
                if w1 == w2: continue
                for sep in separators:
                    res.add(f"{w1}{sep}{w2}")
        return res

    def save_to_file(self, word_list, filename="dictionary.txt"):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for word in word_list:
                    f.write(word + "\n")
            return len(word_list), filename
        except Exception as e:
            raise e
