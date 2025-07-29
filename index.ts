// index.ts
import express from 'express';
import { interpretInvocation } from './invocation';
import { storeMemory } from './memory';

const app = express();
app.use(express.json());

app.post('/invoke', (req, res) => {
  const { phrase } = req.body;
  const invocation = interpretInvocation(phrase);
  storeMemory({
    id: Date.now().toString(),
    content: phrase,
    tags: ["invoked"],
    timestamp: Date.now()
  });
  res.send({ status: "received", invocation });
});

app.listen(3001, () => {
  console.log('Cipher Core running on port 3001');
});
