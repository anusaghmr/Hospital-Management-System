# Imports
from Admin import Admin
from Doctor import Doctor
from Patient import Patient
import sys

def main():
    """
    the main function to be ran when the program runs
    """

    # Initialising the actors
    admin = Admin('admin', '123', 'B1 1AB')# username is 'admin', password is '123'
    try:
        admin.load_admin_from_file()
    except Exception:
        pass
    
    doctors = admin.load_doctors_from_file()
    if not doctors:
        doctors = [
            Doctor('John', 'Smith', 'Internal Med.'),
            Doctor('Jone', 'Smith', 'Pediatrics'),
            Doctor('Jone', 'Carlos', 'Cardiology')
        ]
        admin.save_doctors_to_file(doctors)
    
    patients = admin.load_patients_from_file()
    if not patients:
        patients = [
            Patient('Sara', 'Smith', 20, '07012345678', 'B1 234', ['Fever', 'Cough']),
            Patient('Mike', 'Jones', 37, '07555551234', 'L2 2AB', ['Headache']),
            Patient('David', 'Smith', 15, '07123456789', 'C1 ABC', ['Cold', 'Fatigue'])
        ]
        for patient in patients:
            if patient.get_surname() == 'Smith':
                patient.link('John Smith')
                for doctor in doctors:
                    if doctor.full_name() == 'John Smith':
                        doctor.add_patient(patient)
            elif patient.get_surname() == 'Jones':
                patient.link('Jone Smith')
                for doctor in doctors:
                    if doctor.full_name() == 'Jone Smith':
                        doctor.add_patient(patient)
        admin.save_patients_to_file(patients)
    
    discharged_patients = admin.load_discharged_from_file()

    # keep trying to login tell the login details are correct
    while True:
        try:
            if admin.login():
                running = True # allow the program to run
                break
            else:
                print('Incorrect username or password.')
        except Exception as e:
            print(e)

    while running:
        # print the menu
        print('\n' + '='*50)
        print('HOSPITAL MANAGEMENT SYSTEM')
        print('='*50)
        print('Choose the operation:')
        print(' 1- Doctor Management')
        print(' 2- Patient Management')
        print(' 3- View/Discharge Patients')
        print(' 4- View Discharged Patients')
        print(' 5- Assign Doctor to Patient')
        print(' 6- Relocate Patient to Another Doctor')
        print(' 7- Group Patients by Surname')
        print(' 8- Management Report')
        print(' 9- Update Admin Details')
        print('10- Quit')

        # get the option
        op = input('Option: ')

        if op == '1':
            # 1- Register/view/update/delete doctor
            #ToDo1
            admin.doctor_management(doctors)

        elif op == '2':
            admin.patient_management(patients, doctors)

        elif op == '3':
            # 2- View or discharge patients
            #ToDo2
            admin.view_patient(patients)
            while True:
                op2 = input('Do you want to discharge a patient (Y/N): ').lower()
                if op2 == 'yes' or op2 == 'y':
                    admin.discharge(patients, discharged_patients)
                    break
                elif op2 == 'no' or op2 == 'n':
                    break
                # unexpected entry
                else:
                    print('Please answer by yes or no.')

        elif op == '4':
            # 3 - view discharged patients
            #ToDo4
            admin.manage_discharged(discharged_patients)

        elif op == '5':
            # 4- Assign doctor to a patient
            admin.assign_doctor_to_patient(patients, doctors)

        elif op == '6':
            admin.relocate_patient(patients, doctors)

        elif op == '7':
            admin.group_patients_by_surname(patients)

        elif op == '8':
            admin.management_report(doctors, patients)

        elif op == '9':
            # 5- Update admin detais
            admin.update_details()

        elif op == '10':
            # 6 - Quit
            #ToDo5
            admin.save_doctors_to_file(doctors)
            admin.save_patients_to_file(patients)
            admin.save_discharged_to_file(discharged_patients)
            print("Goodbye!")
            running = False

        else:
            # the user did not enter an option that exists in the menu
            print('Invalid option. Try again')

if __name__ == '__main__':
    main()