#API Documentation:

Base URL: [ip address]:3030/

=================
##Picture Handler: 
- Extension: data/

###GET: Get information about a picture.

Arguments: 
- id: The id of the picture that you want to get information for.

Returns:
- Full picture information in json, including location, user who submitted it, rating, and full picture data.

###POST: Add an image.

Arguments:
- username: The username of the user submitting the image.
- lat: Latitude in degrees
- lon: Longitude in degrees
- rating: Rating from 1-10 given by the user.
- serializedImage: Base64 encoded image data.

Results:
- Database will be updated with this new image, and the user's preferences will be updated accordingly.

==================
##User Handler:
- Extension: users/

###GET: Get information about a user.

Arguments:
- username: The username of the user you are searching for.

Returns:
- A JSON object with username, password, name, preferenceData about various attributes, and a list of images contributed (under 'myItems').

###POST: Create a user.

Arguments:
- username: The username of the user you want to create.
- password: The password of the user you want to create.
- name: The name of the user you want to create.

Results:
- Creates a user with username, password, and name. 
- If this fails, a 400 error is set and the message is set as "User already exists."

===================
##Search Handler:
- Extension: search/

###GET: Search for matches for a user based on various query types.

Arguments:
- username
- [lat] (depends on qType) : Latitude in degrees
- [lon] (depends on qType) : Longitude in degrees
- quant : how many you want
- qType
   1 : By distance (requires lat and lon)
   2 : By rating 
   3 : By preference and rating (returns catered results based on the user's preferences)
   
