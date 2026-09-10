import api from "./api";

export async function listRoles() {
  const response = await api.get("/roles");
  return response.data;
}

export async function getRole(id) {
  const response = await api.get(`/roles/${id}`);
  return response.data;
}

export async function createRole(data) {
  const response = await api.post("/roles", data);
  return response.data;
}

export async function updateRole(id, data) {
  const response = await api.patch(`/roles/${id}`, data);
  return response.data;
}

export async function deleteRole(id) {
  await api.delete(`/roles/${id}`);
}
