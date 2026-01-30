import os
import datetime
from modules.dictionary_attack import DictionaryAttacker
from modules.strength_analyzer import StrengthAnalyzer

class ReportGenerator:
    def __init__(self):
        self.attacker = DictionaryAttacker()
        self.analyzer = StrengthAnalyzer()

    def generate_security_audit(self, hash_file, dict_file, output_file="security_audit_report.txt"):
        """
        Generates a detailed security audit report compliant with professional standards.
        Includes: Executive Summary, Simulation Results, Weak Passwords, Policy Recommendations.
        """
        # 1. Gather Data / Run Simulation
        try:
            # Load Targets
            targets, total_hashes = self.attacker.load_targets(hash_file)
            
            # Run Dictionary Attack Simulation
            start_time = datetime.datetime.now()
            # Defaulting to SHA256 for the simulation audit
            cracked_list = self.attacker.attack(targets, dict_file, "SHA256") 
            duration = (datetime.datetime.now() - start_time).total_seconds()
            
            num_cracked = len(cracked_list)
            success_rate = (num_cracked / total_hashes * 100) if total_hashes > 0 else 0
            
        except Exception as e:
            return f"Error critical: {str(e)}", ""

        # 2. Analyze Findings
        weakness_types = {"Length < 8": 0, "No Numbers": 0, "No Symbols": 0, "Common Word": 0}
        
        for pwd, _ in cracked_list:
            if len(pwd) < 8: weakness_types["Length < 8"] += 1
            if not any(char.isdigit() for char in pwd): weakness_types["No Numbers"] += 1
            if not any(not char.isalnum() for char in pwd): weakness_types["No Symbols"] += 1
            weakness_types["Common Word"] += 1 # All dictionary hits are common words

        # 3. Construct Report
        lines = []
        
        # --- HEADER ---
        lines.append("=" * 60)
        lines.append(f"🔒 CYBERSECURITY AUDIT REPORT")
        lines.append("=" * 60)
        lines.append(f"Generated On   : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Target Database: {os.path.basename(hash_file)}")
        lines.append(f"Audit Source   : {os.path.basename(dict_file)}")
        lines.append("-" * 60)

        # --- EXECUTIVE SUMMARY ---
        lines.append("\n1. EXECUTIVE SUMMARY & RISK ASSESSMENT")
        lines.append("=" * 40)
        
        risk_level = "LOW"
        risk_desc = "Standard security posture."
        if success_rate > 5: 
            risk_level = "MEDIUM"
            risk_desc = "Notable vulnerabilities detected. Remediation required."
        if success_rate > 20: 
            risk_level = "HIGH"
            risk_desc = "Significant exposure. Immediate action recommended."
        if success_rate > 50: 
            risk_level = "CRITICAL"
            risk_desc = "Severe systemic failure. System is compromised."

        lines.append(f"Risk Level      : [{risk_level}]")
        lines.append(f"Total Accounts  : {total_hashes}")
        lines.append(f"Compromised     : {num_cracked}")
        lines.append(f"Vulnerability % : {success_rate:.1f}%")
        lines.append(f"Assessment      : {risk_desc}")

        # --- SIMULATION RESULTS ---
        lines.append("\n2. ATTACK SIMULATION METRICS")
        lines.append("=" * 40)
        lines.append(f"Attack Method   : Dictionary Attack (Wordlist Matching)")
        lines.append(f"Algorithm       : SHA256 (Simulated)")
        lines.append(f"Audit Duration  : {duration:.4f} seconds")
        lines.append(f"Note            : Represents vulnerability to basic offline attacks.")

        # --- WEAK PASSWORDS SUMMARY ---
        lines.append("\n3. WEAKNESS ANALYSIS")
        lines.append("=" * 40)
        lines.append("Breakdown of identified vulnerabilities:")
        for w_type, count in weakness_types.items():
            if count > 0:
                lines.append(f" - {w_type:<15} : {count} occurrences")

        if num_cracked > 0:
            lines.append("\n[Detailed Findings - Sample]")
            lines.append(f"{'Password':<20} | {'Strength Rating':<15} | {'Entropy'}")
            lines.append("-" * 55)
            # Show top 10 only to keep report clean
            for pwd, _ in cracked_list[:10]:
                stats = self.analyzer.evaluate_strength(pwd)
                lines.append(f"{pwd:<20} | {stats['rating']:<15} | {stats['entropy']}")
            
            if num_cracked > 10:
                lines.append(f"... and {num_cracked - 10} more.")

        # --- POLICY RECOMMENDATIONS ---
        lines.append("\n4. RECOMMENDED PASSWORD POLICIES")
        lines.append("=" * 40)
        
        if num_cracked == 0:
            lines.append("✅ No immediate weaknesses found in this dictionary audit.")
            lines.append("-> Continue enforcing current policies.")
            lines.append("-> Recommend quarterly audits with larger wordlists.")
        else:
            lines.append("⚠️ IMMEDIATE ACTIONS REQUIRED:")
            lines.append(f"   1. Force Password Reset: {num_cracked} accounts are using common passwords.")
            
            if weakness_types["Length < 8"] > 0:
                lines.append("   2. Update Policy: Enforce Minimum Length of 12 characters.")
            
            if weakness_types["No Symbols"] > 0:
                lines.append("   3. Complexity Requirement: Mandate at least 1 special character (!@#$).")
                
            if weakness_types["Common Word"] > 0:
                lines.append("   4. Blacklist: Disallow top 1000 common passwords (e.g., 'password', '123456').")
            
            lines.append("   5. Implementation: Enable Multi-Factor Authentication (MFA) on all accounts.")

        lines.append("\n" + "=" * 60)
        lines.append("END OF REPORT")
        lines.append("=" * 60)
        
        full_report = "\n".join(lines)
        with open(output_file, "w", encoding='utf-8') as f:
            f.write(full_report)
            
        return full_report, output_file
