import { useState } from "react";

export default function useModal(persistant: boolean = false) {
  const [opened, setOpened] = useState(false);

  const open = () => {
    setOpened(true);
  }

  const close = () => {
    setOpened(false);
  }

  const backdrop = () => {
    if (!persistant) setOpened(false);
  }

  return {
    opened,
    open,
    close,
    backdrop
  }
}
