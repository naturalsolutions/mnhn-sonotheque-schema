from datetime import date, datetime
from uuid import uuid4
from src.schemas.organization import OrganizationSchema
from src.schemas.person import PersonSchema
from src.schemas.dataset import DatasetSchema


class DefaultRecordFactory:
    def create_default_record(self, record_type: str, **kwargs) -> dict:
        if record_type == "organization":
            default_organization = OrganizationSchema(
                id=uuid4(),
                name="Default Organization",
                type="default",
                dynamic_properties={},
            )
            merged_data = default_organization.model_dump()
            merged_data.update(kwargs)
            return OrganizationSchema(**merged_data).model_dump()
        elif record_type == "person":
            default_person = PersonSchema(
                full_name="Default User",
                email="admin@sonotheque.mnhn.fr",
                birth_date=date(1900, 1, 1),
                death_date=date(1990, 1, 1),
            )
            merged_data = default_person.model_dump()
            merged_data.update(kwargs)
            return PersonSchema(**merged_data).model_dump()
        elif record_type == "dataset":
            default_dataset = DatasetSchema(
                id=uuid4(),
                name="Default Dataset",
                description="Default Dataset",
                doi="10.1000/182",
                contact=uuid4(),
                published_by=uuid4(),
                created_at=datetime.now(),
                updated_at=datetime.now(),
                dynamic_properties={},
            )
            merged_data = default_dataset.model_dump()
            merged_data.update(kwargs)
            return DatasetSchema(**merged_data).model_dump()
        else:
            raise ValueError(f"Unsupported record type: {record_type}")
