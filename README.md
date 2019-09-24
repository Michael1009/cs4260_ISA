# Jersey Marketplace
Our project's goal is to provide a marketplace for Soccer fans to buy and sell used/new jerseys. 

## API

### Create 
_jersey/api/v1/Jersey/create_

In the post body as form data this expects:

A team (CharField), number (PositiveIntegerField), player(CharField), shirt_size(S,M,L,XL,XXL choices), primary color (CharField), secondary color (CharField)

_jersey/api/v1/User/create_

In the post body as form data this expects:

First name (CharField), Last Name(CharField), shirt_size(S,M,L,XL,XXL choices), email (CharField)

### Read
_jersey/api/v1/Jersey_

This returns all Jerseys in the databse.

_jersey/api/v1/User_

This returns all Users in the database.

_jersey/api/v1/Jersey/<int:id>_

This allows you to specify an ID for a Jersey to retur.n

_jersey/api/v1/User/<int:id>_

This allows you to specify an ID for a User to return.

### Update
_jersey/api/v1/Jersey/<int:id>/update_

This takes the exact same form data as the create endpoint but will not create a jersey and instead will update the jersey to whatever data is sent.

_jersey/api/v1/User/<int:id>/update_

This takes the exact same form data as the create endpoint but will not create a user and instead will update the user to whatever data is sent.

### Delete

_jersey/api/v1/User/<int:id>/delete_

This endpoint deletes a user with the specified id.

_jersey/api/v1/Jersey/<int:id>/delete_

This endpoint deletes a jersey with the specified id.


