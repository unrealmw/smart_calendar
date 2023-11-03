import re
import datetime as dt


class Calendar:
    notes = []
    birthdays = dict()
    cached_notes = []
    cached_birthdays = dict()

    @staticmethod
    def show_now():
        print("Current date and time:", dt.datetime.now(), sep="\n")

    def add_notes(self):
        notes_num = int(input("How many notes do you want to add?\n"))
        for i in range(1, notes_num + 1):
            print(f"Enter date and time of note #{i} (in format «YYYY-MM-DD HH:MM»):")
            while True:
                date_time = input()
                if self.date_check(date_time):
                    break
            text = input(f"Enter text of note #{i}:\n")
            self.notes.append([text, date_time.split()])
        print("Notes added!")

    def del_notes(self):
        for note in self.cached_notes:
            choice = input(f"Are you sure you want to delete \"{note[0]}\"?")
            match choice:
                case "yes":
                    self.cached_notes.remove(note)
                    print("Note deleted!")
                case "no":
                    print("Deletion canceled.")

    def add_birthdays(self):
        bd_num = int(input("How many dates of birth do you want to add?\n"))
        for i in range(1, bd_num + 1):
            name = input(f"Enter the name of #{i}:\n")
            date = input(f"Enter the date of birth of #{i} (in format «YYYY-MM-DD»):\n")
            self.birthdays.update({name: date})
        print("Birthdates added!")

    def del_birthdays(self):
        for name in self.cached_birthdays.keys():
            choice = input(f"Are you sure you want to delete \"{name}\"?")
            match choice:
                case "yes":
                    self.birthdays.pop(name)
                    print("Birthdate deleted!")
                case "no":
                    print("Deletion canceled.")

    @staticmethod
    def date_check(date):
        full_match = re.match(r"\d{4}-\d{2}-\d{2}\s{1}\d{2}:\d{2}", date)
        if not full_match:
            print("Incorrect format. Please try again (use the format «YYYY-MM-DD HH:MM»)")
            return False
        else:
            dt_lst = re.split(r"\W+", date)
            if not re.match(r"0[1-9]|1[0-2]", dt_lst[1]):
                print("Incorrect month value. The month should be in 01-12.")
                return False
            if not re.match(r"[01][0-9]|2[0-3]", dt_lst[3]):
                print("Incorrect hour value. The hour should be in 00-23.")
                return False
            if not re.match(r"[0-5][0-9]", dt_lst[-1]):
                print("Incorrect minute value. The minutes should be in 00-59.")
                return False
        return True

    def save_notes(self):
        with open("notes.txt", "w", encoding="utf-8") as file:
            for note in self.notes:
                file.write(f"{note[0]}: {' '.join(note[1])}\n")
            file.write("\n")
            for name, date in self.birthdays.items():
                file.write(f"{name}: {date}\n")

    def take_notes(self):
        with open("notes.txt", "r", encoding="utf-8") as file:
            for line in file:
                if not line.strip():
                    break
                else:
                    text, date_time = line.strip().split(": ")
                    self.notes.append([text, date_time.split()])
            for line in file:
                name, birthdate = line.strip().split(": ")
                self.birthdays.update({name: birthdate})

    def time_remain(self):
        print()
        for note in self.cached_notes:
            td = dt.datetime.strptime(" ".join(note[1]), '%Y-%m-%d %H:%M') - dt.datetime.now()
            days, hours, minutes = td.days, td.seconds // 3600, td.seconds // 60 % 60
            print(f"Before the event note \"{note[0]}\" remains:",
                  f"{days} day(s), {hours} hour(s) and {minutes} minute(s).", sep="\n")

    def time_to_birthday(self):
        print()
        for name, bd_date in self.cached_birthdays.items():
            birth_date = dt.datetime.strptime(bd_date, '%Y-%m-%d')
            today = dt.date.today()
            this_year_bd = dt.date(today.year, birth_date.month, birth_date.day)
            if this_year_bd < today:
                next_year_bd = dt.date(today.year + 1, birth_date.month, birth_date.day)
                days_left = (next_year_bd - today).days
                age = next_year_bd.year - birth_date.year
                print(f"{name}’s birthday is in {days_left} days. He (she) turns {age} years old.")
            elif this_year_bd > today:
                days_left = (this_year_bd - today).days
                age = today.year - birth_date.year
                print(f"{name}’s birthday is in {days_left} days. He (she) turns {age} years old.")
            else:
                age = today.year - birth_date.year
                print(f"{name}’s birthday is today. He (she) turns {age} years old.")

    def view_by_date(self):
        date = input("Enter date (in format «YYYY-MM-DD»):")
        for note in self.notes:
            if date == note[1][0]:
                self.cached_notes.append(self.notes.pop(self.notes.index(note)))
        month_date = "-".join(date.split("-")[1:])
        for key, value in self.birthdays.items():
            if re.search(month_date, value):
                self.cached_birthdays.update({key: value})
        print(f"Found {len(self.cached_notes)} note(s) and {len(self.cached_birthdays)} date(s) of birth on this date:")
        self.time_remain()
        self.time_to_birthday()

    def view_by_name(self):
        print("Enter name:")
        while True:
            name = input()
            if name in self.birthdays.keys():
                self.cached_birthdays.update({name: self.birthdays[name]})
                break
            else:
                print("No such person found. Try again:")
                continue
        print(f"Found {len(self.cached_birthdays)} date of birth:")
        self.time_to_birthday()

    def view_by_note(self):
        print("Enter text of note:")
        print(self.notes)
        while True:
            name = input()
            for note in self.notes:
                if re.search(name, note[0], flags=re.IGNORECASE):
                    self.cached_notes.append(self.notes.pop(self.notes.index(note)))
            if len(self.cached_notes) == 0:
                print("No such note found. Try again:")
                continue
            else:
                break
        print(f"Found {len(self.cached_notes)} note(s) that contain \"{name}\":")
        self.time_remain()

    def save_from_caches(self):
        for note in self.cached_notes:
            self.notes.append(note)
        self.cached_notes.clear()
        self.cached_birthdays.clear()

    def view_or_del(self, command="view"):
        view_command = input(f"What do you want to {command} (date, note, name)?")
        match view_command:
            case "date":
                self.view_by_date()
            case "name":
                self.view_by_name()
            case "note":
                self.view_by_note()
        match command:
            case "delete":
                self.del_notes()
                self.del_birthdays()
        self.save_from_caches()

    def add_menu(self):
        add_command = input("What do you want to add (note, birthday)?\n")
        match add_command:
            case "note":
                self.add_notes()
            case "birthday":
                self.add_birthdays()

    def main_menu(self):
        while True:
            command = input("Enter the command (add, view, delete, exit)")
            match command:
                case "add":
                    self.add_menu()
                case "view":
                    print(self.notes)
                    print(self.birthdays)
                    self.view_or_del(command="view")
                case "delete":
                    self.view_or_del(command="delete")
                case "exit":
                    break


if __name__ == '__main__':
    a = Calendar()
    a.show_now()
    a.take_notes()
    a.main_menu()
    a.save_notes()
