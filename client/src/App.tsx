
import { Tab, TabList, TabPanels, Tabs } from '@carbon/react'
import { ReactNode } from 'react'
import './App.scss'
import PageWrapper from './components/common/PageWrapper'
import DataSources from './components/DataSources/DataSources'
import Router from './Router'

interface TabConfig {
  slug: string,
  title: string,
  component: ReactNode
}

function App() {
  const config: TabConfig[] = [
    {
      slug: 'data-sources',
      title: 'Data Sources',
      component: <DataSources />
    },
    {
      slug: 'data-builder',
      title: 'Data Builder',
      component: <div />
    },
    {
      slug: 'manager',
      title: 'Manager',
      component: <div />
    },
  ];

  return <Router />

  return <Tabs>
    <TabList contained>
      {config.map(item => <Tab key={item.slug}>{ item.title }</Tab>)}
    </TabList>
    <TabPanels>
      {config.map(item => <PageWrapper key={item.slug} title={item.title}>
        {item.component}
      </PageWrapper>)}
    </TabPanels>
  </Tabs>
}

export default App
