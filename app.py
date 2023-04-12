from flask import Flask, render_template, request, jsonify
import requests
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

app = Flask(__name__)

# Replace with your Azure Key Vault URL
KEY_VAULT_URL = 'https://ytadaoakey.vault.azure.net/'

# Connect to Azure Key Vault and retrieve the API key
credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)
api_key = secret_client.get_secret('openaikey').value

API_ENDPOINT = 'https://ytadaopenai.openai.azure.com/v1/engines/davinci-codex/completions'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        prompt = request.form['prompt']
        response = generate_text(prompt)
        return jsonify(response)
    return render_template('index.html')

def generate_text(prompt):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
    }

    data = {
        'prompt': prompt,
        'max_tokens': 150,
        'temperature': 0.7,
    }

    response = requests.post(API_ENDPOINT, headers=headers, json=data)
    response_json = response.json()

    if 'choices' in response_json and len(response_json['choices']) > 0:
        return response_json['choices'][0]['text']
    else:
        return 'Error: Unable to generate text.'

if __name__ == '__main__':
    app.run(debug=True)
