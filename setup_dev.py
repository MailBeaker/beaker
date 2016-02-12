
import json
import requests


headers = {'Content-type': 'application/json'}

base_url = "http://localhost:5000/%s"

users_url = base_url % "api/users/"
orgs_url = base_url % "api/organizations/"
org_users_url = base_url % "api/organizations/%s/users/"
domains_url = base_url % "api/organizations/%s/domains/"
rules_url = base_url % "api/organizations/%s/domains/%s/rules/"

michael = {
    "email": "mike@example.com",
    "first_name": "Michael",
    "last_name": "Smith",
    "password": "test",
    "phone": "5555551234"
}


org = {
    "name": "MailBeaker",
    "billing_address": "1234 Oakwood Lane",
    "billing_phone": "5555551234"
}


domain = {
    "domain_name": "example.com",
    "mx_records": [
        {
            "priority": 10,
            "domain_name": "example.com"
        }
    ]
}

rules = [
    {
        "description": "First Test Rule",
        "alert_admins": True,
        "action": 1,
        "body_mod": 3,
        "body_value": "haxor"
    },
    {
        "description": "Second Test Rule",
        "alert_admins": False,
        "action": 2,
        "sender_mod": 3,
        "sender_value": "computmaxer"
    },
    {
        "description": "Third Test Rule",
        "alert_admins": False,
        "action": 2,
        "sender_mod": 6,
        "sender_value": ".ru"
    }
]

org_id = None
domain_id = None

data = json.dumps(michael)
response = requests.post(users_url, data=data, headers=headers)
michael_id = response.json()['id']

data = json.dumps(org)
response = requests.post(orgs_url, data=data, headers=headers)
if 199 < response.status_code < 300:
    print response.json()
    org_id = response.json()['id']

membership['user_id'] = michael_id
data = json.dumps(membership)
response = requests.post(org_users_url % org_id, data=data, headers=headers)
if 199 < response.status_code < 300:
    print response.json()

data = json.dumps(domain)
response = requests.post(domains_url % org_id, data=data, headers=headers)
if 199 < response.status_code < 300:
    print response.json()
    domain_id = response.json()['id']

for rule in rules:
    data = json.dumps(rule)
    response = requests.post(rules_url % (org_id, domain_id), data=data, headers=headers)
