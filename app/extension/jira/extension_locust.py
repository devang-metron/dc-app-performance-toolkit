import re
from locustio.common_utils import init_logger, jira_measure, run_as_specific_user  # noqa F401
import json
import random
import requests
import re
import urllib.parse
from locustio.jira.requests_params import jira_datasets
from locustio.common_utils import init_logger, jira_measure, RESOURCE_HEADERS, ADMIN_HEADERS, generate_random_string

logger = init_logger(app_type='jira')
jira_dataset = jira_datasets()

@jira_measure("locust_app_specific_action")
# @run_as_specific_user(username='admin', password='admin')  # run as specific user
def app_specific_action(locust):
    # Select Project
    ADMIN_HEADERS_LOCAL = dict(ADMIN_HEADERS)
    ADMIN_HEADERS_LOCAL["Content-Type"] = 'application/json'
    project = random.choice(jira_dataset['projects'])
    project_id = project[1]

    # Get issue type for the project
    response = locust.get(f'/rest/api/2/issue/createmeta/{project_id}/issuetypes', headers=RESOURCE_HEADERS, catch_response=True)
    content = json.loads(response.content)
    issue_type = content["values"][0]["name"]
    if issue_type == "Epic" and len(content["values"]) > 1:
        issue_type = content["values"][1]["name"]
    logger.locust_info(f"issue_type: {issue_type}")
    
    # Create issue in project
    summary = f'Locust summary {generate_random_string(10, only_letters=True)}'
    description = f'Locust description {generate_random_string(10, only_letters=True)}'
    incident_id = f'IncidentId:1234567'

    
    body = {
        "fields": {
            "project": {
                "id": project_id
                },
            "summary": f"{summary}",
            "description": f"{description}",
            "priority": { "name": "High" },
            "labels":[f"{incident_id}"],
            "issuetype": {"name": issue_type}
            }
        }
        
    logger.locust_info(f"Json Body: {body}")
    logger.info(f"Json Body: {body}")
    logger.info(f'admin headers :{ADMIN_HEADERS}')
  
    
    response = locust.post(f'/rest/api/2/issue', headers=ADMIN_HEADERS_LOCAL, json=body, catch_response=True)
    
    # adding issue property
    response = response.json()
    issue_key = response.get("key","")
    logger.info('issue_key is : {}'.format(issue_key))

    body = {
        "id": "1234567"
    }


    response = requests.put(f'http://a0b4f280e1ef94a408498508c2775226-728806281.us-east-2.elb.amazonaws.com/jira/rest/api/2/issue/{issue_key}/properties/digitalshadows_incident', headers=ADMIN_HEADERS_LOCAL, json=body)# Select Project
 