import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Button, Form, Container, Row, Col } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Spinner } from 'react-bootstrap';

const App = () => {
  const [text, setText] = useState('');
  const [translation, setTranslation] = useState('');
  const [sourceLang, setSourceLang] = useState('fr');
  const [targetLang, setTargetLang] = useState('en');
  const [file, setFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [userEmail, setUserEmail] = useState('');


  useEffect(() => {
    const fetchEmail = async () => {
      try {
        const res = await axios.get('/email');
        const parts = res.data.email.split('@')[0].split('.');
        const firstName = parts[0];
        const lastName = parts[1];
        setUserEmail("Welcome " + firstName.charAt(0).toUpperCase() + firstName.slice(1) + " " + lastName.charAt(0).toUpperCase() + lastName.slice(1) + " !");
      } catch (error) {
        console.error(error);
      }
    };
    fetchEmail();
  }, []);

  const translateText = async () => {
    setIsLoading(true);
    try {
      const formData = new FormData();
      formData.append('text_to_translate', text);
      formData.append('lang_from', sourceLang);
      formData.append('lang_to', targetLang);
      if (file) {
        formData.append('file', file);
      }

      const res = await axios.post('/translate', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setTranslation(res.data.translation);
      setIsLoading(false);
    } catch (error) {
      console.error(error);
      setIsLoading(false);
    }
  };

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  return (
    <div>
      <Container>

        <Row className="justify-content-md-center" style={{ marginBottom: '20px' }}>
          <Col md="auto">
            <h1>{userEmail}</h1>
          </Col>
        </Row>

        <Row className="justify-content-md-center">
          <Col md="auto">
            <h1>Translator App</h1>
            <Form>
              <Form.Group controlId="sourceLang" className="mb-3">
                <Form.Label>Source Language</Form.Label>
                <Form.Control as="select" value={sourceLang} onChange={(e) => setSourceLang(e.target.value)}>
                  <option value="fr">French</option>
                  <option value="en">English</option>
                  <option value="es">Spanish</option>
                  <option value="de">German</option>
                </Form.Control>
              </Form.Group>
              <Form.Group controlId="targetLang" className="mb-3">
                <Form.Label>Target Language</Form.Label>
                <Form.Control as="select" value={targetLang} onChange={(e) => setTargetLang(e.target.value)}>
                  <option value="fr">French</option>
                  <option value="en">English</option>
                  <option value="es">Spanish</option>
                  <option value="de">German</option>
                </Form.Control>
              </Form.Group>
              <Form.Group controlId="text" className="mb-3">
                <Form.Label>Text to Translate</Form.Label>
                <Form.Control as="textarea" value={text} onChange={(e) => setText(e.target.value)} />
              </Form.Group>
              <Form.Group as={Row} className="mb-3">
                <Form.Control
                  type="file"
                  className="custom-file-label"
                  id="inputGroupFile01"
                  label={"Upload a file"}
                  onChange={handleFileChange}
                  custom
                />
              </Form.Group>
              <Button variant="primary" onClick={translateText} disabled={isLoading}>
                {isLoading ? <Spinner animation="border" /> : 'Translate'}
              </Button>
            </Form>

            {translation && (
              <div>
                <h3>Translation</h3>
                <p>{translation}</p>
              </div>
            )}
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default App;
