import api from "./api";

export async function listEmployees(params = {}) {
  const response = await api.get("/employees", { params });
  return response.data;
}

export async function createEmployee(data) {
  const response = await api.post("/employees", data);
  return response.data;
}

export async function updateEmployee(id, data) {
  const response = await api.patch(`/employees/${id}`, data);
  return response.data;
}

export async function deleteEmployee(id) {
  await api.delete(`/employees/${id}`);
}
