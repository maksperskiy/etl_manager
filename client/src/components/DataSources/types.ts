import { ReactNode } from "react"

export interface DataSource {
  name: string
  author: number
  file_ext: string
  source_type: string
  created_at: number
  last_used: number
}

export interface RendererProps {
  dataSource: DataSource,
  key: string
}

export interface ColumnDef {
  key: string,
  label: string | null,
  renderer?: (props: RendererProps) => ReactNode
}
