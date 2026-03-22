import { create } from 'zustand'

interface ProjectStore {
  currentProjectId: string | null
  selectedModules: string[]
  setProjectId: (id: string) => void
  toggleModule: (moduleId: string) => void
  clearModules: () => void
}

export const useProjectStore = create<ProjectStore>((set) => ({
  currentProjectId: null,
  selectedModules: [],
  setProjectId: (id) => set({ currentProjectId: id }),
  toggleModule: (moduleId) =>
    set((state) => ({
      selectedModules: state.selectedModules.includes(moduleId)
        ? state.selectedModules.filter((m) => m !== moduleId)
        : [...state.selectedModules, moduleId],
    })),
  clearModules: () => set({ selectedModules: [] }),
}))
