let typingData = [];
let pasteDetected = false;

document.addEventListener('DOMContentLoaded', () => {
  const inputField = document.getElementById('textInput');

  // Detect typing events
  inputField.addEventListener('keydown', (event) => {
    typingData.push({
      key: event.key,
      time: new Date().getTime()
    });
  });

  // Detect paste events
  inputField.addEventListener('paste', () => {
    pasteDetected = true;
  });
});

async function detectEntryType() {
  if (typingData.length === 0) {
    alert('No typing data detected.');
    return;
  }

  try {
    const response = await fetch('http://127.0.0.1:5000/detect', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ typingData, pasteDetected })
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const result = await response.json();
    alert(result.entryType);
  } catch (error) {
    console.error('Error detecting entry type:', error);
    alert('Error detecting entry type');
  }

  // Reset typingData and pasteDetected for the next input
  typingData = [];
  pasteDetected = false;
}
