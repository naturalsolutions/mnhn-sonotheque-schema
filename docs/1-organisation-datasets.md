# 1. L'organisation en `datasets`

## Présentation sommaire

Nous proposons d'organiser l'ensemble des sons et de leur media dérivés (e.g spectrogramme) au sein de **jeux de données** (_datasets_). Les _datasets_ forme un ensemble cohérent de ressources produites et collectés dans un but précis et dans un contexte donné (protocole d'échantillonnage, campagne scientifique, projet de recherche, études d'impact...)

Éléments central d'organisation des données, les _datasets_ peuvent et doivent être lié à des institutions et/ou des organisations. Ces jeux de donnnés ont été créé (_owned_) et peuvent être maintenus (_maintained_) par une ou plusieurs personnes, parfois appelés agent-e-s ou contributeur-rices. Une personne référennte peut également être désigné comme contact.

Il est courant qu'un jeu de données soit associé à une publication via le concept de `Reference`. Nous détaillerons pas ce type de relation dans le schéma actuel mais nous laissons la possibilités aux contributeurs de la base de données d'associé un DOI à chaque _datasets_ créé en base de données

Enfin, les _datasets_ peuvent également être associés à une collection biologique. Du fait de la simplification de notre schéma, les jeux de données peuvet être syonymes de collections.
Toujours dans une perspective de simplification, nous n'avons pas introduit d'organisation hiérarchqiue des jeux de données. En effet, le concept de `Dataset` est [progressivement abandonné](https://dwc.tdwg.org/list/#dwc_Dataset), au profit d'un nouveau standard [ABCD (Access to Biological Collection Data)](https://www.tdwg.org/standards/abcd/). Une intégration de ce standard et de ses concepts associés dans le présent schéma nécessiterait un enrichissement notable de la première ébauche présenté ici.

## Modèle conceptuel de données des classes voisines des `Datasets`

```mermaid
erDiagram
DATASETS ||--o| COLLECTIONS : contains

DATASETS {
    id	uuid	"An identifier for the set of resources"
    name	text	"The name identifying the data set from which the record was derived."
    description	text	"Description of the dataset"
    doi	text	"Publication unique identifier for a reference associated to this datasets"
    created_by	uuid	"Foreign Key to the dataset creator"
    maintained_by	uuid	"Foreign Key to the dataset maintainers; just one maitainer for a given dataset in this version of the schema"
    contact	uuid	"Foreign Key to the contact person for this dataset"
    published_by	uuid	"Foreign Key to the organization"
    created_at	timestamp	"Creation datetime for  this resource"
    updated_at	timestamp	"Modiification datetime for this resource"
    dynamicProperties	JSONB	"Flexible JSON schema to store additionnal properties"
}
ORGANIZATIONS {
    id	uuid	"Organization DB unique identifier"
    parent_id	uuid	"FK to represent hierarchy in organization, e.g., main organizations and units"
    name	text	"Name of the organizations"
    type	text	"Category of the organization"
    contact	text	"Free text form for contact information"
    located_in	uuid	"FK to location"
    description	text	"Description of the organization"
    dynamicProperties	JSONB	"Flexible JSON schema to store additional properties"
}
PEOPLE {
    id	uuid	"Database literal identifier for a person"
    full_name	text	"Full name"
    birth_date	date	"Date of birth"
    death_date	date	"Date of death"
    has_gender	text	"Gender of person, if known or communicated. Stored mainly to distinguish two homonyms"
    email	text	"Contact email"
    identity_provider	text	"If an external identity provider is used (Orcid, OpenId…), "
    identity_token	text	"Key identifier to the external identity provider"
}
MEDIA {
    info	nb	"See 2-media-conncept.md for details"
}
LOCATIONS {
    info	nb	"See 2-media-conncept.md for details"
}
DATASETS ||--o{ MEDIA : has
DATASETS ||--|o PEOPLE : has_contact
PEOPLE }o--o{ DATASETS : maintains
PEOPLE }|--|| DATASETS : created_by
ORGANIZATIONS o|--|{ DATASETS : publishes
ORGANIZATIONS o|--|o LOCATIONS : located_in
ORGANIZATIONS ||--|o PEOPLE : has_contact




```
