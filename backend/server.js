const express = require('express');
const cors = require('cors');
const fs = require('fs');

const app = express();
app.use(cors());

app.get('/summary', (req, res) => {
  fs.readFile('summary_data.json', 'utf8', (err, data) => {
    if (err) {
      console.error('Error reading summary_data.json:', err);
      return res.status(500).json({ error: 'Internal server error' });
    }
    const summary = JSON.parse(data);
    res.json(summary);
  });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});