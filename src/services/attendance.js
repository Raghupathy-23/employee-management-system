import api from "./api";

export async function listAttendance(params = {}) {
  const response = await api.get("/attendance", { params });
  return response.data;
}

export async function getAttendance(id) {
  const response = await api.get(`/attendance/${id}`);
  return response.data;
}

export async function createAttendance(data) {
  const response = await api.post("/attendance", data);
  return response.data;
}

export async function updateAttendance(id, data) {
  const response = await api.patch(`/attendance/${id}`, data);
  return response.data;
}

export async function deleteAttendance(id) {
  await api.delete(`/attendance/${id}`);
}
