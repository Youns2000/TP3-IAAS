import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [text, setText] = useState('');
  const [translation, setTranslation] = useState('');

  const translateText = async () => {
    try {
      const res = await axios.post('/translate', { text_to_translate: text, lang_to: 'en' });
      setTranslation(res.data.translation);
    } catch (error) {
      console.error(error);
    }
  }

  return (
    <div className="App">
      <input type="text" value={text} onChange={(e) => setText(e.target.value)} />
      <button onClick={translateText}>Translate</button>
      {translation && <p>{translation}</p>}
    </div>
  );
}

export default App;
