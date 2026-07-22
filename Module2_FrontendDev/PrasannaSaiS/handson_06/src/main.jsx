import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { Provider } from 'react-redux';
import { store } from './redux/store';
import { EnrollmentProvider } from './context/EnrollmentContext';
import App from './App.jsx';
import './index.css';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Provider store={store}>
      <EnrollmentProvider>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </EnrollmentProvider>
    </Provider>
  </StrictMode>
);
