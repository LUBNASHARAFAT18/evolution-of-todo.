'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';
import { useAuth } from '@/lib/auth.context';
import { useRouter } from 'next/navigation';
import ChatInterface from '@/components/ChatInterface';

interface Todo {
    id: number;
    title: string;
    description?: string;
    priority: 'Low' | 'Medium' | 'High';
    status: 'Incomplete' | 'Complete';
    created_at: string;
}

export default function DashboardPage() {
    const [todos, setTodos] = useState<Todo[]>([]);
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [priority, setPriority] = useState<'Low' | 'Medium' | 'High'>('Medium');
    const [editingTodo, setEditingTodo] = useState<Todo | null>(null);
    const { logout, isAuthenticated } = useAuth();
    const router = useRouter();

    useEffect(() => {
        fetchTodos();
    }, []);

    const fetchTodos = async () => {
        try {
            const res = await api.get('/todos/');
            setTodos(res.data);
        } catch (error) {
            console.error('Failed to fetch todos', error);
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!title.trim()) return;

        try {
            if (editingTodo) {
                await api.patch(`/todos/${editingTodo.id}`, {
                    title,
                    description,
                    priority
                });
                setEditingTodo(null);
            } else {
                await api.post('/todos/', {
                    title,
                    description,
                    priority
                });
            }
            setTitle('');
            setDescription('');
            setPriority('Medium');
            fetchTodos();
        } catch (error) {
            alert('Operation failed');
        }
    };

    const handleEdit = (todo: Todo) => {
        setEditingTodo(todo);
        setTitle(todo.title);
        setDescription(todo.description || '');
        setPriority(todo.priority);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    const toggleTodo = async (todo: Todo) => {
        try {
            const newStatus = todo.status === 'Incomplete' ? 'Complete' : 'Incomplete';
            await api.patch(`/todos/${todo.id}`, { status: newStatus });
            fetchTodos();
        } catch (error) {
            alert('Failed to update status');
        }
    };

    const deleteTodo = async (id: number) => {
        if (!confirm('Are you sure you want to delete this task?')) return;
        try {
            await api.delete(`/todos/${id}`);
            fetchTodos();
        } catch (error) {
            alert('Failed to delete todo');
        }
    };

    return (
        <div className="min-h-screen bg-slate-50 text-slate-900 font-sans">
            {/* Header */}
            <nav className="bg-white/80 backdrop-blur-md sticky top-0 z-40 border-b border-slate-200">
                <div className="max-w-5xl mx-auto px-6 h-16 flex justify-between items-center">
                    <div className="flex items-center gap-2">
                        <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white font-bold shadow-lg shadow-blue-200">
                            ✓
                        </div>
                        <h1 className="text-xl font-extrabold tracking-tight bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                            Todo Evolution
                        </h1>
                    </div>
                    <button
                        onClick={logout}
                        className="text-sm font-medium px-4 py-2 text-slate-600 hover:bg-slate-100 rounded-full transition-colors"
                    >
                        Sign Out
                    </button>
                </div>
            </nav>

            <main className="max-w-3xl mx-auto py-10 px-6">
                {/* Form Section */}
                <section className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 mb-10">
                    <h2 className="text-lg font-bold mb-4 flex items-center gap-2">
                        {editingTodo ? '📝 Edit Task' : '✨ Create New Task'}
                    </h2>
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div className="md:col-span-2">
                                <label className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1 block">Title</label>
                                <input
                                    type="text"
                                    value={title}
                                    onChange={(e) => setTitle(e.target.value)}
                                    placeholder="Add a task title..."
                                    className="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all"
                                    required
                                />
                            </div>
                            <div>
                                <label className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1 block">Priority</label>
                                <select
                                    value={priority}
                                    onChange={(e) => setPriority(e.target.value as any)}
                                    className="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 appearance-none bg-no-repeat bg-[right_1rem_center] bg-[length:1em_1em]"
                                    style={{ backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%2364748b'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E")` }}
                                >
                                    <option value="Low">Low Priority</option>
                                    <option value="Medium">Medium Priority</option>
                                    <option value="High">High Priority</option>
                                </select>
                            </div>
                            <div className="md:col-span-2">
                                <label className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1 block">Description (Optional)</label>
                                <textarea
                                    value={description}
                                    onChange={(e) => setDescription(e.target.value)}
                                    placeholder="Add more details about this task..."
                                    rows={2}
                                    className="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all resize-none"
                                />
                            </div>
                        </div>
                        <div className="flex gap-2">
                            <button
                                type="submit"
                                className="flex-1 py-3 bg-blue-600 text-white font-bold rounded-xl shadow-lg shadow-blue-200 hover:bg-blue-700 active:scale-[0.98] transition-all"
                            >
                                {editingTodo ? 'Update Task' : 'Add Task'}
                            </button>
                            {editingTodo && (
                                <button
                                    type="button"
                                    onClick={() => {
                                        setEditingTodo(null);
                                        setTitle('');
                                        setDescription('');
                                        setPriority('Medium');
                                    }}
                                    className="px-6 py-3 bg-slate-100 text-slate-600 font-bold rounded-xl hover:bg-slate-200 transition-all"
                                >
                                    Cancel
                                </button>
                            )}
                        </div>
                    </form>
                </section>

                {/* List Section */}
                <div className="space-y-4 pb-20">
                    <div className="flex justify-between items-center mb-6">
                        <h3 className="text-xl font-extrabold text-slate-800">Your Tasks</h3>
                        <span className="text-xs font-bold bg-slate-200 text-slate-600 px-3 py-1 rounded-full">
                            {todos.length} Total
                        </span>
                    </div>

                    {todos.length === 0 ? (
                        <div className="text-center py-20 bg-white rounded-2xl border-2 border-dashed border-slate-200">
                            <div className="text-4xl mb-4">🎈</div>
                            <p className="text-slate-500 font-medium">All clear! No tasks found.</p>
                        </div>
                    ) : (
                        todos.map((todo) => {
                            const priorityColors = {
                                High: 'bg-rose-100 text-rose-600',
                                Medium: 'bg-amber-100 text-amber-600',
                                Low: 'bg-emerald-100 text-emerald-600'
                            };

                            return (
                                <div
                                    key={todo.id}
                                    className={`group flex items-start gap-4 p-5 bg-white rounded-2xl shadow-sm border transition-all hover:shadow-md hover:border-blue-200 ${todo.status === 'Complete' ? 'opacity-75 grayscale-[0.5]' : ''
                                        }`}
                                >
                                    <div className="pt-1">
                                        <button
                                            onClick={() => toggleTodo(todo)}
                                            className={`w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all ${todo.status === 'Complete'
                                                    ? 'bg-blue-600 border-blue-600 text-white'
                                                    : 'border-slate-300 hover:border-blue-500 bg-white'
                                                }`}
                                        >
                                            {todo.status === 'Complete' && <span className="text-[10px] font-bold">✓</span>}
                                        </button>
                                    </div>

                                    <div className="flex-1 min-w-0">
                                        <div className="flex items-center gap-2 mb-1">
                                            <span className={`text-[10px] font-bold uppercase tracking-widest px-2 py-0.5 rounded-md ${priorityColors[todo.priority]}`}>
                                                {todo.priority}
                                            </span>
                                        </div>
                                        <h4 className={`font-bold text-lg truncate ${todo.status === 'Complete' ? 'line-through text-slate-400' : 'text-slate-800'
                                            }`}>
                                            {todo.title}
                                        </h4>
                                        {todo.description && (
                                            <p className="mt-1 text-sm text-slate-500 line-clamp-2">
                                                {todo.description}
                                            </p>
                                        )}
                                        <div className="mt-2 text-[10px] text-slate-400 font-medium uppercase tracking-tighter">
                                            Added {new Date(todo.created_at).toLocaleDateString()}
                                        </div>
                                    </div>

                                    <div className="flex flex-col gap-2 transition-opacity md:opacity-0 group-hover:opacity-100">
                                        <button
                                            onClick={() => handleEdit(todo)}
                                            className="p-2 text-slate-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all"
                                            title="Edit"
                                        >
                                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                            </svg>
                                        </button>
                                        <button
                                            onClick={() => deleteTodo(todo.id)}
                                            className="p-2 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-all"
                                            title="Delete"
                                        >
                                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                            </svg>
                                        </button>
                                    </div>
                                </div>
                            );
                        })
                    )}
                </div>
            </main>

            <ChatInterface onAction={fetchTodos} />
        </div>
    );
}
