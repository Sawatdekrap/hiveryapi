import requests
import pprint

def check_endpoints():
    """Check api endpoints follow the spec below

    - Given a company, the API needs to return all their employees.
        Provide the appropriate solution if the company does not have
        any employees.
    - Given 2 people, provide their information (Name, Age, Address,
        phone) and the list of their friends in common which have brown
        eyes and are still alive.
    - Given 1 people, provide a list of fruits and vegetables they like.
        This endpoint must respect this interface for the output:
        `{"username": "Ahi", "age": "30", "fruits": ["banana", "apple"],
        "vegetables": ["beetroot", "lettuce"]}`
    """
    
    company_id = 1
    endpoint_1 = 'http://localhost:5000/api/company/{company_id}/employees'.format(company_id=company_id)
    print("Given a company, the API needs to return all their employees.")
    print("Using url: {url}".format(url=endpoint_1))
    r = requests.get(endpoint_1)
    if not r.ok:
        print("Failed with status_code {}".format(r.status_code))
    else:
        print(pprint.pformat(r.json()))

    person_a_id = 0
    person_b_id = 1
    endpoint_2 = (
        'http://localhost:5000/api/person/{person_a_id}/common_friends/{person_b_id}?eye_color=brown&has_died=false'
        .format(person_a_id=person_a_id, person_b_id=person_b_id)
    )
    print(
        'Given 2 people, provide their information (Name, Age, Address,'
        'phone) and the list of their friends in common which have brown'
        'eyes and are still alive.'
    )
    print("Using url: {url}".format(url=endpoint_2))
    r = requests.get(endpoint_2)
    if not r.ok:
        print("Failed with status_code {}".format(r.status_code))
    else:
        print(pprint.pformat(r.json()))
    
    person_a_id = 0
    endpoint_3 = 'http://localhost:5000/api/person/{person_a_id}/favourite_foods'.format(person_a_id=person_a_id)
    print('Given 1 people, provide a list of fruits and vegetables they like.')
    print("Using url: {url}".format(url=endpoint_3))
    r = requests.get(endpoint_3)
    if not r.ok:
        print("Failed with status_code {}".format(r.status_code))
    else:
        print(pprint.pformat(r.json()))


if __name__ == '__main__':
    check_endpoints()
