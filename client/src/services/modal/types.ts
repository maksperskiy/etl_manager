import { ReactNode } from "react";

export interface Modal<T = { [key: string]: unknown }> {
  component: (props: T) => ReactNode,
  props: T
}
