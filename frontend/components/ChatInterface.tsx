'use client';

import { useState, useRef, useEffect } from 'react';
import api from '@/lib/api';

export default function ChatInterface({ onAction }: { onAction?: () => void }) {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState<{ role: 'user' | 'agent', text: string }[]>([
        { role: 'agent', text: 'Hello! I am your Todo AI. How can I help you today?' }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim() || isLoading) return;

        const userMsg = input;
        setInput('');
        setMessages(prev => [...prev, { role: 'user', text: userMsg }]);
        setIsLoading(true);

        try {
            const res = await api.post('/chat', { message: userMsg });
            setMessages(prev => [...prev, { role: 'agent', text: res.data.reply }]);
            if (res.data.refresh && onAction) {
                onAction();
            }
        } catch (error) {
            setMessages(prev => [...prev, { role: 'agent', text: 'Sorry, I encountered an error. Please try again.' }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="fixed bottom-6 right-6 z-50">
            {isOpen ? (
                <div className="bg-white w-80 h-96 rounded-xl shadow-2xl border flex flex-col overflow-hidden animate-in slide-in-from-bottom-4">
                    <div className="p-4 bg-blue-600 text-white flex justify-between items-center">
                        <span className="font-bold">Todo AI Agent</span>
                        <button onClick={() => setIsOpen(false)} className="hover:opacity-75">✕</button>
                    </div>

                    <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
                        {messages.map((m, i) => (
                            <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                <div className={`max-w-[80%] p-3 rounded-2xl text-sm ${m.role === 'user' ? 'bg-blue-600 text-white rounded-tr-none' : 'bg-white border rounded-tl-none shadow-sm'
                                    }`}>
                                    {m.text}
                                </div>
                            </div>
                        ))}
                        {isLoading && (
                            <div className="flex justify-start">
                                <div className="bg-white border p-3 rounded-2xl animate-pulse text-xs text-gray-400">Thinking...</div>
                            </div>
                        )}
                    </div>

                    <div className="p-3 border-t bg-white flex gap-2">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                            placeholder="Ask me anything..."
                            className="flex-1 p-2 text-sm border rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-500"
                        />
                        <button
                            onClick={handleSend}
                            disabled={isLoading}
                            className="p-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                        >
                            →
                        </button>
                    </div>
                </div>
            ) : (
                <button
                    onClick={() => setIsOpen(true)}
                    className="w-14 h-14 bg-blue-600 text-white rounded-full shadow-lg flex items-center justify-center hover:scale-105 transition-transform active:scale-95"
                >
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                    </svg>
                </button>
            )}
        </div>
    );
}
