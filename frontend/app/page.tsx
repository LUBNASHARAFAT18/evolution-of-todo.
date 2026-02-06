'use client';

import { useState } from 'react';
import api from '@/lib/api';
import { useAuth } from '@/lib/auth.context';
import Link from 'next/link';

export default function SignupPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const { login } = useAuth();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const res = await api.post('/auth/signup', { email, password });
            login(res.data.access_token);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Signup failed');
        }
    };

    return (
        <div className="flex min-h-screen items-center justify-center bg-gray-100">
            <div className="w-full max-w-md p-8 space-y-6 bg-white rounded shadow-md">
                <h2 className="text-2xl font-bold text-center">Sign Up</h2>
                {error && <p className="text-red-500 text-center">{error}</p>}
                <form onSubmit={handleSubmit} className="space-y-4">
                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className="w-full p-2 border rounded"
                        required
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="w-full p-2 border rounded"
                        required
                    />
                    <button type="submit" className="w-full p-2 text-white bg-blue-600 rounded hover:bg-blue-700">
                        Create Account
                    </button>
                </form>
                <p className="text-center">
                    Already have an account? <Link href="/login" className="text-blue-500">Log in</Link>
                </p>
            </div>
        </div>
    );
}
