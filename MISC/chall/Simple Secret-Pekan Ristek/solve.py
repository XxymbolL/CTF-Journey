import builtins
import keyword
import string

# List of banned words (excluding 'flag')
banned_words = [
    'dir', 'globals', 'locals', 'eval', 'exec', 'breakpoint', 'vars', 'getattr', 
    'class', 'mro', 'os', 'popen', 'system',
]

# Display allowed globals
print("\n========= Allowed globals =========")
for w in list(globals()):
    if w.isascii() and not any(word in w for word in banned_words):
        print(w)

# Display allowed builtins
print("\n========= Allowed builtins =========")
for w in list(builtins.__dict__):
    if w.isascii() and not any(word in w for word in banned_words):
        print(w)

# Display allowed keywords
print("\n========= Allowed keywords =========")
for w in list(keyword.kwlist):
    if w.isascii() and not any(word in w for word in banned_words):
        print(w)

# Display allowed special characters
print("\n========= Allowed special chars =========")
for w in string.punctuation:
    if w.isascii():  # Only check ASCII punctuation
        print(w)


