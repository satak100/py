const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const PORT = 3000;
app.use(express.json());
app.use(express.static('public'));

const GAME_FILE = path.join(__dirname, 'gamestate.txt');

// Read current state
app.get('/state', (req, res) => {
  const data = fs.readFileSync(GAME_FILE, 'utf8').split(/\r?\n/);
  res.json({ header: data[0], board: data.slice(1,10).map(r=>r.split(' ')) });
});

// Human makes move
app.post('/move', (req, res) => {
  const { r, c } = req.body;
  const data = fs.readFileSync(GAME_FILE, 'utf8').split(/\r?\n/);
  if (!data[0].startsWith('Human Move')) return res.status(400).send('Not your turn');
  data[0] = 'Human Move:';
  let board = data.slice(1,10).map(r=>r.split(' '));
  const cell = board[r][c];
  // simple append; engine.py will handle explosion and write AI Move
  board[r][c] = cell==='0'? '1R': (cell.endsWith('R')? (parseInt(cell)+1)+'R': cell);
  const out = ['Human Move:'].concat(board.map(r=>r.join(' ')));
  fs.writeFileSync(GAME_FILE, out.join('\n'));
  res.sendStatus(200);
});

app.listen(PORT, () => console.log(`UI server listening on http://localhost:${PORT}`));