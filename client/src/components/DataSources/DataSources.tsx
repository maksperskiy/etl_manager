import './DataSources.scss';

import { Add } from '@carbon/icons-react';
import { Button, Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@carbon/react';
import { useEffect, useState } from 'react';
import dataSourceService from '../../services/data-source';
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

  const [dataSources, setDataSources] = useState<DataSource[]>([]);

  useEffect(() => {
     dataSourceService.getDataSources().then(r => r.json()).then((data: DataSource[]) => setDataSources(data))
  }, [])

  return <div className="etlm-data-sources">
    <Button className="etlm-data-sources__add" renderIcon={Add}>Add New Data Source</Button>
    <Table aria-label="sample table">
      <TableHead>
        <TableRow>
          {columnDefs.map(def => <TableHeader key={def.key}>{ def.label }</TableHeader>)}
        </TableRow>
      </TableHead>
      <TableBody>
        {dataSources.map(src => <TableRow key={src.name}>
          {columnDefs.map(def => <TableCell  key={def.key}>
            { src[def.key as keyof DataSource]

            }
          </TableCell>)}
        </TableRow>)}
      </TableBody>
    </Table>
  </div>
}
