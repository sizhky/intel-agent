import os
import requests
import re
from pathlib import Path

# Configuration
REPO_OWNER = "sizhky"
REPO_NAME = "intel-agent"
PROJECT_NAME = "Competitive Intelligence Agent"

def get_project_id(headers):
    """Get the project ID using GraphQL"""
    query = """
    query {
        viewer {
            projectV2(number: 2) {
                id
                title
                url
            }
        }
    }
    """
    
    response = requests.post(
        "https://api.github.com/graphql",
        headers=headers,
        json={"query": query}
    )
    
    if response.status_code == 200:
        data = response.json()
        print("GraphQL Response:", data)  # Debug print
        if "data" in data and "viewer" in data["data"] and "projectV2" in data["data"]["viewer"]:
            project = data["data"]["viewer"]["projectV2"]
            print(f"Found project: {project['title']} ({project['url']})")
            return project['id']
        else:
            print("Could not find project. Response:", data)
            if "errors" in data:
                print("GraphQL Errors:", data["errors"])
    else:
        print(f"GraphQL request failed with status {response.status_code}:", response.text)
    return None

def add_issue_to_project(headers, project_id, issue_node_id):
    """Add an issue to the project using GraphQL"""
    mutation = """
    mutation($projectId: ID!, $issueId: ID!) {
        addProjectV2ItemById(input: {projectId: $projectId, contentId: $issueId}) {
            item {
                id
            }
        }
    }
    """
    
    response = requests.post(
        "https://api.github.com/graphql",
        headers=headers,
        json={
            "query": mutation,
            "variables": {
                "projectId": project_id,
                "issueId": issue_node_id
            }
        }
    )
    return response.status_code == 200

def setup_github_project(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    graphql_headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.project-beta-graphql+json",
        "X-Github-Next-Global-ID": "1"
    }
    
    # Get project ID
    project_id = get_project_id(graphql_headers)
    if not project_id:
        print("Could not find project. Please create a project first.")
        return
    
    base_url = "https://api.github.com"
    
    # Read project board content
    board_path = Path(__file__).parent.parent / ".github" / "project-board.md"
    with open(board_path, "r") as f:
        content = f.read()
    
    # Parse stories from the markdown
    stories = []
    current_phase = None
    story_pattern = r"- \[ \] \*\*Story \d+: (.+?)\*\*\n(.*?)(?=(?:\n- \[ \]|\n###|\n##|$))"
    
    for line in content.split('\n'):
        if line.startswith("### Phase"):
            current_phase = line.replace("### ", "")
        elif "**Story" in line:
            story_match = re.search(story_pattern, content[content.index(line):], re.DOTALL)
            if story_match:
                title = story_match.group(1)
                details = story_match.group(2)
                
                # Extract priority and estimate
                priority = re.search(r"Priority: (\w+)", details).group(1)
                estimate = re.search(r"Estimate: (\d+)", details).group(1)
                
                # Extract tasks
                tasks = []
                for task_line in details.split('\n'):
                    if "[ ]" in task_line and "Tasks:" not in task_line:
                        task = task_line.split("[ ]")[1].strip()
                        tasks.append(task)
                
                stories.append({
                    "title": f"[{current_phase}] {title}",
                    "body": f"""Part of: {current_phase}
Priority: {priority}
Story Points: {estimate}

## Tasks
{"".join([f'- [ ] {task}\n' for task in tasks])}
""",
                    "labels": [priority.lower(), f"points: {estimate}"]
                })
    
    # Create issues and add them to project
    print("Creating issues and adding to project...")
    for story in stories:
        # Create issue
        issue_url = f"{base_url}/repos/{REPO_OWNER}/{REPO_NAME}/issues"
        response = requests.post(
            issue_url,
            headers=headers,
            json={
                "title": story["title"],
                "body": story["body"],
                "labels": story["labels"]
            }
        )
        
        if response.status_code == 201:
            print(f"Created issue: {story['title']}")
            issue_data = response.json()
            
            # Add issue to project
            if add_issue_to_project(graphql_headers, project_id, issue_data["node_id"]):
                print(f"Added issue to project: {story['title']}")
            else:
                print(f"Failed to add issue to project: {story['title']}")
        else:
            print(f"Failed to create issue: {story['title']}")
            print(f"Error: {response.text}")

if __name__ == "__main__":
    token = input("Enter your GitHub Personal Access Token: ")
    setup_github_project(token)
