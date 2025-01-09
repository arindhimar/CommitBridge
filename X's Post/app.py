    from flask import Flask, jsonify
    import tweepy

    app = Flask(__name__)

    # Replace these with your actual API credentials
    BEARER_TOKEN = 'your_bearer_token'
    API_KEY = 'your_api_key'
    API_SECRET = 'your_api_secret'
    ACCESS_TOKEN = 'your_access_token'
    ACCESS_TOKEN_SECRET = 'your_access_token_secret'

    # Authenticate with Twitter API
    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )

    def post_tweet_instantly(tweet_content):
        """Function to post a tweet instantly for testing purposes."""
        try:
            response = client.create_tweet(text=tweet_content)
            print(f"Tweet posted successfully! Tweet ID: {response.data['id']}")
        except tweepy.TweepyException as e:
            print(f"Error posting tweet: {e}")

    @app.route('/post_tweet', methods=['POST'])
    def post_tweet():
        """Endpoint to post a tweet using Twitter API v2."""
        data = request.get_json()
        tweet_content = data.get('tweet')

        if not tweet_content:
            return jsonify({'error': 'Tweet content is required'}), 400

        try:
            response = client.create_tweet(text=tweet_content)
            return jsonify({
                'message': 'Tweet posted successfully',
                'tweet_id': response.data['id']
            }), 200
        except tweepy.TweepyException as e:
            return jsonify({'error': str(e)}), 500

    if __name__ == '__main__':
        # For testing purposes, tweet instantly when the script starts
        test_tweet = "This is a test tweet posted instantly by a Flask script! 🚀"
        post_tweet_instantly(test_tweet)

        # Run the Flask app
        app.run(debug=True)
