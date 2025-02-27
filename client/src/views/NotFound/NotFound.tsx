import { Home } from '@carbon/icons-react'
import { Button } from '@carbon/react'
import { Link } from 'react-router'
import './NotFound.scss'

export default function NotFound() {
  return <div className="etlm-not-found">
    <h1>404</h1>
    <h2>Page Not Found</h2>
    <Link className="etlm-not-found__link" to="/"><Button kind="tertiary" renderIcon={Home}>Return to main page</ Button> </Link>
  </div>
}
