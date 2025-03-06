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

const getUserFromLocalStorage = () => ((username: string | null) => username
  ? ({
    username,
    email: localStorage.getItem('user.email'),
    user_id: localStorage.getItem('user.user_id')
  } as unknown as User)
  : null)(localStorage.getItem('user.username'));

const useUserStore = create<UserStore>((set) => ({
  user: getUserFromLocalStorage(),
  setUser: (user: User) => set(() => ({ user })),
}))

export default useUserStore
