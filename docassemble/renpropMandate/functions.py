import rsaidnumber
from docassemble.base.util import validation_error, as_datetime, DAValidationError
import datetime
from docassemble.base.functions import get_country, phone_number_is_valid,phone_number_formatted

def validate_id_number(x):
    if  x.person_classification == "South African ID Holder":
        try:
            id_number = rsaidnumber.parse(x.unique_number)
            x.date_of_birth = id_number.date_of_birth
            x.sex = id_number.gender.name.title()
            if id_number.citizenship.name == 'SA_CITIZEN':
                x.country_of_citizenship = 'South Africa'
                x.status_in_south_africa = 'Citizen'
            else: 
                x.status_in_south_africa = 'Permanent Resident'
        except:
            validation_error("You have not entered a valid South African Identity Number", field='x.unique_number')
    else:
        x.status_in_south_africa = 'Foreign National'
     
 