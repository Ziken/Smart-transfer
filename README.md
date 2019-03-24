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
| id_category  | INT FOREIGN KEY(Cateogry) |

## Available Routes
    GET /transfer/category-item/
    GET /transfer/category-item/<int:id_parent>
    POST /transfer/category/
    GET PUT PATCH DELETE /transfer/category/<int:pk>
    POST /transfer/item/
    GET PUT PATCH DELETE /transfer/item/<int:pk>
    POST /transfer/login/
    POST /transfer/user/