from person import Person

class Admin(Person):
    def __init__(self,id,name,email,password,dept="Administrator"):
        super().__init__(id,name,email,password,dept)

    def get_role(self):
        return "Admin"

    def display_info(self):
        print("_"*50,"Admin Information","_"*50)
        print(f"Name: {self.name}\nEmail: {self.email}\nDepartment: {self.dept}")



