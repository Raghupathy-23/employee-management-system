import api from "./api";

export async function login(email, password) {
  const body = new URLSearchParams();
  body.append("username", email);
  body.append("password", password);

  const response = await api.post("/auth/login", body, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });

  localStorage.setItem("access_token", response.data.access_token);
  return response.data;
}

export async function getCurrentUser() {
  const response = await api.get("/auth/me");
  localStorage.setItem("current_user", JSON.stringify(response.data));
  return response.data;
}

export function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("current_user");
}