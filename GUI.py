import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from Admin import Admin
from Doctor import Doctor
from Patient import Patient
import os

class SimpleHospitalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital System")
        self.root.geometry("400x500")
        
        # Initialize admin and load data
        self.admin = Admin('admin', '123', 'B1 1AB')
        try:
            self.admin.load_admin_from_file()
        except Exception:
            pass
        
        # Load data
        self.doctors = []
        self.patients = []
        self.discharged_patients = []
        self.load_all_data()
        
        # Create login window
        self.create_login_window()

    def load_all_data(self):
        """Load all data using admin's methods"""
        self.doctors = self.admin.load_doctors_from_file()
        if not self.doctors:
            self.doctors = [
                Doctor('John', 'Smith', 'Internal Med.'),
                Doctor('Jone', 'Smith', 'Pediatrics'),
                Doctor('Jone', 'Carlos', 'Cardiology')
            ]
            self.admin.save_doctors_to_file(self.doctors)
        
        self.patients = self.admin.load_patients_from_file()
        if not self.patients:
            self.patients = [
                Patient('Sara', 'Smith', 20, '07012345678', 'B1 234', ['Fever', 'Cough']),
                Patient('Mike', 'Jones', 37, '07555551234', 'L2 2AB', ['Headache']),
                Patient('David', 'Smith', 15, '07123456789', 'C1 ABC', ['Cold', 'Fatigue'])
            ]
            for patient in self.patients:
                if patient.get_surname() == 'Smith':
                    patient.link('John Smith')
                    for doctor in self.doctors:
                        if doctor.full_name() == 'John Smith':
                            doctor.add_patient(patient)
                elif patient.get_surname() == 'Jones':
                    patient.link('Jone Smith')
                    for doctor in self.doctors:
                        if doctor.full_name() == 'Jone Smith':
                            doctor.add_patient(patient)
            self.admin.save_patients_to_file(self.patients)
        
        self.discharged_patients = self.admin.load_discharged_from_file()

    def create_login_window(self):
        """Create simple login window"""
        self.clear_window()
        
        tk.Label(self.root, text="Hospital Login", font=('Arial', 16)).pack(pady=20)
        
        tk.Label(self.root, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)
        self.username_entry.insert(0, 'admin')
        
        tk.Label(self.root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show='*')
        self.password_entry.pack(pady=5)
        self.password_entry.insert(0, '123')
        
        tk.Button(self.root, text="Login", command=self.login, width=15).pack(pady=20)

    def login(self):
        """Handle login"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if self.admin.authenticate(username, password):
            messagebox.showinfo("Success", "Login successful!")
            self.create_main_menu()
        else:
            messagebox.showerror("Error", "Wrong username or password")

    def clear_window(self):
        """Clear all widgets from window"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_main_menu(self):
        """Create main menu with back to menu option"""
        self.clear_window()
        
        tk.Label(self.root, text="Hospital System", font=('Arial', 16)).pack(pady=20)
        
        # Create buttons for main menu - ADDED VIEW DISCHARGED PATIENTS
        buttons = [
            ("Doctor Management", self.doctor_menu),
            ("Patient Management", self.patient_menu),
            ("View/Discharge Patients", self.view_patients),
            ("View Discharged Patients", self.view_discharged_patients),
            ("Assign Doctor to Patient", self.assign_doctor),
            ("Relocate Patient", self.relocate_patient),
            ("Group by Surname", self.group_patients),
            ("Management Report", self.management_report),
            ("Update Admin", self.update_admin),
            ("Save & Exit", self.save_and_exit)
        ]
        
        for text, command in buttons:
            tk.Button(self.root, text=text, command=command, width=25).pack(pady=5)

    def add_back_button(self, command):
        """Helper to add a back button"""
        tk.Button(self.root, text="← Back to Menu", command=command, width=15).pack(pady=10)

    def doctor_menu(self):
        """Doctor management menu"""
        self.clear_window()
        
        tk.Label(self.root, text="Doctor Management", font=('Arial', 14)).pack(pady=10)
        
        buttons = [
            ("Add Doctor", self.add_doctor_dialog),
            ("View Doctors", self.view_doctors),
            ("Update Doctor", self.update_doctor_menu),
            ("Delete Doctor", self.delete_doctor_menu)
        ]
        
        for text, command in buttons:
            tk.Button(self.root, text=text, command=command, width=20).pack(pady=5)
        
        # Add back button
        self.add_back_button(self.create_main_menu)

    def add_doctor_dialog(self):
        """Custom dialog for adding a doctor with multiple fields"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Doctor")
        dialog.geometry("300x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Enter Doctor Details", font=('Arial', 12)).pack(pady=10)
        
        # First Name
        tk.Label(dialog, text="First Name:").pack(pady=5)
        first_name_entry = tk.Entry(dialog, width=30)
        first_name_entry.pack(pady=5)
        first_name_entry.focus()
        
        # Surname
        tk.Label(dialog, text="Surname:").pack(pady=5)
        surname_entry = tk.Entry(dialog, width=30)
        surname_entry.pack(pady=5)
        
        # Speciality
        tk.Label(dialog, text="Speciality:").pack(pady=5)
        speciality_entry = tk.Entry(dialog, width=30)
        speciality_entry.pack(pady=5)
        
        def save_doctor():
            first_name = first_name_entry.get().strip()
            surname = surname_entry.get().strip()
            speciality = speciality_entry.get().strip()
            
            if not first_name or not surname or not speciality:
                messagebox.showerror("Error", "All fields are required!")
                return
            
            # Check if exists
            for doctor in self.doctors:
                if doctor.full_name() == f"{first_name} {surname}":
                    messagebox.showerror("Error", "Doctor already exists!")
                    return
            
            self.doctors.append(Doctor(first_name, surname, speciality))
            self.admin.save_doctors_to_file(self.doctors)
            messagebox.showinfo("Success", "Doctor added!")
            dialog.destroy()
            self.doctor_menu()
        
        # Save button
        tk.Button(dialog, text="Save", command=save_doctor, width=15).pack(pady=10)
        
        # Cancel button
        tk.Button(dialog, text="Cancel", command=lambda: [dialog.destroy(), self.doctor_menu()], width=15).pack(pady=5)

    def view_doctors(self):
        """View all doctors"""
        if not self.doctors:
            messagebox.showinfo("Info", "No doctors")
            self.doctor_menu()
            return
        
        self.clear_window()
        tk.Label(self.root, text="Doctors List", font=('Arial', 14)).pack(pady=10)
        
        # Create frame for text and scrollbar
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        text_widget = tk.Text(frame, height=15, width=50)
        scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        for i, doctor in enumerate(self.doctors, 1):
            patient_count = len(doctor.get_patients()) if hasattr(doctor, 'get_patients') else 0
            text_widget.insert(tk.END, f"{i}. Dr. {doctor.full_name()} ({doctor.get_speciality()})\n")
            text_widget.insert(tk.END, f"   Patients: {patient_count}\n\n")
        
        text_widget.configure(state='disabled')
        
        # Add back button
        self.add_back_button(self.doctor_menu)

    def update_doctor_menu(self):
        """Show menu for updating doctors"""
        if not self.doctors:
            messagebox.showinfo("Info", "No doctors to update")
            self.doctor_menu()
            return
        
        self.clear_window()
        tk.Label(self.root, text="Select Doctor to Update", font=('Arial', 14)).pack(pady=10)
        
        # Create list of doctors
        for i, doctor in enumerate(self.doctors, 1):
            btn = tk.Button(self.root, 
                          text=f"{i}. Dr. {doctor.full_name()} ({doctor.get_speciality()})",
                          command=lambda d=doctor: self.update_doctor_dialog(d),
                          width=40, anchor='w')
            btn.pack(pady=2)
        
        # Add back button
        self.add_back_button(self.doctor_menu)

    def update_doctor_dialog(self, doctor):
        """Custom dialog for updating a doctor"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Update Doctor")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text=f"Update Dr. {doctor.full_name()}", font=('Arial', 12)).pack(pady=10)
        
        # Field selection
        tk.Label(dialog, text="Select field to update:").pack(pady=5)
        
        field_var = tk.StringVar(value="1")
        
        tk.Radiobutton(dialog, text="First Name", variable=field_var, value="1").pack(anchor='w', padx=20)
        tk.Radiobutton(dialog, text="Surname", variable=field_var, value="2").pack(anchor='w', padx=20)
        tk.Radiobutton(dialog, text="Speciality", variable=field_var, value="3").pack(anchor='w', padx=20)
        
        # New value
        tk.Label(dialog, text="New value:").pack(pady=5)
        value_entry = tk.Entry(dialog, width=30)
        value_entry.pack(pady=5)
        
        def save_update():
            field = field_var.get()
            new_value = value_entry.get().strip()
            
            if not new_value:
                messagebox.showerror("Error", "Please enter a value!")
                return
            
            if field == "1":
                doctor.set_first_name(new_value)
            elif field == "2":
                doctor.set_surname(new_value)
            elif field == "3":
                doctor.set_speciality(new_value)
            
            self.admin.save_doctors_to_file(self.doctors)
            messagebox.showinfo("Success", "Doctor updated!")
            dialog.destroy()
            self.update_doctor_menu()
        
        # Save button
        tk.Button(dialog, text="Save", command=save_update, width=15).pack(pady=10)

    def delete_doctor_menu(self):
        """Show menu for deleting doctors"""
        if not self.doctors:
            messagebox.showinfo("Info", "No doctors to delete")
            self.doctor_menu()
            return
        
        self.clear_window()
        tk.Label(self.root, text="Select Doctor to Delete", font=('Arial', 14)).pack(pady=10)
        
        # Create list of doctors
        for i, doctor in enumerate(self.doctors, 1):
            btn = tk.Button(self.root, 
                          text=f"{i}. Dr. {doctor.full_name()} ({doctor.get_speciality()})",
                          command=lambda d=doctor: self.delete_doctor_confirmation(d),
                          width=40, anchor='w')
            btn.pack(pady=2)
        
        # Add back button
        self.add_back_button(self.doctor_menu)

    def delete_doctor_confirmation(self, doctor):
        """Confirm and delete a doctor"""
        confirm = messagebox.askyesno("Confirm", f"Delete Dr. {doctor.full_name()}?")
        
        if confirm:
            # Remove from patients
            for patient in self.patients:
                if patient.get_doctor() == doctor.full_name():
                    patient.unlink()
            
            # Remove doctor
            self.doctors.remove(doctor)
            self.admin.save_doctors_to_file(self.doctors)
            messagebox.showinfo("Success", "Doctor deleted!")
        
        self.delete_doctor_menu()

    def patient_menu(self):
        """Patient management menu"""
        self.clear_window()
        
        tk.Label(self.root, text="Patient Management", font=('Arial', 14)).pack(pady=10)
        
        buttons = [
            ("Add Patient", self.add_patient_dialog),
            ("View Patients", self.show_patients),
            ("Update Patient", self.update_patient_menu),
            ("Delete Patient", self.delete_patient_menu)
        ]
        
        for text, command in buttons:
            tk.Button(self.root, text=text, command=command, width=20).pack(pady=5)
        
        # Add back button
        self.add_back_button(self.create_main_menu)

    def add_patient_dialog(self):
        """Custom dialog for adding a patient with multiple fields"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Patient")
        dialog.geometry("400x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Enter Patient Details", font=('Arial', 12)).pack(pady=10)
        
        # First Name
        tk.Label(dialog, text="First Name:").pack(pady=2)
        first_name_entry = tk.Entry(dialog, width=30)
        first_name_entry.pack(pady=2)
        first_name_entry.focus()
        
        # Surname
        tk.Label(dialog, text="Surname:").pack(pady=2)
        surname_entry = tk.Entry(dialog, width=30)
        surname_entry.pack(pady=2)
        
        # Age
        tk.Label(dialog, text="Age:").pack(pady=2)
        age_entry = tk.Entry(dialog, width=30)
        age_entry.pack(pady=2)
        
        # Mobile
        tk.Label(dialog, text="Mobile:").pack(pady=2)
        mobile_entry = tk.Entry(dialog, width=30)
        mobile_entry.pack(pady=2)
        
        # Postcode
        tk.Label(dialog, text="Postcode:").pack(pady=2)
        postcode_entry = tk.Entry(dialog, width=30)
        postcode_entry.pack(pady=2)
        
        # Symptoms
        tk.Label(dialog, text="Symptoms (comma separated):").pack(pady=2)
        symptoms_entry = tk.Entry(dialog, width=30)
        symptoms_entry.pack(pady=2)
        
        def save_patient():
            first_name = first_name_entry.get().strip()
            surname = surname_entry.get().strip()
            age_str = age_entry.get().strip()
            mobile = mobile_entry.get().strip()
            postcode = postcode_entry.get().strip()
            symptoms = symptoms_entry.get().strip()
            
            # Validation
            if not first_name or not surname or not age_str or not mobile or not postcode:
                messagebox.showerror("Error", "Please fill all required fields!")
                return
            
            if not age_str.isdigit():
                messagebox.showerror("Error", "Age must be a number!")
                return
            
            age = int(age_str)
            symptoms_list = [s.strip() for s in symptoms.split(',') if s.strip()] if symptoms else []
            
            patient = Patient(first_name, surname, age, mobile, postcode, symptoms_list)
            self.patients.append(patient)
            self.admin.save_patients_to_file(self.patients)
            messagebox.showinfo("Success", "Patient added!")
            dialog.destroy()
            self.patient_menu()
        
        # Save button
        tk.Button(dialog, text="Save", command=save_patient, width=15).pack(pady=10)
        
        # Cancel button
        tk.Button(dialog, text="Cancel", command=lambda: [dialog.destroy(), self.patient_menu()], width=15).pack(pady=5)

    def show_patients(self):
        """Show all patients"""
        if not self.patients:
            messagebox.showinfo("Info", "No patients")
            self.patient_menu()
            return
        
        self.clear_window()
        tk.Label(self.root, text="Patients List", font=('Arial', 14)).pack(pady=10)
        
        # Create frame for text and scrollbar
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        text_widget = tk.Text(frame, height=20, width=70)
        scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        for i, patient in enumerate(self.patients, 1):
            doctor = patient.get_doctor() if hasattr(patient, 'get_doctor') else "None"
            symptoms = ', '.join(patient.get_symptoms())
            text_widget.insert(tk.END, f"{i}. {patient.full_name()}\n")
            text_widget.insert(tk.END, f"   Age: {patient.get_age()}, Doctor: {doctor}\n")
            text_widget.insert(tk.END, f"   Symptoms: {symptoms}\n")
            text_widget.insert(tk.END, f"   Mobile: {patient.get_mobile()}, Postcode: {patient.get_postcode()}\n")
            text_widget.insert(tk.END, "-"*50 + "\n\n")
        
        text_widget.configure(state='disabled')
        
        # Add back button
        self.add_back_button(self.patient_menu)

    def update_patient_menu(self):
        """Show menu for updating patients"""
        if not self.patients:
            messagebox.showinfo("Info", "No patients to update")
            self.patient_menu()
            return
        
        self.clear_window()
        tk.Label(self.root, text="Select Patient to Update", font=('Arial', 14)).pack(pady=10)
        
        # Create list of patients
        for i, patient in enumerate(self.patients, 1):
            btn = tk.Button(self.root, 
                          text=f"{i}. {patient.full_name()} (Age: {patient.get_age()})",
                          command=lambda p=patient: self.update_patient_dialog(p),
                          width=40, anchor='w')
            btn.pack(pady=2)
        
        # Add back button
        self.add_back_button(self.patient_menu)

    def update_patient_dialog(self, patient):
        """Custom dialog for updating a patient"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Update Patient")
        dialog.geometry("350x350")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text=f"Update {patient.full_name()}", font=('Arial', 12)).pack(pady=10)
        
        # Field selection
        tk.Label(dialog, text="Select field to update:").pack(pady=5)
        
        field_var = tk.StringVar(value="1")
        
        fields = [
            ("First Name", "1"),
            ("Surname", "2"),
            ("Age", "3"),
            ("Mobile", "4"),
            ("Postcode", "5"),
            ("Symptoms", "6")
        ]
        
        for text, value in fields:
            tk.Radiobutton(dialog, text=text, variable=field_var, value=value).pack(anchor='w', padx=20)
        
        # New value
        tk.Label(dialog, text="New value:").pack(pady=5)
        value_entry = tk.Entry(dialog, width=30)
        value_entry.pack(pady=5)
        
        # For symptoms, show current value
        if field_var.get() == "6":
            value_entry.insert(0, ', '.join(patient.get_symptoms()))
        
        def save_update():
            field = field_var.get()
            new_value = value_entry.get().strip()
            
            if not new_value:
                messagebox.showerror("Error", "Please enter a value!")
                return
            
            if field == "1":
                patient.set_first_name(new_value)
            elif field == "2":
                patient.set_surname(new_value)
            elif field == "3":
                if not new_value.isdigit():
                    messagebox.showerror("Error", "Age must be a number!")
                    return
                patient.set_age(int(new_value))
            elif field == "4":
                patient.set_mobile(new_value)
            elif field == "5":
                patient.set_postcode(new_value)
            elif field == "6":
                symptoms = [s.strip() for s in new_value.split(',') if s.strip()]
                patient.set_symptoms(symptoms)
            
            self.admin.save_patients_to_file(self.patients)
            messagebox.showinfo("Success", "Patient updated!")
            dialog.destroy()
            self.update_patient_menu()
        
        # Save button
        tk.Button(dialog, text="Save", command=save_update, width=15).pack(pady=10)

    def delete_patient_menu(self):
        """Show menu for deleting patients"""
        if not self.patients:
            messagebox.showinfo("Info", "No patients to delete")
            self.patient_menu()
            return
        
        self.clear_window()
        tk.Label(self.root, text="Select Patient to Delete", font=('Arial', 14)).pack(pady=10)
        
        # Create list of patients
        for i, patient in enumerate(self.patients, 1):
            btn = tk.Button(self.root, 
                          text=f"{i}. {patient.full_name()} (Age: {patient.get_age()})",
                          command=lambda p=patient: self.delete_patient_confirmation(p),
                          width=40, anchor='w')
            btn.pack(pady=2)
        
        # Add back button
        self.add_back_button(self.patient_menu)

    def delete_patient_confirmation(self, patient):
        """Confirm and delete a patient"""
        confirm = messagebox.askyesno("Confirm", f"Delete {patient.full_name()}?")
        
        if confirm:
            # Remove from doctor
            if patient.get_doctor():
                for doctor in self.doctors:
                    if doctor.full_name() == patient.get_doctor():
                        doctor.remove_patient(patient)
                        break
            
            # Remove patient
            self.patients.remove(patient)
            self.admin.save_patients_to_file(self.patients)
            messagebox.showinfo("Success", "Patient deleted!")
        
        self.delete_patient_menu()

    def view_patients(self):
        """View and discharge patients"""
        if not self.patients:
            messagebox.showinfo("Info", "No patients")
            self.create_main_menu()
            return
        
        self.clear_window()
        tk.Label(self.root, text="View/Discharge Patients", font=('Arial', 14)).pack(pady=10)
        
        # Frame for text widget
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        text_widget = tk.Text(frame, height=15, width=70)
        scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        for i, patient in enumerate(self.patients, 1):
            doctor = patient.get_doctor() if hasattr(patient, 'get_doctor') else "None"
            symptoms = ', '.join(patient.get_symptoms())
            text_widget.insert(tk.END, f"{i}. {patient.full_name()}\n")
            text_widget.insert(tk.END, f"   Doctor: {doctor}, Symptoms: {symptoms}\n\n")
        
        text_widget.configure(state='disabled')
        
        # Discharge section
        tk.Label(self.root, text="Enter patient number to discharge:").pack(pady=5)
        discharge_entry = tk.Entry(self.root, width=10)
        discharge_entry.pack(pady=5)
        
        def discharge():
            try:
                index = int(discharge_entry.get()) - 1
                if index < 0 or index >= len(self.patients):
                    messagebox.showerror("Error", "Invalid number")
                    return
            except:
                messagebox.showerror("Error", "Invalid number")
                return
            
            patient = self.patients[index]
            confirm = messagebox.askyesno("Confirm", f"Discharge {patient.full_name()}?")
            
            if confirm:
                # Remove from doctor
                if patient.get_doctor():
                    for doctor in self.doctors:
                        if doctor.full_name() == patient.get_doctor():
                            doctor.remove_patient(patient)
                            break
                
                self.discharged_patients.append(patient)
                del self.patients[index]
                
                self.admin.save_patients_to_file(self.patients)
                self.admin.save_discharged_to_file(self.discharged_patients)
                messagebox.showinfo("Success", "Patient discharged!")
                self.view_patients()  # Refresh
        
        tk.Button(self.root, text="Discharge", command=discharge, width=15).pack(pady=5)
        
        # Add back button
        self.add_back_button(self.create_main_menu)

    def view_discharged_patients(self):
        """View discharged patients"""
        if not self.discharged_patients:
            messagebox.showinfo("Info", "No discharged patients")
            self.create_main_menu()
            return
        
        self.clear_window()
        tk.Label(self.root, text="Discharged Patients", font=('Arial', 14)).pack(pady=10)
        
        # Frame for text widget
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        text_widget = tk.Text(frame, height=20, width=70)
        scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        for i, patient in enumerate(self.discharged_patients, 1):
            doctor = patient.get_doctor() if hasattr(patient, 'get_doctor') else "None"
            symptoms = ', '.join(patient.get_symptoms())
            text_widget.insert(tk.END, f"{i}. {patient.full_name()}\n")
            text_widget.insert(tk.END, f"   Age: {patient.get_age()}, Doctor: {doctor}\n")
            text_widget.insert(tk.END, f"   Symptoms: {symptoms}\n")
            text_widget.insert(tk.END, f"   Mobile: {patient.get_mobile()}, Postcode: {patient.get_postcode()}\n")
            text_widget.insert(tk.END, "-"*50 + "\n\n")
        
        text_widget.configure(state='disabled')
        
        # Add back button
        self.add_back_button(self.create_main_menu)

    def assign_doctor(self):
        """Assign doctor to patient"""
        if not self.patients:
            messagebox.showinfo("Info", "No patients")
            self.create_main_menu()
            return
        if not self.doctors:
            messagebox.showinfo("Info", "No doctors")
            self.create_main_menu()
            return
        
        # Create dialog for assignment
        dialog = tk.Toplevel(self.root)
        dialog.title("Assign Doctor to Patient")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Assign Doctor to Patient", font=('Arial', 12)).pack(pady=10)
        
        # Patient selection
        tk.Label(dialog, text="Select Patient:").pack(pady=5)
        patient_var = tk.StringVar()
        patient_combo = ttk.Combobox(dialog, textvariable=patient_var, state="readonly")
        patient_combo['values'] = [f"{i+1}. {p.full_name()}" for i, p in enumerate(self.patients)]
        patient_combo.pack(pady=5)
        
        # Doctor selection
        tk.Label(dialog, text="Select Doctor:").pack(pady=10)
        doctor_var = tk.StringVar()
        doctor_combo = ttk.Combobox(dialog, textvariable=doctor_var, state="readonly")
        doctor_combo['values'] = [f"{i+1}. Dr. {d.full_name()}" for i, d in enumerate(self.doctors)]
        doctor_combo.pack(pady=5)
        
        def assign():
            patient_str = patient_var.get()
            doctor_str = doctor_var.get()
            
            if not patient_str or not doctor_str:
                messagebox.showerror("Error", "Please select both patient and doctor!")
                return
            
            try:
                patient_idx = int(patient_str.split('.')[0]) - 1
                doctor_idx = int(doctor_str.split('.')[0]) - 1
            except:
                messagebox.showerror("Error", "Invalid selection!")
                return
            
            patient = self.patients[patient_idx]
            doctor = self.doctors[doctor_idx]
            
            # Remove from old doctor
            if patient.get_doctor():
                old_doctor_name = patient.get_doctor()
                for d in self.doctors:
                    if d.full_name() == old_doctor_name:
                        d.remove_patient(patient)
                        break
            
            # Assign to new doctor
            patient.link(doctor.full_name())
            doctor.add_patient(patient)
            
            self.admin.save_patients_to_file(self.patients)
            messagebox.showinfo("Success", f"Assigned {patient.full_name()} to Dr. {doctor.full_name()}")
            dialog.destroy()
            self.create_main_menu()
        
        # Assign button
        tk.Button(dialog, text="Assign", command=assign, width=15).pack(pady=20)
        
        # Cancel button
        tk.Button(dialog, text="Cancel", command=lambda: [dialog.destroy(), self.create_main_menu()], width=15).pack(pady=5)

    def relocate_patient(self):
        """Relocate patient to another doctor"""
        # Get patients with doctors
        patients_with_doctors = []
        for i, patient in enumerate(self.patients):
            if patient.get_doctor():
                patients_with_doctors.append((i, patient))
        
        if not patients_with_doctors:
            messagebox.showinfo("Info", "No patients with assigned doctors")
            self.create_main_menu()
            return
        
        if len(self.doctors) < 2:
            messagebox.showinfo("Info", "Need at least 2 doctors")
            self.create_main_menu()
            return
        
        # Create dialog for relocation
        dialog = tk.Toplevel(self.root)
        dialog.title("Relocate Patient")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Relocate Patient", font=('Arial', 12)).pack(pady=10)
        
        # Patient selection
        tk.Label(dialog, text="Select Patient:").pack(pady=5)
        patient_var = tk.StringVar()
        patient_combo = ttk.Combobox(dialog, textvariable=patient_var, state="readonly")
        patient_combo['values'] = [f"{i+1}. {p.full_name()} (Current: {p.get_doctor()})" for i, p in patients_with_doctors]
        patient_combo.pack(pady=5)
        
        # Doctor selection
        tk.Label(dialog, text="Select New Doctor:").pack(pady=10)
        doctor_var = tk.StringVar()
        doctor_combo = ttk.Combobox(dialog, textvariable=doctor_var, state="readonly")
        doctor_combo['values'] = [f"{i+1}. Dr. {d.full_name()}" for i, d in enumerate(self.doctors)]
        doctor_combo.pack(pady=5)
        
        def relocate():
            patient_str = patient_var.get()
            doctor_str = doctor_var.get()
            
            if not patient_str or not doctor_str:
                messagebox.showerror("Error", "Please select both patient and doctor!")
                return
            
            try:
                # Extract patient index
                patient_idx = int(patient_str.split('.')[0]) - 1
                doctor_idx = int(doctor_str.split('.')[0]) - 1
                
                # Find actual patient
                patient = patients_with_doctors[patient_idx][1]
            except:
                messagebox.showerror("Error", "Invalid selection!")
                return
            
            new_doctor = self.doctors[doctor_idx]
            old_doctor_name = patient.get_doctor()
            
            # Remove from old doctor
            for d in self.doctors:
                if d.full_name() == old_doctor_name:
                    d.remove_patient(patient)
                    break
            
            # Assign to new doctor
            patient.link(new_doctor.full_name())
            new_doctor.add_patient(patient)
            
            self.admin.save_patients_to_file(self.patients)
            messagebox.showinfo("Success", f"Relocated {patient.full_name()} to Dr. {new_doctor.full_name()}")
            dialog.destroy()
            self.create_main_menu()
        
        # Relocate button
        tk.Button(dialog, text="Relocate", command=relocate, width=15).pack(pady=20)
        
        # Cancel button
        tk.Button(dialog, text="Cancel", command=lambda: [dialog.destroy(), self.create_main_menu()], width=15).pack(pady=5)

    def group_patients(self):
        """Group patients by surname"""
        if not self.patients:
            messagebox.showinfo("Info", "No patients")
            self.create_main_menu()
            return
        
        # Group by surname
        groups = {}
        for patient in self.patients:
            surname = patient.get_surname()
            if surname not in groups:
                groups[surname] = []
            groups[surname].append(patient)
        
        self.clear_window()
        tk.Label(self.root, text="Patients by Surname", font=('Arial', 14)).pack(pady=10)
        
        # Frame for text widget
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        text_widget = tk.Text(frame, height=20, width=60)
        scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        for surname in sorted(groups.keys()):
            text_widget.insert(tk.END, f"\n{surname} Family:\n")
            text_widget.insert(tk.END, "="*30 + "\n")
            
            for patient in groups[surname]:
                doctor = patient.get_doctor() if hasattr(patient, 'get_doctor') else "None"
                text_widget.insert(tk.END, f"  • {patient.get_first_name()} {surname} (Age: {patient.get_age()})\n")
                text_widget.insert(tk.END, f"    Doctor: {doctor}\n\n")
        
        text_widget.configure(state='disabled')
        
        # Add back button
        self.add_back_button(self.create_main_menu)

    def management_report(self):
        """Show management report"""
        self.clear_window()
        tk.Label(self.root, text="Management Report", font=('Arial', 14)).pack(pady=10)
        
        # Frame for text widget
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        text_widget = tk.Text(frame, height=25, width=70)
        scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Generate report
        report = "HOSPITAL MANAGEMENT REPORT\n"
        report += "="*50 + "\n\n"
        
        report += f"Total Doctors: {len(self.doctors)}\n"
        report += f"Total Patients: {len(self.patients)}\n"
        report += f"Discharged Patients: {len(self.discharged_patients)}\n\n"
        
        report += "Doctors and their patients:\n"
        report += "-"*30 + "\n"
        for doctor in self.doctors:
            patient_count = len(doctor.get_patients()) if hasattr(doctor, 'get_patients') else 0
            report += f"Dr. {doctor.full_name()}: {patient_count} patients\n"
        
        report += "\nPatients without doctors:\n"
        report += "-"*30 + "\n"
        unassigned = 0
        for patient in self.patients:
            if not patient.get_doctor():
                unassigned += 1
        report += f"Total: {unassigned} patients\n"
        
        # Age average
        if self.patients:
            ages = [p.get_age() for p in self.patients]
            avg_age = sum(ages) / len(ages)
            report += f"\nAverage patient age: {avg_age:.1f}\n"
        
        text_widget.insert(tk.END, report)
        text_widget.configure(state='disabled')
        
        # Add back button
        self.add_back_button(self.create_main_menu)

    def update_admin(self):
        """Update admin details"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Update Admin Details")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Update Admin Details", font=('Arial', 12)).pack(pady=10)
        
        # Field selection
        tk.Label(dialog, text="Select field to update:").pack(pady=5)
        
        field_var = tk.StringVar(value="1")
        
        tk.Radiobutton(dialog, text="Username", variable=field_var, value="1").pack(anchor='w', padx=20)
        tk.Radiobutton(dialog, text="Password", variable=field_var, value="2").pack(anchor='w', padx=20)
        tk.Radiobutton(dialog, text="Address", variable=field_var, value="3").pack(anchor='w', padx=20)
        
        # New value
        tk.Label(dialog, text="New value:").pack(pady=5)
        value_entry = tk.Entry(dialog, width=30)
        value_entry.pack(pady=5)
        
        def save_update():
            field = field_var.get()
            new_value = value_entry.get().strip()
            
            if not new_value:
                messagebox.showerror("Error", "Please enter a value!")
                return
            
            if field == "1":
                self.admin._Admin__username = new_value
                messagebox.showinfo("Success", "Username updated")
            elif field == "2":
                # For password, ask for confirmation
                confirm = simpledialog.askstring("Confirm Password", "Confirm new password:")
                if confirm == new_value:
                    self.admin._Admin__password = new_value
                    messagebox.showinfo("Success", "Password updated")
                else:
                    messagebox.showerror("Error", "Passwords don't match")
                    return
            elif field == "3":
                self.admin._Admin__address = new_value
                messagebox.showinfo("Success", "Address updated")
            
            self.admin.save_admin_to_file()
            dialog.destroy()
            self.create_main_menu()
        
        # Save button
        tk.Button(dialog, text="Save", command=save_update, width=15).pack(pady=10)
        
        # Cancel button
        tk.Button(dialog, text="Cancel", command=lambda: [dialog.destroy(), self.create_main_menu()], width=15).pack(pady=5)

    def save_and_exit(self):
        """Save all data and exit"""
        try:
            self.admin.save_doctors_to_file(self.doctors)
            self.admin.save_patients_to_file(self.patients)
            self.admin.save_discharged_to_file(self.discharged_patients)
            messagebox.showinfo("Success", "All data saved!")
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Save failed: {str(e)}")

def main():
    root = tk.Tk()
    app = SimpleHospitalGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()