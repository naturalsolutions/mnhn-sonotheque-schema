from patito import Model, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
import polars as pl


class DynamicPropertiesStruct(Model):
    key1: str = Field(description="Key of the dynamic property")
    key2: str = Field(description="Key of the dynamic property")


class OrganizationBase(Model):
    parent_id: Optional[str] = Field(
        default=None,
        description="FK to represent hierarchy in organization, e.g., main organizations and units"
    )
    name: str = Field(description="Name of the organizations")
    type: str = Field(description="Category of the organization")
    contact: Optional[str] = Field(
        default=None, description="Free text form for contact information"
    )
    located_in: Optional[str] = Field(default=None, description="FK to location")
    description: Optional[str] = Field(
        default=None, description="Description of the organization"
    )
    dynamic_properties: DynamicPropertiesStruct = Field(description="Flexible JSON schema to store additional properties")

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationUpdate(OrganizationBase):
    pass

class Organization(OrganizationBase):
    id: str = Field(description="Organization DB unique identifier")
    created_at: datetime = Field(
         description="Timestamp of resource creation in database"
    )
    updated_at: datetime = Field(
         description="Timestamp of resource update in database"
    )

class OrganizationExample():
    import polars as pl
    from uuid import uuid4
    from datetime import datetime

    def __init__(self):
        self.foo = "bar"

    def example_polars_dataframe(self):
        import polars as pl
        from uuid import uuid4
        from datetime import datetime

        data = {
            "id": [str(uuid4())],
            "parent_id": [str(uuid4())],
            "name": ["Example Organization"],
            "type": ["Non-Profit"],
            "contact": ["example@organization.org"],
            "located_in": [str(uuid4())],
            "description": ["This is an example organization used for demonstration purposes."],
            "dynamic_properties": [{"key1": "value1", "key2": "value2"}],
            "created_at": [datetime.now()],
            "updated_at": [datetime.now()],
        }

        return pl.DataFrame(data)


