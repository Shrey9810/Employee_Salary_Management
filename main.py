import pandas as pd
import re
import time

class Employee:
    def __init__(self, name, emp_id, address, mail, mobile_no):
        mobile_no = str(mobile_no)
        
        if not self.validate_email(mail):
            raise ValueError(f"Invalid email address: {mail}")
        if not self.validate_mobile(mobile_no):
            raise ValueError(f"Invalid mobile number: {mobile_no}")

        self.emp_name = name
        self.emp_id = emp_id
        self.address = address
        self.mail_id = mail
        self.mobile_no = mobile_no

    def calculate_salary(self, BP):
        try:
            if BP <= 0:
                raise ValueError("Basic Pay (BP) must be a positive number.")

            DA = 0.97 * BP
            HRA = 0.1 * BP
            PF = 0.12 * BP
            staff_club_fund = 0.001 * BP

            gross_salary = BP + DA + HRA
            net_salary = gross_salary - (PF + staff_club_fund)

            return net_salary
        except Exception as e:
            print(f"Error calculating salary for {self.emp_name}: {e}")
            return None

    @staticmethod
    def validate_email(email):
        pattern = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_mobile(mobile):
        pattern = r'^\d{10}$'
        return re.match(pattern, mobile) is not None

class Programmer(Employee):
    def __init__(self, name, emp_id, address, mail, mobile_no):
        super().__init__(name, emp_id, address, mail, mobile_no)
        self.BP = 100000

    def display_salary(self):
        return self.calculate_salary(self.BP)

class Professor(Employee):
    def __init__(self, name, emp_id, address, mail, mobile_no):
        super().__init__(name, emp_id, address, mail, mobile_no)
        self.BP = 150000

    def display_salary(self):
        return self.calculate_salary(self.BP)

class AssistantProfessor(Employee):
    def __init__(self, name, emp_id, address, mail, mobile_no):
        super().__init__(name, emp_id, address, mail, mobile_no)
        self.BP = 130000

    def display_salary(self):
        return self.calculate_salary(self.BP)

class AssociateProfessor(Employee):
    def __init__(self,name, emp_id, address, mail, mobile_no):
        super().__init__(name, emp_id, address, mail, mobile_no)
        self.BP = 140000

    def display_salary(self):
        return self.calculate_salary(self.BP)

def create_employee_from_data(data):
    name, emp_id, address, mail, mobile_no, role = data
    role_map = {
        "Programmer": Programmer,
        "Professor": Professor,
        "AssistantProfessor": AssistantProfessor,
        "AssociateProfessor": AssociateProfessor
    }
    if role not in role_map:
        raise ValueError(f"Unknown role: {role}")
    return role_map[role](name, emp_id, address, mail, str(mobile_no))  

if __name__ == "__main__":
    
    start_time = time.time()
    
    df = pd.read_excel('employees.xlsx')

    df['Salary'] = None

    for index, row in df.iterrows():
        data = [
            row['Name'], row['Emp ID'], row['Address'], 
            row['Email'], row['Mobile No'], row['Role']
        ]
        try:
            employee = create_employee_from_data(data)
            salary = employee.display_salary()
            df.at[index, 'Salary'] = salary
        except ValueError as e:
            print(f"Error: {e}")

    df.to_excel('employees.xlsx', index=False)
    end_time = time.time()
    time_taken = end_time - start_time
    print("Salary Calculated.")
    print(f"Time taken : {time_taken:.4f} seconds")