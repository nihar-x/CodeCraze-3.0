import { useEffect, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { verifyMagicLink } from "../services/api";
import { FaCar, FaSpinner, FaExclamationCircle } from "react-icons/fa";

const MagicLogin = () => {
    const [searchParams] = useSearchParams();
    const [status, setStatus] = useState("verifying"); // verifying, success, error
    const [error, setError] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
        const token = searchParams.get("token");

        if (!token) {
            setStatus("error");
            setError("No login token found. Please request a new magic link.");
            return;
        }

        const verify = async () => {
            try {
                const res = await verifyMagicLink(token);

                // Log user in
                localStorage.setItem("parkmate_user", JSON.stringify(res.user));

                // If your backend returns a token, store it
                if (res.token) {
                    localStorage.setItem("parkmate_token", res.token);
                }

                setStatus("success");
                window.dispatchEvent(new CustomEvent("userLoggedIn"));

                // Brief delay then redirect to dashboard
                setTimeout(() => navigate("/dashboard"), 1500);
            } catch (err) {
                setStatus("error");
                setError(err.message || "The link is invalid or has expired. Please request a new one.");
            }
        };

        verify();
    }, [searchParams, navigate]);

    return (
        <div className="min-h-screen flex items-center justify-center bg-[#f4f3fb] px-5 py-8">
            <div className="w-full max-w-[400px] bg-white rounded-3xl shadow-xl border border-gray-100 p-10 text-center relative overflow-hidden">
                {/* Decorative background element */}
                <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-violet-600 via-indigo-600 to-blue-600" />

                <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-violet-600 to-indigo-700 flex items-center justify-center text-white text-2xl shadow-lg shadow-indigo-200 mx-auto mb-8">
                    <FaCar />
                </div>

                {status === "verifying" && (
                    <div className="space-y-6">
                        <h1 className="text-[24px] font-black text-gray-900 tracking-tight">
                            Verifying your identity
                        </h1>
                        <p className="text-[14px] text-gray-500 leading-relaxed">
                            We're securely signing you into <span className="font-bold text-gray-900">ParkMate</span>.
                            This will only take a moment.
                        </p>
                        <div className="flex flex-col items-center gap-4 pt-4">
                            <div className="flex gap-1.5">
                                {[0, 1, 2].map((i) => (
                                    <div
                                        key={i}
                                        className="w-2.5 h-2.5 rounded-full bg-violet-600 animate-pulse"
                                        style={{ animationDelay: `${i * 0.2}s` }}
                                    />
                                ))}
                            </div>
                            <span className="text-[11px] font-bold text-violet-600 uppercase tracking-widest">Secure Handshake</span>
                        </div>
                    </div>
                )}

                {status === "success" && (
                    <div className="space-y-6 animate-fade-up">
                        <h1 className="text-[24px] font-black text-gray-900 tracking-tight">
                            Welcome back!
                        </h1>
                        <div className="flex flex-col items-center gap-4">
                            <div className="w-12 h-12 rounded-full bg-emerald-100 flex items-center justify-center text-emerald-600 text-xl font-bold">
                                ✓
                            </div>
                            <p className="text-[14px] text-emerald-600 font-bold">
                                Successfully authenticated.
                            </p>
                            <p className="text-[12px] text-gray-400">
                                Taking you to your dashboard...
                            </p>
                        </div>
                    </div>
                )}

                {status === "error" && (
                    <div className="space-y-6 animate-fade-up">
                        <div className="w-16 h-16 rounded-2xl bg-red-50 flex items-center justify-center text-red-500 text-2xl mx-auto mb-2">
                            <FaExclamationCircle />
                        </div>
                        <h1 className="text-[24px] font-black tracking-tight text-red-600">
                            Link Expired
                        </h1>
                        <p className="text-[14px] text-gray-500 leading-relaxed">
                            {error}
                        </p>
                        <button
                            onClick={() => navigate("/")}
                            className="mt-4 w-full bg-gray-900 hover:bg-black text-white py-4 px-6 rounded-2xl font-bold text-[14px] transition-all shadow-lg hover:shadow-xl active:scale-[0.98]"
                        >
                            Back to Homepage
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default MagicLogin;
