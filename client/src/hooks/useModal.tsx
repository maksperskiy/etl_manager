import { ReactNode, useState } from "react";

export default function useModal(component: ReactNode, actions: string[] = [], initialData = {}) {
  const [data, setData] = useState(initialData);
}
