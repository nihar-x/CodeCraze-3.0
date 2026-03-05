import { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import Navbar     from './Components/Navbar';
import LoginModal from './Components/LoginModal';

import Home        from './pages/Home';
import BookSlot    from './pages/BookSlot';
import Availability from './pages/Availability';
import Payment     from './pages/Payment';
import MyBookings  from './pages/MyBookings';
import Contact        from './pages/Contact';
import Signup        from './pages/Signup';
import ForgotPassword from './pages/ForgotPassword';

function App() {
  const [loginOpen, setLoginOpen] = useState(false);

  // Allow other components to open the login modal via custom event
  useEffect(() => {
    const handler = () => setLoginOpen(true);
    window.addEventListener('openLogin', handler);
    return () => window.removeEventListener('openLogin', handler);
  }, []);

  return (
    <BrowserRouter>
      <Navbar onLoginClick={() => setLoginOpen(true)} />
      <LoginModal isOpen={loginOpen} onClose={() => setLoginOpen(false)} />

      <Routes>
        <Route path="/"             element={<Home />}         />
        <Route path="/book"         element={<BookSlot />}     />
        <Route path="/availability" element={<Availability />} />
        <Route path="/payment"      element={<Payment />}      />
        <Route path="/bookings"     element={<MyBookings />}   />
        <Route path="/contact"         element={<Contact />}         />
        <Route path="/signup"          element={<Signup />}          />
        <Route path="/forgot-password" element={<ForgotPassword />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
