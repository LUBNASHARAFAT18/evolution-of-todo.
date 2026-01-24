'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';
import { useAuth } from '@/lib/auth.context';
import { useRouter } from 'next/navigation';

interface Todo {
    id: number;
    title: string;
    status: 'Incomplete' | 'Complete';
}

export default function DashboardPage() {
    const [todos, setTodos] = useState<Todo[]>([]);
    const [newTodo, setNewTodo] = useState('');
    const { logout, isAuthenticated } = useAuth();
    const router = useRouter();

    useEffect(() => {
        if (!isAuthenticated) {
            // Wait a bit or let middleware handle it, but here is fine for now
            // router.push('/login'); 
        }
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

    const addTodo = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!newTodo.trim()) return;
        try {
            await api.post('/todos/', { title: newTodo });
            setNewTodo('');
            fetchTodos();
        } catch (error) {
            alert('Failed to add todo');
        }
    };

    const toggleTodo = async (todo: Todo) => {
        try {
            const newStatus = todo.status === 'Incomplete' ? 'Complete' : 'Incomplete';
            await api.patch(`/todos/${todo.id}`, { status: newStatus });
            fetchTodos();
        } catch (error) {
            alert('Failed to update todo');
        }
    };

    const deleteTodo = async (id: number) => {
        try {
            await api.delete(`/todos/${id}`);
            fetchTodos();
        } catch (error) {
            alert('Failed to delete todo');
        }
    };

    return (
        <div className="min-h-screen bg-gray-50">
            <nav className="bg-white shadow p-4 flex justify-between items-center">
                <h1 className="text-xl font-bold">Evolution of Todo</h1>
                <button onClick={logout} className="text-red-500 hover:text-red-700">Logout</button>
            </nav>

            <main className="max-w-2xl mx-auto mt-8 p-4">
                <form onSubmit={addTodo} className="flex gap-2 mb-8">
                    <input
                        type="text"
                        value={newTodo}
                        onChange={(e) => setNewTodo(e.target.value)}
                        placeholder="What needs to be done?"
                        className="flex-1 p-3 border rounded shadow-sm"
                    />
                    <button type="submit" className="px-6 py-3 bg-blue-600 text-white rounded shadow hover:bg-blue-700">
                        Add
                    </button>
                </form>

                <div className="space-y-4">
                    {todos.map((todo) => (
                        <div key={todo.id} className="flex items-center justify-between p-4 bg-white rounded shadow">
                            <div className="flex items-center gap-3">
                                <input
                                    type="checkbox"
                                    checked={todo.status === 'Complete'}
                                    onChange={() => toggleTodo(todo)}
                                    className="w-5 h-5"
                                />
                                <span className={todo.status === 'Complete' ? 'line-through text-gray-400' : ''}>
                                    {todo.title}
                                </span>
                            </div>
                            <button
                                onClick={() => deleteTodo(todo.id)}
                                className="text-red-500 hover:text-red-700 text-sm"
                            >
                                Delete
                            </button>
                        </div>
                    ))}
                    {todos.length === 0 && <p className="text-center text-gray-500">No tasks yet. Add one!</p>}
                </div>
            </main>
        </div>
    );
}
