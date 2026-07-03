import secrets

UPPERCASE_CHARS = "ABCDEFGHJKLMNOPQRSTUVWXYZ"  # Safe default sets
LOWERCASE_CHARS = "abcdefghijkmnopqrstuvwxyz"
NUMBER_CHARS = "23456789"
SYMBOL_CHARS = "!@#$%^&*()_+-=[]{}|;:,.<>?"

# Strict Ambiguous lists
AMBIGUOUS_CHARS = "O0I1l"

def generate_secure_passwords(
    length: int,
    use_upper: bool,
    use_lower: bool,
    use_numbers: bool,
    use_symbols: bool,
    exclude_ambiguous: bool,
    quantity: int = 1
) -> list[str]:
    """Generates cryptographically high-entropy passwords with absolute structural rules."""
    
    # Input Validation bounds
    if not (4 <= length <= 128):
        raise ValueError("Password length must be between 4 and 128 characters.")
    if not (1 <= quantity <= 20):
        raise ValueError("Quantity must be between 1 and 20.")
        
    # Pool formulation
    upper_pool = UPPERCASE_CHARS + ("O" if not exclude_ambiguous else "")
    lower_pool = LOWERCASE_CHARS + ("l" if not exclude_ambiguous else "")
    number_pool = NUMBER_CHARS + ("0" if not exclude_ambiguous else "")
    symbol_pool = SYMBOL_CHARS
    
    if not exclude_ambiguous:
        upper_pool += "I"
        lower_pool += "i"
        number_pool += "1"
        
    pools = []
    if use_upper: pools.append(upper_pool)
    if use_lower: pools.append(lower_pool)
    if use_numbers: pools.append(number_pool)
    if use_symbols: pools.append(symbol_pool)
    
    if not pools:
        raise ValueError("At least one character type must be selected.")
        
    if length < len(pools):
        raise ValueError(f"Length is too short! Minimum requirement is {len(pools)} characters based on chosen pools.")

    generated_passwords = []
    
    for _ in range(quantity):
        password_chars = []
        
        # Rule Guarantee: Force one character from each active pool selection
        for pool in pools:
            password_chars.append(secrets.choice(pool))
            
        # Combine all selections into one target array
        full_pool = "".join(pools)
        
        # Fill out remaining allocation length bounds
        while len(password_chars) < length:
            password_chars.append(secrets.choice(full_pool))
            
        # High security Fisher-Yates shuffle implementation mapping via secrets
        for i in range(len(password_chars) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            password_chars[i], password_chars[j] = password_chars[j], password_chars[i]
            
        generated_passwords.append("".join(password_chars))
        
    return generated_passwords
