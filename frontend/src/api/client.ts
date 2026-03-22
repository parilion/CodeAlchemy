import axios from 'axios'

const api = axios.create({ baseURL: 'http://localhost:8000' })

export const uploadProject = (file: File) => {
  const form = new FormData()
  form.append('file', file)
  return api.post<{ project_id: string }>('/api/enhance/upload', form)
}

export const enhanceProject = (projectId: string, modules: string[]) =>
  api.post<{
    project_id: string
    download_url: string
    injected_modules: string[]
    analysis: Record<string, unknown>
  }>('/api/enhance/', { project_id: projectId, modules })

export const generateFromTemplate = (requirement: string, modules: string[]) =>
  api.post<{
    project_id: string
    template_used: string
    download_url: string
  }>('/api/templates/generate', { requirement, modules })

export const listProjects = () =>
  api.get<{ project_id: string }[]>('/api/projects/')
