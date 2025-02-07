import { ReactElement } from 'react';
import { create } from 'zustand';

export interface Modal<T = { [key: string]: unknown }> {
  component: ReactElement,
  data: T
}

interface IndexedModal<T = { [key: string]: unknown }> extends Modal<T> {
  id: string
}

interface ModalStoreState {
  modals: IndexedModal[]
}

interface ModalStore extends ModalStoreState {
  open: (modal: Modal) => void
  close: (id: string) => void
}

const useModalStore = create<ModalStore>(
  (set) => ({
    modals: [],
    open: (modal: Modal) => set((state: ModalStoreState) => ({ modals: [...state.modals, { ...modal, id: '1' }] })),
    close: (id: string) => set((state: ModalStoreState) => ({ modals: state.modals.filter(modal => modal.id !== id) })),
  }),
);

export default useModalStore;
