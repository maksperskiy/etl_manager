import { ReactNode, useState } from "react";
import { ModalAction } from "../stores/modal";

export default function useModal<T = string>(component: ReactNode, actions: ModalAction[] = [], initialData = {}) {
  const [data, setData] = useState(initialData);

  const modal = {

  }
}
