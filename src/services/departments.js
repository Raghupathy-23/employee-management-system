import api from "./api";

export async function listDepartments(params = {}) {
  const response = await api.get("/departments", { params });
  return response.data;
}

export async function createDepartment(data) {
  const response = await api.post("/departments", data);
  return response.data;
}

export async function updateDepartment(id, data) {
  const response = await api.patch(`/departments/${id}`, data);
  return response.data;
}

export async function deleteDepartment(id) {
  await api.delete(`/departments/${id}`);
}
