const express = require('express');
const cors = require('cors');
const fs = require('fs');

const app = express();
app.use(cors());


function readSummaryData() {
  try {
    const data = fs.readFileSync('summary_data.json', 'utf8');
    return JSON.parse(data);
  } catch (err) {
    console.error('Error reading summary_data.json:', err);
    return null;
  }
}


app.get('/api/summary', (req, res) => {
  const summary = readSummaryData();
  if (!summary) return res.status(500).json({ error: 'Internal server error' });

  res.json(summary.overall_metrics);
});


app.get('/api/channels', (req, res) => {
  const summary = readSummaryData();
  if (!summary) return res.status(500).json({ error: 'Internal server error' });

  let channels = summary.channel_metrics;


  const { sort_by = 'roas', order = 'desc' } = req.query;
  channels.sort((a, b) => {
    if (order === 'asc') return a[sort_by] - b[sort_by];
    return b[sort_by] - a[sort_by];
  });

  res.json({ channels });
});


app.get('/api/monthly', (req, res) => {
  const summary = readSummaryData();
  if (!summary) return res.status(500).json({ error: 'Internal server error' });

  let monthly = summary.monthly_metrics;
  const { month } = req.query;
  if (month) monthly = monthly.filter(m => m.month === month);

  res.json({ monthly_data: monthly });
});


app.get('/api/campaigns', (req, res) => {
  const summary = readSummaryData();
  if (!summary) return res.status(500).json({ error: 'Internal server error' });

  let campaigns = summary.top_campaigns || []; 
  const { channel, min_roas, max_roas } = req.query;

  if (channel) campaigns = campaigns.filter(c => c.channel === channel);
  if (min_roas) campaigns = campaigns.filter(c => c.roas >= parseFloat(min_roas));
  if (max_roas) campaigns = campaigns.filter(c => c.roas <= parseFloat(max_roas));

  res.json({ campaigns });
});


app.get('/api/insights', (req, res) => {
  const summary = readSummaryData();
  if (!summary) return res.status(500).json({ error: 'Internal server error' });

  res.json({
    insights: summary.insights,
    generated_at: new Date().toISOString()
  });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});