import './DataSources.scss';

import { Add } from '@carbon/icons-react';
import { Button, Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@carbon/react';
import { useEffect, useState } from 'react';
import dataSourceService from '../../services/data-source';
import useModalStore from '../../stores/modal';
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

  const handleAddClick = () => {
    open({
      component: <Button />,
      data: {}
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
