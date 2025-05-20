import express from 'express';
import cors from 'cors';
import predictionRouter from './api/routes/predictions';

const app = express();
const PORT = 3001;

app.use(cors());
app.use(express.json());

app.use('/predictions', predictionRouter) 

app.get('/ping', (_req, _res) => {
    _res.status(200).send('Server is up and running.');
  });

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});