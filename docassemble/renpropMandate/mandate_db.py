# Import any DAObject classes that you will need
from docassemble.base.util import Individual, Person, DAObject
# Import the SQLObject and some associated utility functions
from docassemble.base.sql import alchemy_url, connect_args, upgrade_db, SQLObject, SQLObjectRelationship
# Import SQLAlchemy names
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, MetaData, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 

# Only allow these names (DAObject classes) to be imported with a modules block
__all__ = ['Owner', 'Account', 'Unit', 'BodyCorporate', 'MandateApplication']

metadata_obj = MetaData(schema="mandate") 

# Create the base class for SQLAlchemy table definitions
Base = declarative_base(metadata=metadata_obj) 
 
# SQLAlchemy table definition for definition of applicants 
class OwnerModel(Base):
    __tablename__ = 'owners'
    id = Column(Integer, primary_key=True)
    unique_identification_number = Column(String(250), unique=True) 
    person_classification = Column(String(250)) 
    person_type = Column(String(250))
    first_name = Column(String(250))
    middle_names = Column(String(250))
    surname = Column(String(250))
    entity_name = Column(String(250))
    primary_contact_number = Column(String(250))
    alternative_contact_number = Column(String(250)) 
    email_address = Column(String(250))
    physical_address = Column(String(250))
    physical_address_city = Column(String(250))
    physical_address_suburb = Column(String(250))
    physical_address_province = Column(String(250))
    physical_address_postal_code = Column(Integer)
    postal_address = Column(String(250))
    postal_address_city = Column(String(250))
    postal_address_suburb = Column(String(250))
    postal_address_province = Column(String(250))
    postal_address_postal_code = Column(Integer)
    # Identity_Document = Column(file) 
    # Proof_of_Address = Column(file)
    # Entity_Resolution = Column(file)
    # Entity_Documents = Column(file)
    cpa_applicable = Column(Boolean) 
    application_id = Column(Integer, ForeignKey('mandate_applications.id', ondelete='CASCADE')) 

class UnitModel(Base):
    __tablename__ = 'units'
    id = Column(Integer, primary_key=True)
    complex_name = Column(String(250))
    complex_unit_number = Column(String(250))
    complex_street_address = Column(String(250))
    complex_city = Column(String(250))
    complex_suburb = Column(String(250))
    complex_province = Column(String(250))
    complex_postal_code = Column(String(250))
    unit_floor = Column(Integer)
    vacant = Column(String(250))
    occupant_name = Column(String(250))
    occupant_contact_number = Column(Integer)
    number_of_bedrooms = Column(Integer)
    number_of_bathrooms = Column(Integer)
    size_m2 = Column(Integer)
    furnished = Column(Boolean)
    lounge = Column(Boolean)
    study = Column(Boolean)
    garden = Column(Boolean)
    parking = Column(Boolean)
    pet_friendly = Column(Boolean)
    application_id = Column(Integer, ForeignKey('mandate_applications.id', ondelete='CASCADE')) 

class AccountModel(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    account_holder = Column(String(250))
    account_type = Column(String(250))
    account_number = Column(String(250))
    bank = Column(String(250))
    application_id = Column(Integer, ForeignKey('mandate_applications.id', ondelete='CASCADE')) 

class BodyCorporateModel(Base):
    __tablename__ = 'body_corporates'
    id = Column(Integer, primary_key=True)
    monthly_levy = Column(Integer)
    renewal_date = Column(String(250))
    account_holder = Column(String(250))
    account_type = Column(String(250))
    account_number = Column(String(250))
    bank = Column(String(250))
    branch_code = Column(Integer)
    address = Column(String(250))
    city = Column(String(250))
    suburb = Column(String(250))
    province = Column(String(250))
    zip = Column(String(250))
    application_id = Column(Integer, ForeignKey('mandate_applications.id', ondelete='CASCADE')) 

class MandateApplicationModel(Base):
    __tablename__ = 'mandate_applications'
    id = Column(Integer, primary_key=True)
    status = Column(String(250))

# Form the URL for connecting to the database based on the "demo db" directive in the Configuration
url = alchemy_url('demo db')
 
# Build the "engine" for connecting to the SQL server, using the URL for the database.
conn_args = connect_args('demo db')
if url.startswith('postgres'):
    engine = create_engine(url, connect_args=conn_args, pool_pre_ping=False)
else: 
    engine = create_engine(url, pool_pre_ping=False)

# Create the tables  
Base.metadata.create_all(engine)

# Get SQLAlchemy ready
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)()

# Perform any necessary database schema updates using alembic, if there is an alembic
# directory and alembic.ini file in the package.
upgrade_db(url, __file__, engine, version_table='auto', conn_args=conn_args)

class Owner(DAObject, SQLObject):
    _model = OwnerModel
    _session = DBSession
    _required = ['unique_identification_number']
    _uid = 'id'

    def init(self, *pargs, **kwargs, ):
        super().init(*pargs, **kwargs)
        self.sql_init()
        if not hasattr(self, 'mandate_application'):
            self.initializeAttribute('mandate_application', MandateApplication)

    def db_get(self, column):
        if column == 'unique_identification_number':
            return self.unique_number
        if column == 'person_classification':
            return self.person_classification
        if column == 'person_type':
            return self.person_type
        if column == 'first_name':
            return self.first_name
        if column == 'middle_names':
            return self.middle_names
        if column == 'surname':
            return self.surname
        if column == 'entity_name':
            return self.entity_name
        if column == 'primary_contact_number':
            return self.primary_contact_number
        if column == 'alternative_contact_number':
            return self.alternative_contact_number
        if column == 'email_address':
            return self.email
        if column == 'physical_address':
            return self.owner_address
        if column == 'physical_address_city':
            return self.city
        if column == 'physical_address_suburb': 
            return self.county
        if column == 'physical_address_province': 
            return self.state
        if column == 'physical_address_postal_code':
            return self.zip
        if column == 'postal_address':
            return self.postal_address
        if column == 'postal_address_city': 
            return self.postal_city
        if column == 'postal_address_suburb': 
            return self.postal_county 
        if column == 'postal_address_province':
            return self.postal_state
        if column == 'postal_address_postal_code':
            return self.postal_zip
        # if column == 'Identity_Document':
        #     return self.
        # if column == 'Proof_of_Address':
        #     return self.
        # if column == 'Entity_Resolution':
        #     return self.
        # if column == 'Entity_Documents':
        #     return self.
        if column == 'cpa_applicable':
            return self.cpa_applicable
        if column == 'application_id':     
            return self.mandate_application.id  
        raise Exception("Invalid column " + column) 

    def db_set(self, column, value):
        if column == 'unique_identification_number':
            self.unique_number = value
        elif column == 'person_classification':
            self.person_classification = value
        elif column == 'person_type':
            self.person_type = value
        elif column == 'first_name':
            self.first_name = value
        elif column == 'middle_names':
            self.middle_names = value
        elif column == 'surname':
            self.surname = value
        elif column == 'entity_name':
            self.entity_name = value
        elif column == 'primary_contact_number':
            self.primary_contact_number = value
        elif column == 'alternative_contact_number':
            self.alternative_contact_number = value
        elif column == 'email_address':
            self.email = value
        elif column == 'physical_address':
            self.owner_address= value
        elif column == 'physical_address_city':
            self.city = value
        elif column == 'physical_address_suburb': 
            self.county = value
        elif column == 'physical_address_province': 
            self.state = value
        elif column == 'physical_address_postal_code':
            self.zip = value
        elif column == 'postal_address':
            self.postal_address= value
        elif column == 'postal_address_city': 
            self.postal_city= value
        elif column == 'postal_address_suburb': 
            self.postal_county= value
        elif column == 'postal_address_province':
            self.postal_state = value
        elif column == 'postal_address_postal_code':
            self.postal_zip = value
        # elif column == 'Identity_Document':
        #     self.unique_id_upload = value
        # elif column == 'Proof_of_Address':
        #     self.proof_of_address_upload = value
        # elif column == 'Entity_Resolution':
        #     self.entity_resolution_upload = value
        # elif column == 'Entity_Documents':
        #     self.entity_documents_upload = value
        elif column == 'cpa_applicable':
            self.cpa_applicable = value
        elif column == 'application_id':
            self.application_id = MandateApplication.by_id(value)
        else:
            raise Exception("Invalid column " + column) 


    def db_null(self, column):
        if column == 'unique_identification_number':
             del self.unique_number  
        elif column == 'person_classification':
             del self.person_classification
        elif column == 'person_type':
             del self.person_type 
        elif column == 'first_name':
             del self.first_name  
        elif column == 'middle_names':
             del self.middle_names  
        elif column == 'surname':
             del self.surname  
        elif column == 'entity_name':
             del self.entity_name  
        elif column == 'primary_contact_number':
             del self.primary_contact_number  
        elif column == 'alternative_contact_number':
             del self.alternative_contact_number  
        elif column == 'email_address':
             del self.email  
        elif column == 'physical_address':
             del self.owner_address 
        elif column == 'physical_address_city':
             del self.city  
        elif column == 'physical_address_suburb': 
             del self.county  
        elif column == 'physical_address_province': 
             del self.state  
        elif column == 'physical_address_postal_code':
             del self.zip  
        elif column == 'postal_address':
             del self.postal_address 
        elif column == 'postal_address_city': 
             del self.postal_city 
        elif column == 'postal_address_suburb': 
             del self.postal_county
        elif column == 'postal_address_province':
             del self.postal_state  
        elif column == 'postal_address_postal_code':
             del self.postal_zip  
        # elif column == 'Identity_Document':
        #      del self.unique_id_upload  
        # elif column == 'Proof_of_Address':
        #      del self.proof_of_address_upload  
        # elif column == 'Entity_Resolution':
        #      del self.entity_resolution_upload  
        # elif column == 'Entity_Documents':
        #      del self.entity_documents_upload  
        elif column == 'cpa_applicable':
             del self.cpa_applicable  
        elif column == 'application_id':
             del self.mandate_application.id
        else:
            raise Exception("Invalid column " + column)

class Unit(DAObject, SQLObject):
    _model = UnitModel
    _session = DBSession
    _required = ['id']
    _uid = 'id'

    def init(self, *pargs, **kwargs, ):
        super().init(*pargs, **kwargs)
        self.sql_init()
        if not hasattr(self, 'mandate_application'):
            self.initializeAttribute('mandate_application', MandateApplication)

    def db_get(self, column):
        if column == 'complex_name':
            return self.name
        elif column == 'complex_unit_number':
            return self.unit_no
        elif column == 'complex_street_address':
            return self.address
        elif column == 'complex_suburb':
            return self.county
        elif column == 'complex_province':
            return self.state
        elif column == 'complex_city':
            return self.city
        elif column == 'complex_postal_code':
            return self.zip
        elif column == 'unit_floor':
            return self.unit_floor
        elif column == 'vacant':
            return self.vacant_on_application
        elif column == 'occupant_name':
            return self.occupant_name
        elif column == 'occupant_contact_number':
            return self.occupant_contact_no
        elif column == 'number_of_bedrooms':
            return self.bedroom_count
        elif column == 'number_of_bathrooms':
            return self.bathroom_count
        elif column == 'size_m2':
            return self.unit_size
        elif column == 'furnished':
            return self.furnished
        elif column == 'lounge':
            return self.lounge
        elif column == 'study':
            return self.study
        elif column == 'garden':
            return self.garden
        elif column == 'parking':
            return self.parking
        elif column == 'pet_friendly':
            return self.pet_friendly
        if column == 'application_id':     
            return self.mandate_application.id  
        else:
            raise Exception("Invalid column " + column) 

    def db_set(self, column, value):
        if column == 'complex_name':
            self.name = value
        elif column == 'complex_unit_number':
            self.unit_no = value
        elif column == 'complex_street_address':
            self.address = value
        elif column == 'complex_suburb':
            self.county = value
        elif column == 'complex_province':
            self.state = value
        elif column == 'complex_city':
            self.city = value
        elif column == 'complex_postal_code':
            self.zip = value
        elif column == 'unit_floor':
            self.unit_floor = value
        elif column == 'vacant':
            self.vacant_on_application = value
        elif column == 'occupant_name':
            self.occupant_name = value
        elif column == 'occupant_contact_number':
            self.occupant_contact_no = value
        elif column == 'number_of_bedrooms':
            self.bedroom_count = value
        elif column == 'number_of_bathrooms':
            self.bathroom_count = value
        elif column == 'size_m2':
            self.unit_size = value
        elif column == 'furnished':
            self.furnished = value
        elif column == 'lounge':
            self.lounge = value
        elif column == 'study':
            self.study = value
        elif column == 'garden':
            self.garden = value
        elif column == 'parking':
            self.parking = value
        elif column == 'pet_friendly':
            self.pet_friendly = value
        elif column == 'application_id':
            self.application_id = MandateApplication.by_id(value)
        else:
            raise Exception("Invalid column " + column) 

    def db_null(self, column):
        if column == 'complex_name':
            del self.name 
        elif column == 'complex_unit_number':
            del self.unit_no 
        elif column == 'complex_street_address':
            del self.address 
        elif column == 'complex_suburb':
            del self.account_holder_name 
        elif column == 'complex_province':
            del self.state 
        elif column == 'complex_city':
            del self.city 
        elif column == 'complex_postal_code':
            del self.zip 
        elif column == 'unit_floor':
            del self.unit_floor 
        elif column == 'vacant':
            del self.vacant_on_application 
        elif column == 'occupant_name':
            del self.occupant_name 
        elif column == 'occupant_contact_number':
            del self.occupant_contact_no 
        elif column == 'number_of_bedrooms':
            del self.bedroom_count 
        elif column == 'number_of_bathrooms':
            del self.bathroom_count 
        elif column == 'size_m2':
            del self.unit_size 
        elif column == 'furnished':
            del self.furnished 
        elif column == 'lounge':
            del self.lounge 
        elif column == 'study':
            del self.study 
        elif column == 'garden':
            del self.garden 
        elif column == 'parking':
            del self.parking 
        elif column == 'pet_friendly':
            del self.pet_friendly 
        elif column == 'application_id':
             del self.mandate_application.id
        else:
            raise Exception("Invalid column " + column)

class Account(DAObject, SQLObject):
    _model = AccountModel
    _session = DBSession
    _required = ['account_number']
    _uid = 'id'

    def init(self, *pargs, **kwargs, ):
        super().init(*pargs, **kwargs)
        self.sql_init()
        if not hasattr(self, 'mandate_application'):
            self.initializeAttribute('mandate_application', MandateApplication)

    def db_get(self, column):
        if column == 'account_holder':
            return self.account_holder_name 
        elif column == 'account_type':
            return self.account_type 
        elif column == 'account_number':
            return self.bank_account_number 
        elif column == 'bank':
            return self.account_bank
        if column == 'application_id':     
            return self.mandate_application.id   
        else:
            raise Exception("Invalid column " + column) 

    def db_set(self, column, value):
        if column == 'account_holder':
            self.account_holder_name = value
        elif column == 'account_type':
            self.account_type = value
        elif column == 'account_number':
            self.bank_account_number = value
        elif column == 'bank':
            self.account_bank = value
        elif column == 'application_id':
            self.application_id = MandateApplication.by_id(value)
        else:
            raise Exception("Invalid column " + column) 

    def db_null(self, column):
        if column == 'account_holder':
             del self.account_holder_name 
        elif column == 'account_type':
             del self.account_type   
        elif column == 'account_number':
             del self.bank_account_number   
        elif column == 'bank':
             del self.account_bank   
        elif column == 'application_id':
             del self.mandate_application.id
        else:
            raise Exception("Invalid column " + column)

class BodyCorporate(DAObject, SQLObject):
    _model = BodyCorporateModel
    _session = DBSession
    _required = ['account_number']
    _uid = 'id'

    def init(self, *pargs, **kwargs, ):
        super().init(*pargs, **kwargs)
        self.sql_init()
        if not hasattr(self, 'mandate_application'):
            self.initializeAttribute('mandate_application', MandateApplication)

    def db_get(self, column): 
        if column == 'monthly_levy':
            return self.monthly_levy 
        elif column == 'renewal_date':
            return self.Levy_Renewal_Date 
        elif column == 'account_holder':
            return self.corporate_account_holder_name 
        elif column == 'account_type':
            return self.account_type 
        elif column == 'account_number':
            return self.account_no 
        elif column == 'bank':
            return self.bank 
        elif column == 'branch_code':
            return self.branch 
        elif column == 'address':
            return self.address 
        elif column == 'city':
            return self.city 
        elif column == 'suburb':
            return self.county 
        elif column == 'province':
            return self.state 
        elif column == 'zip':
            return self.zip 
        if column == 'application_id':     
            return self.mandate_application.id   
        else:
            raise Exception("Invalid column " + column) 

    def db_set(self, column, value):
        if column == 'monthly_levy':
            self.monthly_levy = value
        elif column == 'renewal_date':
            self.Levy_Renewal_Date = value
        elif column == 'account_holder':
            self.corporate_account_holder_name = value
        elif column == 'account_type':
            self.account_type = value
        elif column == 'account_number':
            self.account_no = value
        elif column == 'bank': 
            self.bank = value
        elif column == 'branch_code': 
            self.branch = value
        elif column == 'address':
            self.address = value
        elif column == 'city':
            self.city = value
        elif column == 'suburb':
            self.county = value
        elif column == 'province':
            self.state = value
        elif column == 'zip':
            self.zip = value
        elif column == 'application_id':
            self.application_id = MandateApplication.by_id(value)
        else:
            raise Exception("Invalid column " + column) 

    def db_null(self, column):
        if column == 'monthly_levy':
             del self.monthly_levy 
        elif column == 'renewal_date':
            del self.Levy_Renewal_Date
        elif column == 'account_holder':
             del self.corporate_account_holder_name   
        elif column == 'account_type':
             del self.account_type   
        elif column == 'account_number':
             del self.account_no  
        elif column == 'bank':
             del self.bank
        elif column == 'branch_code':
             del self.branch
        elif column == 'address':
             del self.address  
        elif column == 'city':
             del self.city  
        elif column == 'suburb':
             del self.county  
        elif column == 'province':
             del self.state  
        elif column == 'zip':
             del self.zip  
        elif column == 'application_id':
             del self.mandate_application.id
        else:
            raise Exception("Invalid column " + column)

class MandateApplication(DAObject, SQLObject):
    _model = MandateApplicationModel
    _session = DBSession
    _required = ['id']
    _uid = 'id' 

    def init(self, *pargs, **kwargs, ):
        super().init(*pargs, **kwargs)
        self.sql_init() 

    def db_get(self, column): 
        if column == 'status':
            return self.status 
        else:
            raise Exception("Invalid column " + column) 

    def db_set(self, column, value):
        if column == 'status':
            self.status = value  
        else:
            raise Exception("Invalid column " + column) 

    def db_null(self, column):
        if column == 'status':
            del self.status  
        else:
            raise Exception("Invalid column " + column)