import { Heading, TabPanel } from '@carbon/react';
import { ReactNode } from "react";

import "./PageWrapper.scss";

interface PageWrapperProps {
  children: ReactNode
  title: string
}

export default function PageWrapper(props: PageWrapperProps) {
  return <TabPanel className="etlm-page-wrapper">
    <Heading className="etlm-page-wrapper__title">{ props.title }</Heading>
    <div className="etlm-page-wrapper__content">{ props.children }</div>
  </TabPanel>
}
