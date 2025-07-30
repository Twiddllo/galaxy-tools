const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export async function login(email: string, password: string) {
  const res = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) throw new Error((await res.json()).detail || 'Login failed');
  return res.json();
}

export async function register(data: any) {
  const res = await fetch(`${API_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username: data.username,
      first_name: data.firstName,
      last_name: data.lastName,
      email: data.email,
      phone: data.phone,
      password: data.password,
      confirm_password: data.confirmPassword,
    }),
  });
  if (!res.ok) throw new Error((await res.json()).detail || 'Registration failed');
  return res.json();
}

export async function forgotPassword(email: string) {
  const res = await fetch(`${API_URL}/auth/password-reset-request`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email }),
  });
  if (!res.ok) throw new Error((await res.json()).detail || 'Failed to send reset link');
  return res.json();
} 