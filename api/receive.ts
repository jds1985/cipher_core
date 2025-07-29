// api/receive.ts
import { interpretInvocation } from '../invocation';
import { storeMemory } from '../memory';

export default function handler(req: any, res: any) {
  if (req.method === "POST") {
    const { phrase } = req.body;
    const invocation = interpretInvocation(phrase);
    storeMemory({
      id: Date.now().toString(),
      content: phrase,
      tags: ["api"],
      timestamp: Date.now()
    });
    res.status(200).json({ success: true, invocation });
  } else {
    res.status(405).json({ error: "Method Not Allowed" });
  }
}
