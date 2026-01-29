from Doctor import Doctor
from Patient import Patient
import os

class Admin:
    """A class that deals with the Admin operations"""
    def __init__(self, username, password, address=''):
        """
        Args:
            username (string): Username
            password (string): Password
            address (string, optional): Address Defaults to ''
        """

        self.__username = username
        self.__password = password
        self.__address = address
        self.__doctors_file = 'doctors.txt'
        self.__patients_file = 'patients.txt'
        self.__admin_file = 'admin.txt'
        self.__discharged_file = 'discharged_patients.txt'
        self.__appointments_file = 'appointments.txt'

    def save_admin_to_file(self):
        try:
            with open(self.__admin_file, 'w') as f:
                f.write(f"username: {self.__username}\n")
                f.write(f"password: {self.__password}\n")
                f.write(f"address: {self.__address}\n")
        except Exception:
            pass

    def load_admin_from_file(self):
        if not os.path.exists(self.__admin_file):
            return

        try:
            with open(self.__admin_file, 'r') as f:
                content = [line.strip() for line in f if line.strip()]

            if not content:
                return

            if len(content) == 1 and ',' in content[0]:
                parts = content[0].split(',')
                if len(parts) >= 2:
                    self.__username = parts[0].strip()
                    self.__password = parts[1].strip()
                    if len(parts) > 2:
                        self.__address = parts[2].strip()
                return
            data = {}
            for line in content:
                if ':' in line:
                    key, val = line.split(':', 1)
                    data[key.strip().lower()] = val.strip()

            if 'username' in data:
                self.__username = data['username']
            if 'password' in data:
                self.__password = data['password']
            if 'address' in data:
                self.__address = data['address']
        except Exception:
            pass

    def authenticate(self, username, password):
        try:
            return username == self.__username and password == self.__password
        except Exception:
            return False

    def view(self, a_list):
        """
        print a list
        Args:
            a_list (list): a list of printables
        """
        for index, item in enumerate(a_list):
            print(f'{index+1:3}|{item}')

    def login(self):
        """
        A method that deals with the login
        Raises:
            Exception: returned when the username and the password ...
                    ... don`t match the data registered
        Returns:
            string: the username
        """
        print("-----Login-----")
        #Get the details of the admin

        username = input('Enter the username: ')
        password = input('Enter the password: ')

        # check if the username and password match the registered ones
        #ToDo1

        if username == self.__username and password == self.__password:
            return self.__username
        else:
            raise Exception("Invalid username or password")

    def find_index(self, index, doctors):
        if index in range(0, len(doctors)):

            return True
        
        # if the id is not in the list of doctors
        else:
            return False

    def get_doctor_details(self):
        """
       Get the details needed to add a doctor
        Returns:
            first name, surname and ...
                            ... the speciality of the doctor in that order.
        """
        #ToDo2

        print('Enter the doctor\'s details:')
        first_name = input('Enter the first name: ')
        surname = input('Enter the surname: ')
        speciality = input('Enter the speciality: ')
        return first_name, surname, speciality

    def save_doctors_to_file(self, doctors):
        with open(self.__doctors_file, 'w') as f:
            for doctor in doctors:
                f.write(f"{doctor.get_first_name()},{doctor.get_surname()},{doctor.get_speciality()}\n")

    def load_doctors_from_file(self):
        doctors = []
        if os.path.exists(self.__doctors_file):
            with open(self.__doctors_file, 'r') as f:
                for line in f:
                    data = line.strip().split(',')
                    if len(data) == 3:
                        doctors.append(Doctor(data[0], data[1], data[2]))
        return doctors

    def save_patients_to_file(self, patients):
        with open(self.__patients_file, 'w') as f:
            for patient in patients:
                symptoms_str = ';'.join(patient.get_symptoms()) if patient.get_symptoms() else ''
                f.write(f"{patient.get_first_name()},{patient.get_surname()},{patient.get_age()},{patient.get_mobile()},{patient.get_postcode()},{patient.get_doctor()},{symptoms_str}\n")

    def load_patients_from_file(self):
        patients = []
        if os.path.exists(self.__patients_file):
            with open(self.__patients_file, 'r') as f:
                for line in f:
                    data = line.strip().split(',')
                    if len(data) >= 6:
                        symptoms = data[6].split(';') if len(data) > 6 and data[6] else []
                        patient = Patient(data[0], data[1], int(data[2]), data[3], data[4], symptoms)
                        patient.link(data[5])
                        patients.append(patient)
        return patients

    def save_discharged_to_file(self, discharged_patients):
        with open(self.__discharged_file, 'w') as f:
            for patient in discharged_patients:
                symptoms_str = ';'.join(patient.get_symptoms()) if patient.get_symptoms() else ''
                f.write(f"{patient.get_first_name()},{patient.get_surname()},{patient.get_age()},{patient.get_mobile()},{patient.get_postcode()},{patient.get_doctor()},{symptoms_str}\n")

    def load_discharged_from_file(self):
        discharged = []
        if os.path.exists(self.__discharged_file):
            with open(self.__discharged_file, 'r') as f:
                for line in f:
                    data = line.strip().split(',')
                    if len(data) >= 6:
                        symptoms = data[6].split(';') if len(data) > 6 and data[6] else []
                        patient = Patient(data[0], data[1], int(data[2]), data[3], data[4], symptoms)
                        patient.link(data[5])
                        discharged.append(patient)
        return discharged

    def doctor_management(self, doctors):
        """
        A method that deals with registering, viewing, updating, deleting doctors
        Args:
            doctors (list<Doctor>): the list of all the doctors names
        """
        print("-----Doctor Management-----")

        # menu
        print('Choose the operation:')
        print(' 1 - Register')
        print(' 2 - View')
        print(' 3 - Update')
        print(' 4 - Delete')
        print(' 5 - Print All Doctors')
        print(' 6 - Save to File')
        print(' 7 - Load from File')

        #ToDo3

        op = input('Input: ')

        # register
        if op == '1':
            print("-----Register-----")

            # get the doctor details
            #ToDo4
            first_name, surname, speciality = self.get_doctor_details()
            # check if the name is already registered
            name_exists = False
            for doctor in doctors:
                if first_name == doctor.get_first_name() and surname == doctor.get_surname():
                    print('Name already exists.')
                    #ToDo5
                    # save time and end the loop
                    name_exists = True
                    break
            #ToDo6
            # add the doctor ...
            # ... to the list of doctors
            if not name_exists:
                new_doctor = Doctor(first_name, surname, speciality)
                doctors.append(new_doctor)
                self.save_doctors_to_file(doctors)
                print('Doctor registered.')

        # View
        elif op == '2':
            print("-----List of Doctors-----")
            #ToDo7
            self.view(doctors)

        # Update
        elif op == '3':
            while True:
                print("-----Update Doctor`s Details-----")
                print('ID |          Full name           |  Speciality')
                self.view(doctors)
                try:
                    index = int(input('Enter the ID of the doctor: ')) - 1
                    if self.find_index(index, doctors):
                        break
                    else:
                        print("Doctor not found")
                        # doctor_index is the ID mines one (-1)
                except ValueError:# the entered id could not be changed into an int
                    print('The ID entered is incorrect')

            print('Choose the field to be updated:')
            print(' 1 First name')
            print(' 2 Surname')
            print(' 3 Speciality')

            while True:
                try:
                    op = int(input('Input: '))# make the user input lowercase
                    #ToDo8
                    break
                except ValueError:
                    print('Invalid input. Please enter 1, 2, or 3.')

            doctor = doctors[index]
            if op == 1:
                new_first_name = input('Enter the new first name: ')
                doctor.set_first_name(new_first_name)
                print('First name updated.')
            elif op == 2:
                new_surname = input('Enter the new surname: ')
                doctor.set_surname(new_surname)
                print('Surname updated.')
            elif op == 3:
                new_speciality = input('Enter the new speciality: ')
                doctor.set_speciality(new_speciality)
                print('Speciality updated.')
            else:
                print('Invalid option.')
            
            self.save_doctors_to_file(doctors)
        # Delete
        elif op == '4':
            print("-----Delete Doctor-----")
            print('ID |          Full Name           |  Speciality')
            self.view(doctors)
            doctor_index = input('Enter the ID of the doctor to be deleted: ')
            #ToDo9
            try:
                doctor_index = int(doctor_index) - 1
                if self.find_index(doctor_index, doctors):
                    removed_doctor = doctors.pop(doctor_index)
                    self.save_doctors_to_file(doctors)
                    print(f'Doctor {removed_doctor.full_name()} deleted.')
                else:
                    print('The id entered was not found.')
            except ValueError:
                print('The id entered is incorrect')
                # if the id is not in the list of patients

        elif op == '5':
            print("-----All Doctors-----")
            print('ID |          Full Name           |  Speciality')
            self.view(doctors)

        elif op == '6':
            self.save_doctors_to_file(doctors)
            print('Doctors saved to file.')

        elif op == '7':
            doctors.clear()
            doctors.extend(self.load_doctors_from_file())
            print('Doctors loaded from file.')

        else:
            print('Invalid operation chosen.')

    def view_patient(self, patients):
        """
        print a list of patients
        Args:
            patients (list<Patients>): list of all the active patients
        """
        print("-----View Patients-----")
        print('ID |          Full Name           |      Doctor`s Full Name      | Age |    Mobile     | Postcode ')
        #ToDo10
        self.view(patients)

    def assign_doctor_to_patient(self, patients, doctors):
        print("-----Assign-----")
        print("-----Patients-----")
        print('ID |          Full Name           |      Doctor`s Full Name      | Age |    Mobile     | Postcode ')
        self.view(patients)

        patient_index = input('Please enter the patient ID: ')
        try:
            # patient_index is the patient ID mines one (-1)
            patient_index = int(patient_index) - 1

            # check if the id is not in the list of patients
            if patient_index not in range(len(patients)):
                print('The id entered was not found.')
                return # stop the procedures
        except ValueError:# the entered id could not be changed into an int
            print('The id entered is incorrect')
            return

        print("-----Doctors Select-----")
        print('Select the doctor that fits these symptoms:')
        patients[patient_index].print_symptoms()# print the patient symptoms
        print('--------------------------------------------------')
        print('ID |          Full Name           |  Speciality   ')
        self.view(doctors)
        doctor_index = input('Please enter the doctor ID: ')

        try:
            # doctor_index is the patient ID mines one (-1)
            doctor_index = int(doctor_index) - 1

            # check if the id is in the list of doctors
            if self.find_index(doctor_index, doctors):
                # link the patients to the doctor and vice versa
                #ToDo11
                patient = patients[patient_index]
                old_doctor = patient.get_doctor()
                
                if old_doctor != 'None':
                    for doctor in doctors:
                        if doctor.full_name() == old_doctor:
                            doctor.remove_patient(patient)
                
                patient.link(doctors[doctor_index].full_name())
                doctors[doctor_index].add_patient(patient)
                self.save_patients_to_file(patients)
                print('The patient is now assigned to the doctor.')
                # if the id is not in the list of doctors
            else:
                print('The id entered was not found.')
        except ValueError: # the entered id could not be changed into an in
            print('The id entered is incorrect')

    def discharge(self, patients, discharge_patients):
        """
        Allow the admin to discharge a patient when treatment is done
        Args:
            patients (list<Patients>): the list of all the active patients
            discharge_patients (list<Patients>): the list of all the non-active patients
        """
        print("-----Discharge Patient-----")
        patient_index = input('Please enter the patient ID: ')
        #ToDo12
        try:
            patient_index = int(patient_index) - 1
            if patient_index in range(len(patients)):
                discharged_patient = patients.pop(patient_index)
                discharge_patients.append(discharged_patient)
                self.save_patients_to_file(patients)
                self.save_discharged_to_file(discharge_patients)
                print(f'Patient {discharged_patient.full_name()} has been discharged.')
            else:
                print('The id entered was not found.')
        except ValueError:
            print('The id entered is incorrect')

    def view_discharge(self, discharged_patients):
        """
        Prints the list of all discharged patients
        Args:
            discharge_patients (list<Patients>): the list of all the non-active patients
        """
        print("-----Discharged Patients-----")
        print('ID |          Full Name           |      Doctor`s Full Name      | Age |    Mobile     | Postcode ')
        #ToDo13
        self.view(discharged_patients)

    def manage_discharged(self, discharged_patients):
        """Allow viewing and deleting discharged patients (single or all)."""
        print("-----Manage Discharged Patients-----")
        if not discharged_patients:
            print('No discharged patients.')
            return

        self.view_discharge(discharged_patients)

        print('\nChoose the operation:')
        print(' 1 - Delete a discharged patient')
        print(' 2 - Delete all discharged patients')
        print(' 3 - Back')
        op = input('Input: ').strip()

        if op == '1':
            try:
                idx = int(input('Enter the ID of the discharged patient to delete: ')) - 1
                if idx in range(len(discharged_patients)):
                    removed = discharged_patients.pop(idx)
                    self.save_discharged_to_file(discharged_patients)
                    try:
                        print(f'Patient {removed.full_name()} removed from discharged list.')
                    except Exception:
                        print('Patient removed from discharged list.')
                else:
                    print('The id entered was not found.')
            except ValueError:
                print('The id entered is incorrect')

        elif op == '2':
            confirm = input('Are you sure you want to delete ALL discharged patients? (Y/N): ').lower()
            if confirm in ('y', 'yes'):
                discharged_patients.clear()
                self.save_discharged_to_file(discharged_patients)
                print('All discharged patients deleted.')
            else:
                print('Operation cancelled.')

        elif op == '3':
            return
        else:
            print('Invalid option.')

    def update_details(self):
        """
        Allows the user to update and change username, password and address
        """

        print('Choose the field to be updated:')
        print(' 1 Username')
        print(' 2 Password')
        print(' 3 Address')
        while True:
            try:
                op = int(input('Input: '))
                break
            except ValueError:
                print('Invalid input. Please enter 1, 2, or 3.')

        if op == 1:
            #ToDo14
            new_username = input('Enter the new username: ')
            self.__username = new_username
            print('Username updated.')
            self.save_admin_to_file()
        elif op == 2:
            password = input('Enter the new password: ')
            # validate the password
            if password == input('Enter the new password again: '):
                self.__password = password
                print('Password updated.')
                self.save_admin_to_file()
        elif op == 3:
            #ToDo15
            new_address = input('Enter the new address: ')
            self.__address = new_address
            print('Address updated.')
            self.save_admin_to_file()
        else:
            #ToDo16
            print('Invalid option.')

    def group_patients_by_surname(self, patients):
        print("-----Search Patients by Surname-----")
        surname_search = input('Enter surname to search: ').strip()
        if not surname_search:
            print('No surname entered.')
            return

        matches = [p for p in patients if p.get_surname().lower() == surname_search.lower()]

        if not matches:
            print(f'No patients found with surname {surname_search}.')
            return

        print(f"\nPatients with surname: {surname_search}")
        print('ID |          Full Name           |      Doctor`s Full Name      | Age |    Mobile     | Postcode ')
        for i, patient in enumerate(matches, 1):
            print(f'{i:3}|{patient}')

    def relocate_patient(self, patients, doctors):
        print("-----Relocate Patient-----")
        print("-----Patients-----")
        self.view(patients)
        
        patient_index = input('Please enter the patient ID to relocate: ')
        try:
            patient_index = int(patient_index) - 1
            if patient_index not in range(len(patients)):
                print('The id entered was not found.')
                return
        except ValueError:
            print('The id entered is incorrect')
            return
        
        print("-----Current Doctors-----")
        self.view(doctors)
        
        new_doctor_index = input('Please enter the new doctor ID: ')
        try:
            new_doctor_index = int(new_doctor_index) - 1
            if not self.find_index(new_doctor_index, doctors):
                print('The doctor id entered was not found.')
                return
        except ValueError:
            print('The id entered is incorrect')
            return
        
        patient = patients[patient_index]
        old_doctor_name = patient.get_doctor()
        
        for doctor in doctors:
            if doctor.full_name() == old_doctor_name:
                doctor.remove_patient(patient)
        
        patient.link(doctors[new_doctor_index].full_name())
        doctors[new_doctor_index].add_patient(patient)
        self.save_patients_to_file(patients)
        print(f'Patient {patient.full_name()} relocated to Dr. {doctors[new_doctor_index].full_name()}')

    def management_report(self, doctors, patients):
        print("-----Management Report-----")
        
        print(f"1. Total number of doctors in the system: {len(doctors)}")
        
        print("\n2. Total number of patients per doctor:")
        for doctor in doctors:
            print(f"   Dr. {doctor.full_name()}: {len(doctor.get_patients())} patients")
        
        print("\n3. Patients grouped by illness type (symptoms):")
        illness_groups = {}
        for patient in patients:
            for symptom in patient.get_symptoms():
                if symptom not in illness_groups:
                    illness_groups[symptom] = 0
                illness_groups[symptom] += 1
        
        for illness, count in illness_groups.items():
            print(f"   {illness}: {count} patient(s)")
        
        print("\n4. Family groups (patients with same surname):")
        family_groups = {}
        for patient in patients:
            surname = patient.get_surname()
            if surname not in family_groups:
                family_groups[surname] = []
            family_groups[surname].append(patient)
        
        for surname, group in family_groups.items():
            print(f"   {surname} family: {len(group)} member(s)")

    def patient_management(self, patients, doctors):
        print("-----Patient Management-----")
        print('Choose the operation:')
        print(' 1 - View All Patients')
        print(' 2 - Add New Patient')
        print(' 3 - Update Patient')
        print(' 4 - Group by Surname')
        print(' 5 - Save to File')
        print(' 6 - Load from File')
        print(' 7 - Add Symptoms')

        op = input('Input: ')

        if op == '1':
            self.view_patient(patients)

        elif op == '2':
            print("-----Add New Patient-----")
            first_name = input('Enter first name: ')
            surname = input('Enter surname: ')
            age = int(input('Enter age: '))
            mobile = input('Enter mobile: ')
            postcode = input('Enter postcode: ')
            
            symptoms_input = input('Enter symptoms (comma separated): ')
            symptoms = [s.strip() for s in symptoms_input.split(',')] if symptoms_input else []
            
            patient = Patient(first_name, surname, age, mobile, postcode, symptoms)
            patients.append(patient)
            self.save_patients_to_file(patients)
            print('Patient added.')

        elif op == '3':
            print("-----Update Patient-----")
            self.view_patient(patients)
            try:
                index = int(input('Enter patient ID: ')) - 1
                if index in range(len(patients)):
                    patient = patients[index]
                    print('Choose field to update:')
                    print(' 1 - First Name')
                    print(' 2 - Surname')
                    print(' 3 - Age')
                    print(' 4 - Mobile')
                    print(' 5 - Postcode')
                    choice = int(input('Input: '))
                    
                    if choice == 1:
                        patient.set_first_name(input('New first name: '))
                    elif choice == 2:
                        patient.set_surname(input('New surname: '))
                    elif choice == 3:
                        patient.set_age(int(input('New age: ')))
                    elif choice == 4:
                        patient.set_mobile(input('New mobile: '))
                    elif choice == 5:
                        patient.set_postcode(input('New postcode: '))
                    else:
                        print('Invalid choice.')
                    
                    self.save_patients_to_file(patients)
                    print('Patient updated.')
                else:
                    print('Invalid patient ID.')
            except ValueError:
                print('Invalid input.')

        elif op == '4':
            self.group_patients_by_surname(patients)

        elif op == '5':
            self.save_patients_to_file(patients)
            print('Patients saved to file.')

        elif op == '6':
            patients.clear()
            patients.extend(self.load_patients_from_file())
            print('Patients loaded from file.')

        elif op == '7':
            self.view_patient(patients)
            try:
                index = int(input('Enter patient ID to add symptoms: ')) - 1
                if index in range(len(patients)):
                    symptom = input('Enter symptom: ')
                    patients[index].add_symptom(symptom)
                    self.save_patients_to_file(patients)
                    print('Symptom added.')
                else:
                    print('Invalid patient ID.')
            except ValueError:
                print('Invalid input.')