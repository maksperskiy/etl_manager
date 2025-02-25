import { FileUploader, Form, Select, SelectItem, TextInput, Toggle } from "@carbon/react"
import { ChangeEvent, useState } from "react"

import './DataSourceForm.scss'

type DataSourceType = 'FILE' | 'postgres' | 'mysql' | 's3'

export interface DataSourceFormModel {
  pk?: number
  name?: string
  source_type?: DataSourceType
  upload?: File
  header?: boolean
}

interface DataSourceFormProps {
  model?: DataSourceFormModel
  onChange?: (model: DataSourceFormModel) => void
}

export default function DataSourceForm({ model = {}, onChange }: DataSourceFormProps) {
  const [state, setState] = useState({
    source_type: 'FILE',
    ...model
  } as DataSourceFormModel);

  const HandleChange = <T,>(setter: (event: ChangeEvent<T>) => void) => (event: ChangeEvent<T>) => {
    setter(event);
    onChange?.(state);
  }

  const handleNameChange = HandleChange<HTMLInputElement>(event => {
    setState({ ...state, name: event.target.value });
  });

  const handleSourceTypeChange = HandleChange<HTMLSelectElement>(event => {
    setState({ ...state, source_type: event.target.value as DataSourceType });
  });

  const handleFileChange = HandleChange<HTMLInputElement>(event => {
    setState({
      ...state,
      upload: event.target.files?.[0],
      header: !state.upload?.name.endsWith('.csv')
    });
  });

  const handleHeaderChange = (checked: boolean) => {
    setState({ ...state, header: checked });
    onChange?.(state);
  }

  return <Form className="data-source-form">
    <TextInput id="name" labelText="Name" value={model.name} onChange={handleNameChange} />
    <Select id="sourceType" labelText="Type" value={model.source_type} onChange={handleSourceTypeChange}>
      <SelectItem value="FILE" text="File" />
      <SelectItem value="postgres" text="PostgreSQL" />
      <SelectItem value="mysql" text="MySQL" />
      <SelectItem value="s3" text="S3 Bucket" />
    </Select>
    {
      state.source_type === 'FILE' &&
      <>
        <FileUploader
          filenameStatus="edit"
          name="upload"
          accept={['.csv', '.xls', '.xlsx']}
          labelTitle="Upload file"
          size="md"
          labelDescription="Max file size is 50 MB. Only .csv, .xls, xlsx files are supported."
          onChange={handleFileChange}
        />
        {
          state.upload?.name.endsWith('.csv') &&
          <Toggle id="header" labelA="exclude headers" labelB="include headers" onToggle={handleHeaderChange} />
        }
      </>
    }
  </Form>
}
