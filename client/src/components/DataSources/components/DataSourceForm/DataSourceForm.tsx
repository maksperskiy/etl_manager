import { Select, SelectItem, TextInput } from "@carbon/react"

import { ChangeEvent, useRef } from "react"
import './DataSourceForm.scss'

type DataSourceType = 'file' | 'postgres' | 'mysql' | 's3'

export interface DataSourceFormModel {
  name?: string
  source_type?: DataSourceType
}

interface DataSourceFormProps {
  model?: DataSourceFormModel
  onChange?: (model: DataSourceFormModel) => void
}

export default function DataSourcetForm({ model = {}, onChange }: DataSourceFormProps) {
  const state = useRef(model);

  const HandleChange = <T,>(setter: (event: ChangeEvent<T>) => void) => (event: ChangeEvent<T>) => {
    setter(event);
    onChange?.(state.current);
  }

  const handleNameChange = HandleChange<HTMLInputElement>(event => {
    state.current.name = event.target.value;
  });

  const handleSourceTypeChange = HandleChange<HTMLSelectElement>(event => {
    state.current.source_type = event.target.value as DataSourceType;
  });

  return <form className="data-source-form">
    <TextInput id="name" labelText="Name" value={model.name} onChange={handleNameChange} />
    <Select id="sourceType" labelText="Type" value={model.source_type} onChange={handleSourceTypeChange}>
      <SelectItem value="file" text="File" />
      <SelectItem value="postgres" text="PostgreSQL" />
      <SelectItem value="mysql" text="MySQL" />
      <SelectItem value="s3" text="S3 Bucket" />
    </Select>
  </form>
}
