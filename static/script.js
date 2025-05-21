const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let drawing = false;

const colorPicker = document.getElementById('color');
const sizePicker = document.getElementById('size');
const player = document.getElementById('player');

canvas.addEventListener('mousedown', () => drawing = true);
canvas.addEventListener('mouseup', () => drawing = false);
canvas.addEventListener('mouseout', () => drawing = false);
canvas.addEventListener('mousemove', draw);

function draw(e) {
  if (!drawing) return;
  ctx.fillStyle = colorPicker.value;
  ctx.beginPath();
  ctx.arc(e.offsetX, e.offsetY, sizePicker.value, 0, Math.PI * 2);
  ctx.fill();
}

function clearCanvas() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  fetch('/clear', { method: 'POST' })
    .then(res => res.json())
    .then(() => {
      player.src = '';
    });
}

function generateMusic() {
  const dataURL = canvas.toDataURL();

  const generateBtn = document.querySelector('button[onclick="generateMusic()"]');
  generateBtn.disabled = true;
  generateBtn.textContent = "Generating...";

  fetch('/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image: dataURL })
  })
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        alert(data.error);
      } else {
        player.src = data.audio_url + '?t=' + new Date().getTime();
        player.play();
      }
    })
    .catch(err => {
      console.error("Error generating music:", err);
      alert("Something went wrong. Please try again.");
    })
    .finally(() => {
      generateBtn.disabled = false;
      generateBtn.textContent = "Generate Music";
    });
}

document.querySelectorAll('.swatch').forEach(swatch => {
  swatch.addEventListener('click', () => {
    const color = swatch.dataset.color;
    colorPicker.value = color;
  });
});

document.querySelector('.control.play').addEventListener('click', () => {
  if (player.paused) {
    player.play();
  } else {
    player.pause();
  }
});