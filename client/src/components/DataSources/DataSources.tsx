import './DataSources.scss';

import { Add } from '@carbon/icons-react';
import { Button, Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@carbon/react';
import { useEffect, useRef, useState } from 'react';
import dataSourceService from '../../services/data-source';
import useModalStore from '../../stores/modal';
import DataSourceForm, { DataSourceFormModel } from './components/DataSourceForm/DataSourceForm';
import DateRenderer from './renderers/DateRenderer';
import { ColumnDef, DataSource } from './types';

export default function DataSources() {
  const columnDefs: ColumnDef[] = [
    {
      key: 'name',
      label: 'Name',
    },
    {
      key: 'created_at',
      label: 'Loaded',
      renderer: DateRenderer
    },
    {
      key: 'last_used',
      label: 'Last Used',
    },
    {
      key: 'actions',
      label: null,
    }
  ];

  const { open } = useModalStore();
  const createModel = useRef({});

  const handleAddClick = () => {
    open({
      title: 'Add Data Source',
      component: <DataSourceForm onChange={(model: DataSourceFormModel) => { createModel.current = model; }} />,
      actions: [
        {
          key: 'close',
          label: 'Close',
          kind: 'ghost',
          close: true
        },
        {
          key: 'save',
          label: 'Save',
          kind: 'primary',
          close: true,
          callback: () => { console.log(createModel.current) }
        }
      ],
      persistent: true
    });
  }

  const [dataSources, setDataSources] = useState<DataSource[]>([]);

  useEffect(() => {
    (async () => {
      const res = await dataSourceService.getDataSources();
      setDataSources(await res.json());
    })();
  }, [])

  return <div className="etlm-data-sources">
    <Button className="etlm-data-sources__add" renderIcon={Add} onClick={handleAddClick}>Add New Data Source</Button>
    <Table aria-label="sample table">
      <TableHead>
        <TableRow>
          {columnDefs.map(def => <TableHeader key={def.key}>{ def.label }</TableHeader>)}
        </TableRow>
      </TableHead>
      <TableBody>
        {dataSources.map(src => <TableRow key={src.name}>
          {columnDefs.map(def => <TableCell  key={def.key}>
            { src[def.key as keyof DataSource] }
          </TableCell>)}
        </TableRow>)}
      </TableBody>
    </Table>
  </div>
}
