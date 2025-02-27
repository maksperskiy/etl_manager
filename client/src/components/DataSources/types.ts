import { ReactNode } from "react"

export interface DataSource {
  pk: number
  name: string
  author: number
  file_ext: string
  source_type: string
  created_at: number
  last_used: number
}

export interface RendererProps {
  dataSource: DataSource
  key: string
}

export type ExtendedRendererProps<T> = RendererProps & T;

export type Renderer<T> = (props: T) => ReactNode

export interface ColumnDef<T> {
  key: string
  label: string | null
  renderer?: Renderer<ExtendedRendererProps<T>>
  props?: T
  class?: string
}
