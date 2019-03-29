# Smart transfer
Simple django project using REST API.


## Tables
**Category**

| Name         | Type                       |
|--------------|----------------------------|
| id           | INT                        |
| id_parent    | INT FOREIGN KEY (Category) |
| created_date | DATA                       |
| created_by   | INT FOREIGN KEY (User)     |

**Item**

| Name         | Type                      |
|--------------|---------------------------|
| name         | VARCHAR(200)              |
| status       | VARCHAR(100)              |
| description  | TEXT                      |
| created_data | DATE                      |
| id_category  | INT FOREIGN KEY(Category) |


## Docs
**Interactive API documentation available at `/docs/` route created with Django REST Swagger**

Available routes:

    GET /transfer/category-item/
    GET /transfer/category-item/{id_parent}
    POST /transfer/category/
    GET /transfer/category/{id}
    PUT /transfer/category/{id}
    PATCH /transfer/category/{id}
    DELETE /transfer/category/{id}
    GET /transfer/item/{id}
    PUT /transfer/item/{id}
    PATCH /transfer/item/{id}
    DELETE /transfer/item/{id}
    POST /transfer/token/
    POST /transfer/user/