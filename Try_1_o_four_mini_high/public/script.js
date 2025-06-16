const boardEl = document.getElementById('board');
let boardData = [];

async function fetchState() {
  const res = await fetch('/state');
  const json = await res.json();
  boardData = json.board;
  render();
}

function render() {
  boardEl.innerHTML = '';
  boardData.forEach((row, i) => row.forEach((cell, j) => {
    const el = document.createElement('div');
    el.className = 'cell';
    el.onclick = () => humanMove(i,j);
    if (cell !== '0') {
      const cnt = +cell.slice(0,-1), col = cell.slice(-1);
      for(let k=0;k<cnt;k++){
        const orb = document.createElement('div');
        orb.className = `orb ${col}`;
        orb.style.top = `${(k%2)*15+10}px`;
        orb.style.left = `${Math.floor(k/2)*15+10}px`;
        el.appendChild(orb);
      }
    }
    boardEl.appendChild(el);
  }));
}

async function humanMove(r,c) {
  await fetch('/move', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({r,c}) });
}

setInterval(fetchState, 1000);
fetchState();