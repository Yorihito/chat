import os
import openai
from flask import Flask, render_template, request, jsonify
import requests
#from azure.identity import DefaultAzureCredential
#from azure.keyvault.secrets import SecretClient

app = Flask(__name__)

# Replace with your Azure Key Vault URL
#KEY_VAULT_URL = 'https://ytadaoakey.vault.azure.net/'

# Connect to Azure Key Vault and retrieve the API key
#credential = DefaultAzureCredential()
#secret_client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)
#api_key = secret_client.get_secret('openaikey').value
api_key = '9c3dc9eadc174f93b665dceaddca2f84'

openai.api_type = "azure"
openai.api_base = "https://ytadaopenai.openai.azure.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = api_key
systemmsg = {"role": "system", "content": "You are a helpful assistant."}
messages = [systemmsg]

def add_message(msg, role, content):
    new_message = {"role": role, "content": content}
    msg.append(new_message)

@app.route('/reset', methods=['POST'])
def reset_messages():
    global messages
    messages = [systemmsg]
    return jsonify({"status": "success"})

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        prompt = request.form['prompt']
        add_message(messages, "user", prompt)
        response = generate_text(messages)
        return jsonify(response)
    return render_template('index.html')

def generate_text(msg):

    response = openai.ChatCompletion.create(
        engine="gpt4",
        messages = msg,
        temperature=0.9,
        max_tokens=800,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None)

    if 'choices' in response and len(response['choices']) > 0:
        resp = response['choices'][0]['message']['content']
        add_message(msg, "assistant", resp)
        return resp
    else:
        return 'Error: Unable to generate text.'

if __name__ == '__main__':
    app.run(debug=True)
