import { create } from "zustand";

export interface User {
  user_id: number
  username: string
  email: string
}

interface UserStoreState {
  user: User | null
}

interface UserStore extends UserStoreState {
  setUser: (user: User) => void
}

const useUserStore = create<UserStore>((set) => ({
  user: null,
  setUser: (user: User) => set(() => ({ user })),
}))

export default useUserStore
