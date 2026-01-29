class Patient:
    """Patient class"""

    def __init__(self, first_name, surname, age, mobile, postcode, symptoms=None):
        """
        Args:
            first_name (string): First name
            surname (string): Surname
            age (int): Age
            mobile (string): the mobile number
            postcode (string): postcode
            symptoms (list): list of symptoms
        """

        #ToDo1
        self.__first_name = first_name
        self.__surname = surname
        self.__age = age
        self.__mobile = mobile
        self.__postcode = postcode
        self.__doctor = 'None'
        self.__symptoms = symptoms if symptoms else []

    def full_name(self):
        """full name is first_name and surname"""
        #ToDo2
        return f"{self.__first_name} {self.__surname}"
    
    def get_first_name(self):
        return self.__first_name
    
    def get_surname(self):
        return self.__surname
    
    def get_age(self):
        return self.__age
    
    def get_mobile(self):
        return self.__mobile
    
    def get_postcode(self):
        return self.__postcode
    
    def get_doctor(self):
        #ToDo3
        return self.__doctor

    def get_symptoms(self):
        return self.__symptoms
    
    def set_first_name(self, new_first_name):
        self.__first_name = new_first_name
    
    def set_surname(self, new_surname):
        self.__surname = new_surname
    
    def set_age(self, new_age):
        self.__age = new_age
    
    def set_mobile(self, new_mobile):
        self.__mobile = new_mobile
    
    def set_postcode(self, new_postcode):
        self.__postcode = new_postcode
    
    def set_symptoms(self, symptoms):
        self.__symptoms = symptoms
    
    def add_symptom(self, symptom):
        self.__symptoms.append(symptom)

    def link(self, doctor):
        """Args: doctor(string): the doctor full name"""
        self.__doctor = doctor

    def print_symptoms(self):
        """prints all the symptoms"""
        #ToDo4
        print(f"Symptoms for {self.full_name()}:")
        for symptom in self.__symptoms:
            print(f"  - {symptom}")

    def __str__(self):
        return f'{self.full_name():^30}|{self.__doctor:^30}|{self.__age:^5}|{self.__mobile:^15}|{self.__postcode:^10}'