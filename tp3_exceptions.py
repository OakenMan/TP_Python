# Exemple basique pour lever une exception avec assert et raise
def division(a, b):
    try:
        assert(b != 0)
    except:
        raise ZeroDivisionError
    else:
        return a / b

print(division(4, 2))
print(division(2, 0))

