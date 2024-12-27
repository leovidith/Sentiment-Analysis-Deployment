document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('sentiment-form');
    const textInput = document.getElementById('text-input');
    const resultDiv = document.getElementById('result');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const userInput = textInput.value.trim();
        if (!userInput) {
            resultDiv.textContent = "Please enter some text.";
            return;
        }

        resultDiv.textContent = "Analyzing...";

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: userInput })
            });

            const data = await response.json();
            if (data.error) {
                resultDiv.textContent = `Error: ${data.error}`;
            } else {
                resultDiv.textContent = `Sentiment: ${data.sentiment}`;
            }
        } catch (error) {
            resultDiv.textContent = "An error occurred. Please try again.";
        }
    });
});