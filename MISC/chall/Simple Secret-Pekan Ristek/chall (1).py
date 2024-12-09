import secret

def challenge():
    print("Welcome to Pekan RISTEK NetSOS 2024")
    print("This is a simple python challenge (pyjail maybe?)")
    print("Good luck!")
    
    is_this_even_needed = [
        'dir',
        'globals',
        'locals',
        'eval',
        'exec',
        'breakpoint',
        'vars',
        'getattr',
        'class',
        'mro',
        'os',
        'popen',
        'system',
    ]

    while True:
        user_input = input("Enter variable name: ").strip()
        
        if any(word in user_input for word in is_this_even_needed) or not user_input.isascii():
            print("NT! Sadly that won't work hehe")
            continue
        
        try:
            exec(f"print(secret.{user_input})")
        except:
            print("Error or variable not found")

if __name__ == '__main__':
    challenge()