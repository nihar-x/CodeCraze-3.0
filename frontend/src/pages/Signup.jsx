import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  FaEnvelope, FaCheckCircle, FaCar, FaPaperPlane
} from 'react-icons/fa';
import { sendMagicLink } from '../services/api';

const perks = [
  { icon: '🚗', text: 'Book parking slots in seconds' },
  { icon: '📍', text: 'Real-time slot availability' },
  { icon: '💳', text: 'Secure, hassle-free payments' },
  { icon: '📱', text: 'Instant SMS & email confirmations' },
];

const Signup = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isSent, setIsSent] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await sendMagicLink({ email });
      setIsSent(true);
    } catch (err) {
      setError(err.message || 'Failed to send login link. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen pt-[60px] overflow-hidden">
      {/* ── Left Panel ── */}
      <div
        className="hidden lg:flex lg:w-[42%] flex-col justify-between p-12 relative overflow-hidden flex-shrink-0"
        style={{
          background: 'linear-gradient(150deg, #0d0a28 0%, #1a1050 50%, #0b1630 100%)',
        }}
      >
        {/* Glow blobs */}
        <div className="absolute top-0 left-0 w-80 h-80 rounded-full pointer-events-none"
          style={{ background: 'radial-gradient(circle, rgba(124,58,237,0.35) 0%, transparent 70%)' }} />
        <div className="absolute bottom-0 right-0 w-72 h-72 rounded-full pointer-events-none"
          style={{ background: 'radial-gradient(circle, rgba(37,99,235,0.25) 0%, transparent 70%)' }} />

        <div className="relative z-10 h-6" />

        <div className="relative z-10">
          <h2 className="text-[36px] font-extrabold text-white leading-tight tracking-tight mb-4">
            Park smarter,<br />
            <span style={{
              background: 'linear-gradient(135deg, #a78bfa, #60a5fa)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}>
              live better.
            </span>
          </h2>
          <p className="text-white/50 text-[14px] leading-relaxed mb-8">
            Join thousands of drivers who save time and money with intelligent parking management.
          </p>

          <div className="space-y-4">
            {perks.map((p, i) => (
              <div key={i} className="flex items-center gap-3">
                <span className="w-9 h-9 rounded-xl bg-white/8 border border-white/10 flex items-center justify-center text-base flex-shrink-0">
                  {p.icon}
                </span>
                <span className="text-white/70 text-[13px] font-medium">{p.text}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="relative z-10 text-white/30 text-[11px]">
          © 2025 ParkMate. All rights reserved.
        </div>
      </div>

      {/* ── Right Panel ── */}
      <div className="flex-1 flex items-center justify-center px-6 py-8 bg-[#f4f3fb] overflow-y-auto">
        <div className="w-full max-w-[420px] my-auto">
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
            <div className="h-1 w-full" style={{ background: 'linear-gradient(90deg, #7c3aed, #4f46e5, #2563eb)' }} />

            <div className="p-8">
              {isSent ? (
                <div className="text-center py-10 animate-fade-up">
                  <div className="w-20 h-20 rounded-2xl bg-emerald-50 text-emerald-500 flex items-center justify-center text-4xl mx-auto mb-6">
                    <FaPaperPlane className="translate-x-1 -translate-y-1" />
                  </div>
                  <h1 className="text-[24px] font-black text-gray-900 mb-3 leading-tight">
                    Check your inbox!
                  </h1>
                  <p className="text-[14px] text-gray-500 leading-relaxed mb-8">
                    We've sent a magic login link to <br />
                    <span className="font-bold text-gray-900">{email}</span>. <br />
                    Click it to instantly create your account and log in.
                  </p>

                  <div className="space-y-4 pt-4">
                    <button
                      onClick={() => setIsSent(false)}
                      className="w-full bg-violet-600 hover:bg-violet-700 text-white py-4 rounded-xl font-bold text-[14px] transition-all shadow-lg hover:shadow-violet-200"
                    >
                      Resend Link
                    </button>
                    <Link to="/" className="block text-[13px] font-semibold text-gray-400 hover:text-gray-600 transition">
                      Back to Home
                    </Link>
                  </div>
                </div>
              ) : (
                <>
                  <div className="mb-8">
                    <h1 className="text-[24px] font-black text-gray-900 tracking-tight">
                      Sign up for <span className="text-violet-600">ParkMate</span>
                    </h1>
                    <p className="text-[14px] text-gray-400 mt-2">
                      No passwords, no stress. Enter your email to get started.
                    </p>
                  </div>

                  {error && (
                    <div className="mb-6 px-4 py-3 rounded-xl bg-red-50 border border-red-100 text-red-600 text-[13px] text-center font-medium">
                      {error}
                    </div>
                  )}

                  <form onSubmit={handleSubmit} className="space-y-6">
                    {/* Email Input */}
                    <div className="space-y-2">
                      <label className="block text-[13px] font-bold text-gray-700 ml-1">Email Address</label>
                      <div className="relative group">
                        <FaEnvelope className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 group-focus-within:text-violet-500 transition-colors text-[12px]" />
                        <input
                          type="email"
                          value={email}
                          onChange={(e) => setEmail(e.target.value)}
                          placeholder="name@company.com"
                          required
                          className="w-full pl-11 pr-4 py-4 bg-gray-50 border border-gray-200 rounded-xl focus:bg-white focus:border-violet-500 focus:ring-4 focus:ring-violet-500/10 outline-none transition-all text-[14px]"
                        />
                      </div>
                    </div>

                    <button
                      type="submit"
                      disabled={loading}
                      className="w-full bg-violet-600 hover:bg-violet-700 text-white py-4 rounded-xl font-black text-[15px] transition-all shadow-lg hover:shadow-violet-200 disabled:opacity-60 disabled:cursor-not-allowed flex items-center justify-center gap-3"
                    >
                      {loading ? (
                        <>
                          <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                          <span>Sending link...</span>
                        </>
                      ) : (
                        <>
                          <span>Continue with Magic Link</span>
                          <span className="text-lg">→</span>
                        </>
                      )}
                    </button>
                  </form>

                  <p className="mt-8 text-center text-[13px] text-gray-500 font-medium">
                    Already have an account?{' '}
                    <Link to="/" className="text-violet-600 hover:text-violet-800 font-black transition-all"
                      onClick={() => window.dispatchEvent(new CustomEvent('openLogin'))}>
                      Log In
                    </Link>
                  </p>
                </>
              )}
            </div>
          </div>

          <p className="mt-8 text-center text-[11px] text-gray-400 leading-relaxed px-4">
            By continuing, you agree to ParkMate's <span className="underline cursor-pointer">Terms of Service</span> and <span className="underline cursor-pointer">Privacy Policy</span>.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Signup;
