import os

import openai
import praw

# Replace YOUR_GPT3_API_KEY with your own OpenAI API key
openai.api_key = os.environ.get('OPENAPI')
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
username = os.environ.get('USERNAME')
password = os.environ.get('PASS')


# Replace YOUR_CLIENT_ID and YOUR_CLIENT_SECRET with your own Reddit API credentials
def get_reddit_instance():
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent='windows:github.com/matej2/RedditOpenApi:v0.6 (by /u/mtj510)',
                         username=username,
                         password=password)
    if not reddit.read_only:
        print("Connected and running.")
        return reddit
    else:
        return False


def reply_to_comment(comment):
    # Check if the bot is tagged in the comment
    if "u/"+username in comment.body:
        # Use GPT-3 to generate a response to the comment
        response = openai.Completion.create(engine="text-davinci-002", prompt=comment.body, max_tokens=1024,
                                            temperature=0.5).choices[0].text

        print("Replied to response" + comment.body)
        # Post the response as a comment
        comment.reply(response)


def main():
    reddit = get_reddit_instance()

    # Monitor the inbox for new messages
    for message in reddit.inbox.stream():
        # Check if the message is a comment
        if isinstance(message, praw.models.Comment):
            # Reply to the comment if the bot is tagged
            reply_to_comment(message)
            message.mark_read()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
