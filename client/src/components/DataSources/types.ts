import { ReactNode } from "react"

export interface DataSource {
  name: string,
  type: string,
  dateLoaded: number,
  dateUsed: number,
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
