document.getElementById('chat-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const model = document.getElementById('model');
    const prompt = document.getElementById('prompt');
    const responseDiv = document.getElementById('response');
    const loadingDiv = document.getElementById('loading');

    loadingDiv.classList.remove('hidden');

    const response = await fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ 'model': model.value, 'prompt': prompt.value })
    });

    const responseData = await response.json();
    responseDiv.innerHTML += `<p><strong>You:</strong> ${prompt.value}</p>`;
    responseDiv.innerHTML += `<p><strong>AI:</strong> ${responseData}</p>`;
    loadingDiv.classList.add('hidden');
    prompt.value = '';
});

document.getElementById('reset').addEventListener('click', async () => {
    const responseDiv = document.getElementById('response');
    const loadingDiv = document.getElementById('loading');
    loadingDiv.classList.remove('hidden');

    await fetch('/reset', { method: 'POST' });

    responseDiv.innerHTML = '';
    loadingDiv.classList.add('hidden');
});
