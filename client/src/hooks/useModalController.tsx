import { useState } from 'react'

type ModalEventCallback<T = unknown> = (buffer?: T) => void

export default function useModal<T>(persistant: boolean = false) {
  const [opened, setOpened] = useState(false)

  const openCallbacks: ModalEventCallback<T>[] = []
  const closeCallbacks: ModalEventCallback[] = []

  const open = (buffer?: T) => {
    openCallbacks.forEach(callback => callback(buffer))
    setOpened(true)
  }

  const close = () => {
    closeCallbacks.forEach(callback => callback())
    setOpened(false)
  }

  const backdrop = () => {
    if (!persistant) close()
  }

  const onOpen = (callback: ModalEventCallback<T>) => {
    openCallbacks.push(callback)
  }

  const onClose = (callback: ModalEventCallback) => {
    closeCallbacks.push(callback)
  }

  return {
    opened,
    open,
    close,
    backdrop,
    onOpen,
    onClose
  }
}
