import requests

# Replace these with your actual access token and LinkedIn user ID (numeric ID)
access_token = 'your_access_token_here'
linkedin_id = 'your_numeric_linkedin_id_here'  # Replace with your numeric LinkedIn ID

# Define the API URL for UGC post
api_url = 'https://api.linkedin.com/v2/ugcPosts'

# Headers including the Bearer token for authorization
headers = {
    'Authorization': f'Bearer {access_token}',
    'Connection': 'Keep-Alive',
    'Content-Type': 'application/json',
}

# Define the post body as per the UGC post structure
post_body = {
    'author': f'urn:li:person:{linkedin_id}',  # Ensure you're using the numeric LinkedIn ID
    'lifecycleState': 'PUBLISHED',
    'specificContent': {
        'com.linkedin.ugc.ShareContent': {
            'shareCommentary': {
                'text': 'Check out our latest blog post!',
            },
            'shareMediaCategory': 'ARTICLE',
            'media': [
                {
                    'status': 'READY',
                    'description': {
                        'text': 'Read our latest blog post about LinkedIn API!',
                    },
                    'originalUrl': '<your_blog_post_url>', 
                },
            ],
        },
    },
    'visibility': {
        'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC',
    },
}

# Send the POST request to LinkedIn's UGC API
response = requests.post(api_url, headers=headers, json=post_body)

# Check the response status and print the result
if response.status_code == 201:
    print('Post successfully created!')
else:
    print(f'Post creation failed with status code {response.status_code}: {response.text}')
