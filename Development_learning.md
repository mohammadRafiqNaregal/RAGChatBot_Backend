- internal server error when trying to login with email instead of username. or any mismatch in username/email and password. the error is due to the fact that the code is trying to find the user by email instead of username, which is not implemented in the current code. we need to implement the function to find user by email or change the login to use username instead of email.
- unprocessed request error due to pydontic validation error. the login request model is expecting a username field, but the test is sending an email field. we need to change the test to send a username field instead of email, or we need to change the login request model to accept email instead of username.

* fastapi generally returns detail: not found when route does not match.
* check for each feild consistency in all the flow starting from the request model, controller, and router. for example, if we are using username in the request model, then we should use username in the controller and router as well.
* authenticationa and athurization are 2 different things, and can impliment saparate authorization for all the routes.
* route mathting should be carefully handled. else we get not Found error. for example, if we have a route /users/{user_id} and we try to access /users/me, it will not match the route and return not found error. we need to handle this case separately in the router.

\*\*\* understand the work flows like setof tasks same as listing the steps one by one like we do for api intergration in frontend. first action producer, ==> reducer ==> store ==> consumer. this will help us to understand the flow of data and how the different components interact with each other.
