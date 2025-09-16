from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator,model_validator,computed_field
from typing import List,Dict,Optional,Literal,Annotated

class Patient(BaseModel):
    name:Annotated[str,Field(min_length=2,max_length=50,description="Full name of the patient",example="John Doe")]
    age:Annotated[int,Field(ge=0,description="Age of the patient",example=30)]
    weight:Optional[Annotated[float,Field(gt=0,description="Weight of the patient in kg",example=70.5)]]=None
    height:Optional[Annotated[float,Field(gt=0,description="Height of the patient in cm",example=175.0)]]=None
    email:Annotated[EmailStr,Field(description="Email address of the patient",example="john.doe@example.com")]
    website:Optional[Annotated[AnyUrl,Field(description="Website URL of the patient",example="https://johndoe.com")]]=None
    married:Optional[Annotated[Literal["yes","no"],Field(description="Marital status of the patient",example="no")]]="Not specified"
    allergies:Optional[List[Annotated[str,Field(max_length=100)]]]=Field(default_factory=list,description="List of allergies the patient has",
                                        example=["Peanuts","Penicillin"],max_length=5)
    contact_details:Dict[str,str]= Field(...,example={"phone":"123-456-7890","address":"123 Main St"}, 
                                         description="A dictionary containing contact details like phone number and address")
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, value):
        valid_domains=['hdfc.com','axis.com']

        domain=value.split('@')[-1]
        if domain not in valid_domains:
            raise ValueError(f'Email domain must be one of {valid_domains}')
        
    @field_validator('name')
    @classmethod
    def name_upper(cls,value):
        return value.upper()
    
    @model_validator(mode='after')
    @classmethod
    def validate_emergency_contact(cls,model):
        if model.age>60 and'emergency_contact' not in model.contact_details:
            raise ValueError('Emergency contact must be provided in contact_details')
        return model
    
    @computed_field
    @property
    def bmi(self)->Optional[float]:
        if self.weight and self.height:
            height_in_meters=self.height/100
            bmi_value=self.weight/(height_in_meters**2)
            return round(bmi_value,2)
        return None

def patient_info(patient:Patient):
    print(f"Patient Name: {patient.name}")
    print(f"Patient Age: {patient.age}")
    print(f"Patient Email: {patient.email}")
    print(f"Patient Website: {patient.website}")
    print(f"Patient Married: {patient.married}")
    print("Patient Contact Details:")
    for key, value in patient.contact_details.items():
        print(f"  {key}: {value}")
    print(f"Patient BMI: {patient.bmi}")

patient1=Patient(name='John Doe', age=80, email="john.doe@hdfc.com", website="https://johndoe.com", contact_details={"phone": "123-456-7890","emergency_contact":"Jane Doe"}, weight=80, height=175)

patient_info(patient1)