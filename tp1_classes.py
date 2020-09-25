class Date:

    # Constructeur
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year

    # Surcharge de l'opérateur ==
    def __eq__(self, other):
        return self.day == other.day and self.month == other.month and self.year == other.year

    # Surchage de l'opérateur <
    def __lt__(self, other):
        if self.year < other.year:
            return True
        elif self.year == other.year and self.month < other.month:
            return True
        elif self.year == other.year and self.month == other.month and self.day < other.day:
            return True
        else:
            return False

    # Surcharge de l'opérateur "str()"
    def __str__(self):
        return str(self.day) + "/" + str(self.month) + "/" + str(self.year)


date1 = Date(15, 9, 2020)
date2 = Date(15, 9, 2020)
date3 = Date(20, 10, 2020)

print(date1 == date2)
print(date3 < date2)
print(date1)


# Renvoie une adresse mail à partir du nom et du prénom
def makemail(firstname, lastname):
    return firstname.lower() + "." + lastname.lower() + "@etu.univ-tours.fr"


class Student:

    # Constructeur
    def __init__(self, firstname, lastname, birth):
        self.firstname = firstname
        self.lastname = lastname
        self.birth = birth
        self.mail = makemail(firstname, lastname)

    # Surcharge de l'opérateur "str()"
    def __str__(self):
        return self.firstname + " " + self.lastname + " - " + str(self.birth) + self.mail


students = []

try:
    file = open("/home/tom/Téléchargements/Python/fichetu.csv", "r")
except:
    print("Erreur : le fichier n'existe pas")
    exit()

lines = file.readlines()
for line in lines:
    array = line.split(';')
    date = array[2].split('/')
    student = Student(array[0], array[1], Date(date[0], date[1], date[2]))
    students.append(student)

print("List of students :")
for student in students:
    print(student)
