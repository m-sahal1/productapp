# Django Ecommerce Backend Application

This Django backend application is designed to store and manage various e-commerce related objects. It includes models for products, variants, images, collections, categories, and subcategories, with specified relationships between them.

## Models

### Product
- Fields:
  - Title
  - Description
  - Created_at
  - Updated_at

### Variant
- Fields:
  - Title (Title is a combination of product's title and variant's title)
  - Created_at
  - Updated_at
  - Available_for_sale
  - Price

### Image
- Fields:
  - Source
  - Alt_text
  - Updated_at

### Collection
- Fields:
  - Title
  - Published
  - Updated_at

### Category/Subcategory
- Fields:
  - Title
  - Created_at
  - Updated_at

## Conditions

- A product can have multiple variants, but a variant can belong to only one product.
- A variant will always have an associated image.
- Products can have zero or more images, including variant images.
- A product can belong to multiple collections, and a collection can contain multiple products.
- A product can belong to a category or subcategory.
- A category can have multiple levels of subcategories.

## Functionalities

### List Products
- Returns a list of dictionary objects with fields:
  - Title
  - Description
  - Created_at
  - Updated_at
  - Images

### List Variants
- Returns a list of dictionary objects with fields:
  - Title (Title is product’s title + variant’s title)
  - Created_at
  - Updated_at	
  - Available_for_sale
  - Price
  - Image

### List Collections
- Returns a list of dictionaries with fields:
  - Title
  - Published
  - Updated_at

### List Products Belonging to Collections
- Takes collection id as input
- Returns a list of dictionaries with fields:
  - Title
  - Description
  - Created_at
  - Updated_at
  - Images

### List Variants Belonging to a Collection
- Takes collection id as input
- Returns a list of dictionaries with fields:
  - Title (Title is product’s title + variant’s title)
  - Created_at
  - Updated_at	
  - Available_for_sale
  - Price
  - Image

### List Variants Belonging to a Category/Subcategory
- Takes category/subcategory id as input
- Returns a list of variants with fields:
  - Title (Title is product’s title + variant’s title)
  - Created_at
  - Updated_at	
  - Available_for_sale
  - Price
  - Image

## Implementation Details

- UI is not implemented; Django admin page is used for CRUD operations.
- The above functionalities are also available as REST APIs using Django Rest Framework (DRF).
- The application utilizes Django's user model for user authentication.
- User authentication is token-based.
- Create/update operations are restricted to staff users; all other operations are allowed for registered users.

## Celery Integration

- An API is available to send emails to all users.
- Emails are sent to all users after a new product is added, with the subject "New product added" and the body containing the new product's title and description.
- Daily emails are sent to staff users with status updates.

Feel free to customize and expand upon this README as needed for your project.
