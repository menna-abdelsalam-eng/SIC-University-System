class Authentication:

    def __init__(self, system):
        self.system = system

    # Authenticate a user and return the matching user object
    def login(self):
        while True:
            print("\nLogin as:\n"
                  "1. Student\n"
                  "2. Instructor\n"
                  "3. Admin\n"
                  "4. Back")
            choice = input("Choose:").strip()
            if choice == "1":
                users= self.system.students
                break
            elif choice == "2":
                users= self.system.instructors
                break
            elif choice == "3":
                users= self.system.admins
                break
            elif choice == "4":
                return None
            else:
                print("Invalid choice")
        email = input("Enter email:").strip()
        password = input("Enter password:")

        for user in users:
            if user.email == email and user.password == password:
                print("_"*20,"Login successful","_"*20)
                print()
                user.display_info()
                return user
        print("Invalid email or password")
        return None

    # Register a new Student or Instructor through the RegistrationSystem
    def register(self):
        while True:
            print("\nRegister as:\n"
                "1. Student\n"
                "2. Instructor\n"
                "3. Back")
            choice = input("Choose:").strip()
            if choice == "1":
                return self.system.register_student()
            elif choice == "2":
                return self.system.register_instructor()
            elif choice == "3":
                return None
            else:
                print("Invalid choice")

