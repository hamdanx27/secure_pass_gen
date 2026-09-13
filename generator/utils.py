import string
from random import SystemRandom

def generate_password(
    length: int = 16,
    include_upper: bool = True,
    include_lower: bool = True,
    include_numbers: bool = True,
    include_symbols: bool = True,
    exclude_ambiguous: bool = False
) -> str:
    """Generates a secure password using CSPRNG."""
    if not any([include_upper, include_lower, include_numbers, include_symbols]):
        raise ValueError("At least one character type must be selected.")
        
    if length < 4:
        raise ValueError("Password length must be at least 4 characters.")

    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    numbers = string.digits
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    if exclude_ambiguous:
        ambiguous = "il1Lo0O"
        upper = "".join(c for c in upper if c not in ambiguous)
        lower = "".join(c for c in lower if c not in ambiguous)
        numbers = "".join(c for c in numbers if c not in ambiguous)
        symbols = "".join(c for c in symbols if c not in ambiguous)

    pool = ""
    guaranteed_chars = []
    secure_rng = SystemRandom()

    # Ensure at least one character of each selected type is included
    if include_upper:
        pool += upper
        guaranteed_chars.append(secure_rng.choice(upper))
    if include_lower:
        pool += lower
        guaranteed_chars.append(secure_rng.choice(lower))
    if include_numbers:
        pool += numbers
        guaranteed_chars.append(secure_rng.choice(numbers))
    if include_symbols:
        pool += symbols
        guaranteed_chars.append(secure_rng.choice(symbols))

    remaining_length = length - len(guaranteed_chars)
    if remaining_length < 0:
         raise ValueError("Length is too short to include all selected character types.")

    # Fill the rest of the password
    random_chars = [secure_rng.choice(pool) for _ in range(remaining_length)]
    all_chars = guaranteed_chars + random_chars
    
    # Shuffle the characters securely so the guaranteed characters aren't always at the start
    secure_rng.shuffle(all_chars)
    
    return "".join(all_chars)