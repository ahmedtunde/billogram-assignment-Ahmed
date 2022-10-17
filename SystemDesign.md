### Service User flow
Summary of Use case Description
#### Generation of Discount codes for brands to be used by users
For this flow, the brands would have discount codes generated for them but would need to provide few details of their customized discount.
The brand needs to:
- Give a human-readable string (like AHMED2022BILLO)
- the rule associated with the discount code, such as 5%, 10% etc on all products of the given brand, valid until the end of ...
- Validity Period, the expiry period for the discount code.

The discount code could then be used by all users who haven't used it already.

For this we would need to store
- the discount codes 
- and the discount rules, 
- as well as the consumation of the discount codes to avoid multiple usages.

Then the users are notified by email and can read the discount code and the rule/ term associated with it.

We can later give the brand chance to select what rule for what User groups ie, Users who purchased more than twice before or users who made a purchase of above 100 euro before but for now we can leave that.

#### Fetching the discount code
The user would enter the discount code upon checking out the shopping cart just before making the 
purchase.
The flow would be the following
1. The user sends a request with the string of the discount code (that they retrieved from the email or popped on their screen after requesting a discount from the brand)
2. The server fetches the corresponding discount code from the data store if it exists
3. The server validates the discount code: checks expiry and previous usage. 
4. If the discount code is valid, then a new "discount code usage" is created in the data store and logged. 
5. The discount rule is applied, and the amount to be paid is reduced based on the percentage set in the discount rule.
6. The brand is notified that the user has used the discount code.
7. If the discount code is invalid, the server lets the user know.


### API
This was done in a REST API call.
#### Generating the code
Generating a discount code creates an object in the database (and notifies the users).
- `POST /api/v1/discountcode/`
  - The payload would be the code itself and the rule associated with it.
  The validation would check that the brand (e.g. an admin user) created the discount code for itself, that the expiration 
  date is in the future and the discount is between 0% and 100%.
#### Fetching the code
This flow involves getting the code and logging the usage of the code in the data store.
We might want to wrap this in a remote action call, but I suggest implementing them in two separate requests. 
First the discount code is fetched from the database.
- `GET /api/v1/discountcode/<id>/`
  - I assume the discount codes to be unique so the string itself can double as an id, but it might be a good idea to hash
  the string and put the hash in the URL instead.

Since at this point no validation has been done, we should create the discount code usage explicitly, so it can return 
an error message to the client, in case the discount code existed but is not valid.
- `POST /api/v1/discountcodeusage/`
  - The payload would be the discount code and the user. The validation would check that the user in the payload is the 
  requesting user, and that no such user-discount code pair exists already.

### Data stores
To help decide which kind of database to use for which models, let us start with a back-of-the-envelope estimation first.
If our marketplace has 1000 brands, and they come up with a new discount code every month, then the number of discount 
codes will reach 100 000 in about 8 years. This is a manageable size when fetching discount codes.

The discount codes could have a one-to-one relationship with the rules but there is nothing preventing us from even
re-using the same rules for different campaigns. So the number of discount rules will be on the same magnitude.

However, if we have 1 million users per month, and each of them use 10 discount codes a month (only 1% of the available 
brands), then the number of discount code usages (logs) will grow much quicker, to 100 million in less than a year, 
which is about 4 magnitudes faster than for the discount codes.
Since we need to be able to tell whether a certain user-discount code pair exists in the database, even an indexed 
database call would quickly become unsustainable.

Consequently, I recommend
- a relational database for the discount codes and the discount rules.
- and a non-relational database (e.g. a key-value store) for the discount code logs -- to enable lower latency, better
scalability and higher performance.

#### Data model
- DiscountCode
  - id: string
  - rule: ForeignKey(DiscountRule)
  - validity: datetime
- DiscountRule
  - id: integer
  - brand: ForeignKey(Brand)
  - discount: integer(0<x<100) [percentage]
- DiscountCodeUsage
  - key: hash of the combination of user id and discount code id
  - value: datetime

### Data validation
#### Generating discount codes
The validation would check that
- the brand (e.g. an admin user) created the discount code for itself, 
- the expiration date is in the future 
- and that the discount is between 0% and 100%.

#### The discount code fetching
The validation (when POSTing the discount code usage) would check that
- the expiration date of the discount code is not passed
- the user has not used the discount code (it is not in the logs)

### Async communication
I recommend Celery to schedule asynchronous tasks i.e email notification to users and brands. This kind  of communications need not be other than task scheduling service.

### Authentication
Generating a discount code should only be available for brands.

Fetching a discount code and creating a discount code usage log should only be available for authenticated users.

### If I had more time
-I would create an endpoint for validating tokens, such that it returns the details of a user and the validity of the token.

-I would complete Celery setup and send the emails to users and brands. - completed
-I will put in valid API KEY for sendgrid so that emails can be fired correctly. - 