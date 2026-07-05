def check_first_matching_type(password):
    for char in password:
        # Match the character 'char' against different conditions
        match char:
            # 'c' binds to the character, and the 'if' acts as a guard
            case c if c.isdigit():
                return "Contains a number"

            case c if c.isupper():
                return "Contains an uppercase letter"

            case c if c.islower():
                return "Contains a lowercase letter"

            # You can also check against specific groups of characters
            case c if c in "!@#$%^&*":
                return "Contains a special symbol"

            # Catch-all for spaces, other symbols, etc.
            case _:
                continue
                
    return "Nothing special found"

# --- Testing it out ---
print(check_first_matching_type("hello"))  # Output: Contains a lowercase letter
print(check_first_matching_type("HELLO"))  # Output: Contains an uppercase letter
print(check_first_matching_type("12345"))  # Output: Contains a number
print(check_first_matching_type("!@#$"))   # Output: Contains a special symbol