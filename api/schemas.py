from enum import Enum

from pydantic import BaseModel, Field


class Workclass(str, Enum):
    STATE_GOV = "State-gov"
    SELF_EMP_NOT_INC = "Self-emp-not-inc"
    PRIVATE = "Private"
    FEDERAL_GOV = "Federal-gov"
    LOCAL_GOV = "Local-gov"
    UNKNOWN = "?"
    SELF_EMP_INC = "Self-emp-inc"
    WITHOUT_PAY = "Without-pay"
    NEVER_WORKED = "Never-worked"


class Education(str, Enum):
    PRESCHOOL = "Preschool"
    FIRST_TO_FOURTH = "1st-4th"
    FIFTH_TO_SIXTH = "5th-6th"
    SEVENTH_TO_EIGHTH = "7th-8th"
    NINTH = "9th"
    TENTH = "10th"
    ELEVENTH = "11th"
    TWELFTH = "12th"
    HS_GRAD = "HS-grad"
    SOME_COLLEGE = "Some-college"
    ASSOC_ACDM = "Assoc-acdm"
    ASSOC_VOC = "Assoc-voc"
    BACHELORS = "Bachelors"
    MASTERS = "Masters"
    DOCTORATE = "Doctorate"
    PROF_SCHOOL = "Prof-school"


class MaritalStatus(str, Enum):
    NEVER_MARRIED = "Never-married"
    MARRIED_CIV_SPOUSE = "Married-civ-spouse"
    DIVORCED = "Divorced"
    MARRIED_SPOUSE_ABSENT = "Married-spouse-absent"
    SEPARATED = "Separated"
    MARRIED_AF_SPOUSE = "Married-AF-spouse"
    WIDOWED = "Widowed"


class Occupation(str, Enum):
    ADM_CLERICAL = "Adm-clerical"
    EXEC_MANAGERIAL = "Exec-managerial"
    HANDLERS_CLEANERS = "Handlers-cleaners"
    PROF_SPECIALTY = "Prof-specialty"
    OTHER_SERVICE = "Other-service"
    SALES = "Sales"
    CRAFT_REPAIR = "Craft-repair"
    TRANSPORT_MOVING = "Transport-moving"
    FARMING_FISHING = "Farming-fishing"
    MACHINE_OP_INSPCT = "Machine-op-inspct"
    TECH_SUPPORT = "Tech-support"
    UNKNOWN = "?"  # Handling the "?" as UNKNOWN
    PROTECTIVE_SERV = "Protective-serv"
    ARMED_FORCES = "Armed-Forces"
    PRIV_HOUSE_SERV = "Priv-house-serv"


class Relationship(str, Enum):
    NOT_IN_FAMILY = "Not-in-family"
    HUSBAND = "Husband"
    WIFE = "Wife"
    OWN_CHILD = "Own-child"
    UNMARRIED = "Unmarried"
    OTHER_RELATIVE = "Other-relative"


class Race(str, Enum):
    WHITE = "White"
    ASIAN_PAC_ISLANDER = "Asian-Pac-Islander"
    AMER_INDIAN_ESKIMO = "Amer-Indian-Eskimo"
    OTHER = "Other"
    BLACK = "Black"


class Sex(str, Enum):
    MALE = "Male"
    FEMALE = "Female"


class NativeCountry(str, Enum):
    UNITED_STATES = "United-States"
    CUBA = "Cuba"
    JAMAICA = "Jamaica"
    INDIA = "India"
    UNKNOWN = "?"  # Handling the "?" as UNKNOWN
    MEXICO = "Mexico"
    SOUTH = "South"
    PUERTO_RICO = "Puerto-Rico"
    HONDURAS = "Honduras"
    ENGLAND = "England"
    CANADA = "Canada"
    GERMANY = "Germany"
    IRAN = "Iran"
    PHILIPPINES = "Philippines"
    ITALY = "Italy"
    POLAND = "Poland"
    COLUMBIA = "Columbia"
    CAMBODIA = "Cambodia"
    THAILAND = "Thailand"
    ECUADOR = "Ecuador"
    LAOS = "Laos"
    TAIWAN = "Taiwan"
    HAITI = "Haiti"
    PORTUGAL = "Portugal"
    DOMINICAN_REPUBLIC = "Dominican-Republic"
    EL_SALVADOR = "El-Salvador"
    FRANCE = "France"
    GUATEMALA = "Guatemala"
    CHINA = "China"
    JAPAN = "Japan"
    YUGOSLAVIA = "Yugoslavia"
    PERU = "Peru"
    OUTLYING_US = "Outlying-US(Guam-USVI-etc)"
    SCOTLAND = "Scotland"
    TRINIDAD_TOBAGO = "Trinadad&Tobago"
    GREECE = "Greece"
    NICARAGUA = "Nicaragua"
    VIETNAM = "Vietnam"
    HONG = "Hong"
    IRELAND = "Ireland"
    HUNGARY = "Hungary"
    HOLAND_NETHERLANDS = "Holand-Netherlands"


class InputBody(BaseModel):
    age: int = Field(..., gt=0, description="Age of the person")
    workclass: Workclass = Field(..., description="Workclass of the person")
    fnlwgt: int = Field(..., gt=0, description="Final weight")
    education: Education = Field(..., description="Education of the person")
    education_num: int = Field(..., gt=0, description="Number of years of education")
    marital_status: MaritalStatus = Field(
        ..., description="Marital status of the person"
    )
    occupation: Occupation = Field(..., description="Occupation of the person")
    relationship: Relationship = Field(..., description="Relationship of the person")
    race: Race = Field(..., description="Race of the person")
    sex: Sex = Field(..., description="Sex of the person")
    capital_gain: int = Field(..., ge=0, description="Capital gain")
    capital_loss: int = Field(..., ge=0, description="Capital loss")
    hours_per_week: int = Field(..., gt=0, description="Hours per week")
    native_country: NativeCountry = Field(
        ..., description="Native country of the person"
    )
    income: int = Field(..., description="Income of the person")

    def transform(self):
        # Transform income
        income_ = 1 if self.income <= 50000 else 0

        # Transform sex
        sex_ = 1 if self.sex == Sex.MALE else 0

        # Handle native country and categorize as US or Non-US
        country_ = (
            None
            if self.native_country == NativeCountry.UNKNOWN
            else self.native_country
        )
        country_ = 1 if country_ == NativeCountry.UNITED_STATES else 0

        # Map marital status
        marital_status_ = 0
        if self.marital_status in [
            MaritalStatus.DIVORCED,
            MaritalStatus.MARRIED_SPOUSE_ABSENT,
            MaritalStatus.NEVER_MARRIED,
            MaritalStatus.SEPARATED,
            MaritalStatus.WIDOWED,
        ]:
            marital_status_ = 1  # Single
        elif self.marital_status in [
            MaritalStatus.MARRIED_AF_SPOUSE,
            MaritalStatus.MARRIED_CIV_SPOUSE,
        ]:
            marital_status_ = 0  # Couple

        # Transform relationship
        rel_map = {
            Relationship.UNMARRIED: 0,
            Relationship.WIFE: 1,
            Relationship.HUSBAND: 2,
            Relationship.NOT_IN_FAMILY: 3,
            Relationship.OWN_CHILD: 4,
            Relationship.OTHER_RELATIVE: 5,
        }
        relationship_ = rel_map[self.relationship]

        # Transform race
        race_map = {
            Race.WHITE: 0,
            Race.AMER_INDIAN_ESKIMO: 1,
            Race.ASIAN_PAC_ISLANDER: 2,
            Race.BLACK: 3,
            Race.OTHER: 4,
        }
        race_ = race_map[self.race]

        # Transform workclass to employment_type
        employment_type_ = self._workclass_trans(self.workclass)

        # Binary encoding for capital gain and loss
        capital_gain_ = 1 if self.capital_gain > 0 else 0
        capital_loss_ = 1 if self.capital_loss > 0 else 0

        # Return a dictionary of the transformed values
        return {
            "age": self.age,
            "fnlwgt": self.fnlwgt,
            "education_num": self.education_num,
            "hours_per_week": self.hours_per_week,
            "income": income_,
            "sex": sex_,
            "country": country_,
            "marital_status": marital_status_,
            "relationship": relationship_,
            "race": race_,
            "employment_type": employment_type_,
            "capital_gain": capital_gain_,
            "capital_loss": capital_loss_,
        }

    def _workclass_trans(self, workclass):
        if workclass in [
            Workclass.FEDERAL_GOV,
            Workclass.LOCAL_GOV,
            Workclass.STATE_GOV,
        ]:
            return 0  # govt
        elif workclass == Workclass.PRIVATE:
            return 1  # private
        elif workclass in [Workclass.SELF_EMP_INC, Workclass.SELF_EMP_NOT_INC]:
            return 2  # self_employed
        else:
            return 3  # without_pay
