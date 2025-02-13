import { ButtonKind } from '@carbon/react';
import { ReactElement } from 'react';
import { create } from 'zustand';

export type ModalActionCallback = (...args: unknown[]) => void;

export interface ModalAction {
  key: string
  label: string
  kind: ButtonKind
  callback?: ModalActionCallback
  close: boolean
}

export interface Modal {
  component: ReactElement
  persistent?: boolean
  actions: ModalAction[]
}

export interface IndexedModal extends Modal {
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
