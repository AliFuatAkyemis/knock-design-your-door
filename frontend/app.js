const dropZone = document.getElementById('dropZone');
const audioInput = document.getElementById('audioInput');
const fileName = document.getElementById('fileName');
const submitBtn = document.getElementById('submitBtn');
const statusBar = document.getElementById('statusBar');
const resultsSection = document.getElementById('resultsSection');

let selectedFile = null;

// Drop zone interactions
dropZone.addEventListener('click', () => audioInput.click());

dropZone.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));

dropZone.addEventListener('drop', (e) => {
  e.preventDefault();
  dropZone.classList.remove('dragover');
  const file = e.dataTransfer.files[0];
  if (file && file.type.startsWith('audio/')) setFile(file);
});

audioInput.addEventListener('change', () => {
  if (audioInput.files[0]) setFile(audioInput.files[0]);
});

function setFile(file) {
  selectedFile = file;
  fileName.textContent = file.name;
  fileName.style.display = 'block';
  submitBtn.disabled = false;
}

// Form submission
submitBtn.addEventListener('click', async () => {
  if (!selectedFile) return;

  submitBtn.disabled = true;
  resultsSection.classList.remove('visible');
  showStatus('Transcribing your cover with Whisper... (this may take 20-60 seconds)', false);

  const formData = new FormData();
  formData.append('audio', selectedFile);
  formData.append('cover_artist', document.getElementById('artistInput').value || 'Unknown Artist');
  formData.append('cover_year', document.getElementById('yearInput').value || '');
  formData.append('cover_style', document.getElementById('styleSelect').value);

  try {
    // Note: do NOT set Content-Type manually — browser adds multipart boundary
    const response = await fetch('/api/process', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const err = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(err.detail || `HTTP ${response.status}`);
    }

    showStatus('Generating your visual artifact...', false);
    const data = await response.json();
    renderResults(data);
  } catch (err) {
    showStatus(`Error: ${err.message}`, true);
    submitBtn.disabled = false;
  }
});

function showStatus(msg, isError) {
  statusBar.textContent = msg;
  statusBar.className = 'status-bar visible' + (isError ? ' error' : '');
}

function renderResults(data) {
  // Image
  const img = document.getElementById('generatedImage');
  img.src = data.image_url;
  const dl = document.getElementById('downloadBtn');
  dl.href = data.image_url;

  // Transcription
  document.getElementById('transcriptionText').textContent = data.transcription.text;
  document.getElementById('langNote').textContent =
    `Language: ${data.transcription.language} — ${data.transcription.confidence_note}`;

  // Analysis
  const themesList = document.getElementById('themesList');
  themesList.innerHTML = data.analysis.themes
    .map(t => `<li>${t}</li>`)
    .join('');

  document.getElementById('emotionalTone').textContent = data.analysis.emotional_tone;
  document.getElementById('dylanInterp').textContent = data.analysis.dylan_interpretation;
  document.getElementById('conn1973').textContent = data.analysis.connection_to_1973;
  document.getElementById('doorSymbol').textContent = data.analysis.door_symbolism;

  // Image prompt
  document.getElementById('imagePromptText').textContent = data.image_prompt;

  // Show results, hide status
  statusBar.classList.remove('visible');
  resultsSection.classList.add('visible');
  submitBtn.disabled = false;

  resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}
