import requests
import google.generativeai as genai

# GitHub API authentication (use your personal access token)
GITHUB_TOKEN = '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'  # Replace with your actual token
REPO_OWNER = 'arindhimar'  # Owner of the repo (can be your GitHub username or organization)
REPO_NAME = 'CommitBridge'  # Name of the repository you want to track commits for

# Define the GitHub API URL for commits
api_url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits'

# Configure Google Generative AI API key
genai.configure(api_key="YOUR_API_KEY")  # Replace with your actual API key

# Set up the request headers with the authentication token
headers = {
    'Authorization': f'token {GITHUB_TOKEN}'
}

# Function to fetch all commits
def fetch_all_commits():
    commits = []
    page = 1
    
    while True:
        # Get the commits for the specified repository and page
        response = requests.get(api_url, headers=headers, params={'page': page, 'per_page': 100})
        
        if response.status_code != 200:
            print(f"Failed to fetch commits: {response.status_code}")
            break
        
        data = response.json()
        
        if not data:
            break  # No more commits, exit the loop

        # Store commit details
        for commit in data:
            commit_info = {
                'commit_sha': commit['sha'],
                'message': commit['commit']['message'],
                'author_name': commit['commit']['author']['name'],
                'date': commit['commit']['author']['date'],
                'url': commit['html_url'],
                'changes': get_commit_changes(commit['sha'])
            }
            commits.append(commit_info)
        
        page += 1  # Go to the next page if available
    
    return commits

# Function to fetch commit changes (files modified) and the actual code changes (diffs)
def get_commit_changes(commit_sha):
    commit_url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits/{commit_sha}'
    response = requests.get(commit_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch commit details for {commit_sha}: {response.status_code}")
        return []
    
    commit_data = response.json()
    
    # Extract file changes: file name, additions, deletions, and changes (diffs)
    changes = []
    for file in commit_data.get('files', []):
        file_changes = {
            'file_name': file['filename'],
            'status': file['status'],
            'additions': file['additions'],
            'deletions': file['deletions'],
            'patch': file.get('patch', 'No patch available'),  # The actual code changes (diffs)
        }
        changes.append(file_changes)
    
    return changes

# Function to summarize commit information using Gemini
def summarize_commit(commit):
    model = genai.GenerativeModel("gemini-1.5-flash")
    summary_prompt = f"Summarize the following commit:\n\nMessage: {commit['message']}\nChanges: {commit['changes']}"
    
    try:
        response = model.generate_content(summary_prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error summarizing commit: {e}")
        return "Could not generate summary due to an error."

# Get all commits for the given repository
commits = fetch_all_commits()

# Print the results
if commits:
    print(f"Commits made to the repo {REPO_NAME}:")
    for commit in commits:
        print(f"SHA: {commit['commit_sha']}\nMessage: {commit['message']}\nAuthor: {commit['author_name']}\nDate: {commit['date']}\nURL: {commit['url']}\n")
        
        # Print detailed changes (files modified and diffs)
        for change in commit['changes']:
            print(f"File: {change['file_name']}")
            print(f"  Status: {change['status']}")
            print(f"  Additions: {change['additions']}")
            print(f"  Deletions: {change['deletions']}")
            print(f"  Code Changes (diff):\n{change['patch']}\n")
        
        # Summarize the commit
        summary = summarize_commit(commit)
        print(f"Summary: {summary}\n")
else:
    print(f"No commits found for the repo {REPO_NAME}.")