# Usage
## Getting started
All application functions can be accessed using the provided Makefile using `make`

To get the flask app up and running, run the following command
```bash
make requirements
make db-init
make up
```

To run the pytest unit tests use
```bash
make test
```

And finally, to run a script to check the required api endpoints (See spec below), use
```bash
make api_features
```

However, if you want to test if yourselves, the relevant endpoints are listed below
```
# Company Employees
http://localhost:5000/api/company/{company_id}/employees
# Common Friends
http://localhost:5000/api/person/{person_a_id}/common_friends/{person_b_id}?eye_color=brown&has_died=false
# Favourite Foods
http://localhost:5000/api/person/{person_a_id}/favourite_foods
```

...Or you can view the swagger API docs at
```
http://localhost:5000/api/
```

## Changing the resources files
If you need to change the resources files, they are located in the resources directory.

The additional `food.json` file has been generated by me to classify fruits and vegetables, so please don't remove it. If you would like to add more fruits and vegetables, feel free to edit the file and rebuild the database (`make db-init`)


# Assumptions
* `Makefile` assumes that Python 3.X is available via command `python`, and Pip 3.X via `pip`. Please edit `Makefile` if this is not true to `python3`/`pip3` or equivalent.
## Database
* Some model field restrictions are chosen based on the provided data. For example:
    * Person.guid, Person.phone, Person._id all have exactly the same length in the provided data, and so is assumed to always be of that length
    * Person.picture, Person.eye_color, Company.name, etc. have tried to be restricted to a reasonable length based on the data provided.
    * Person.balance is represented as cents (Assumed to be the lowest possible split)
## Api
* The `index` field is used as a primary key for the company and person tables, and so is used for `company_id`/`person_id` in the API
* Friend relationships are assumed to be one way (as in, A can be friends with B without B bring friends with A). This assumption is based on people in person.json
* Fruits and vegetables were manually classified as fruits or vegetables. This classification is stored in the food.json file and can be altered if required.

# Paranuara Challenge (Provided Spec)
Paranuara is a class-m planet. Those types of planets can support human life, for that reason the president of the Checktoporov decides to send some people to colonise this new planet and
reduce the number of people in their own country. After 10 years, the new president wants to know how the new colony is growing, and wants some information about his citizens. Hence he hired you to build a rest API to provide the desired information.

The government from Paranuara will provide you two json files (located at resource folder) which will provide information about all the citizens in Paranuara (name, age, friends list, fruits and vegetables they like to eat...) and all founded companies on that planet.
Unfortunately, the systems are not that evolved yet, thus you need to clean and organise the data before use.
For example, instead of providing a list of fruits and vegetables their citizens like, they are providing a list of favourite food, and you will need to split that list (please, check below the options for fruits and vegetables).

## New Features
Your API must provides these end points:
- Given a company, the API needs to return all their employees. Provide the appropriate solution if the company does not have any employees.
- Given 2 people, provide their information (Name, Age, Address, phone) and the list of their friends in common which have brown eyes and are still alive.
- Given 1 people, provide a list of fruits and vegetables they like. This endpoint must respect this interface for the output: `{"username": "Ahi", "age": "30", "fruits": ["banana", "apple"], "vegetables": ["beetroot", "lettuce"]}`

## Delivery
To deliver your system, you need to send the link on GitHub. Your solution must provide tasks to install dependencies, build the system and run. Solutions that does not fit this criteria **will not be accepted** as a solution. Assume that we have already installed in our environment Java, Ruby, Node.js, Python, MySQL, MongoDB and Redis; any other technologies required must be installed in the install dependencies task. Moreover well tested and designed systems are one of the main criteria of this assessement 

## Evaluation criteria
- Solutions written in Python would be preferred.
- Installation instructions that work.
- During installation, we may use different companies.json or people.json files.
- The API must work.
- Tests

Feel free to reach to your point of contact for clarification if you have any questions.
