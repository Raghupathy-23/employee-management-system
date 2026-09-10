import api from "./api";

export async function listLeaves(params = {}) {
  const response = await api.get("/leaves", { params });
  return response.data;
}

export async function getLeave(id) {
  const response = await api.get(`/leaves/${id}`);
  return response.data;
}

export async function createLeave(data) {
  const response = await api.post("/leaves", data);
  return response.data;
}

export async function updateLeave(id, data) {
  const response = await api.patch(`/leaves/${id}`, data);
  return response.data;
}

export async function deleteLeave(id) {
  await api.delete(`/leaves/${id}`);
}

export async function approveLeave(id, approval_comment = "") {
  const response = await api.patch(`/leaves/${id}/approve`, { approval_comment });
  return response.data;
}

export async function rejectLeave(id, approval_comment = "") {
  const response = await api.patch(`/leaves/${id}/reject`, { approval_comment });
  return response.data;
}

export async function getLeaveBalance(employeeId) {
  const response = await api.get(`/employees/${employeeId}/leave-balance`);
  return response.data;
}
