import { Logout, Settings } from '@carbon/icons-react';
import { Button, MenuButton, MenuItem } from '@carbon/react';
import { Link, useNavigate } from 'react-router';
import commonService from '../../../services/common';
import useUserStore from '../../../stores/user';
import './Header.scss';

export default function Header() {
  const navigate = useNavigate();
  const { user } = useUserStore(store => store);

  const handleSettingsClick = () => {
    navigate('/settings');
  }

  const handleLogoutClick = async () => {
    await commonService.logout()
    navigate('/login')
  }

  return <header className="etlm-header">
    <Link to="/data-sources"><Button>Data Sources</Button></Link>
    <Link to="/data-builder"><Button>Data Builder</Button></Link>
    <Link to="/manager"><Button>Manager</Button></Link>
    <MenuButton className="etlm-header__menu-button" label={user?.username} menuAlignment="bottom">
      <MenuItem label="Settings" renderIcon={Settings} onClick={handleSettingsClick}></MenuItem>
      <MenuItem label="Logout" renderIcon={Logout} onClick={handleLogoutClick}></MenuItem>
    </MenuButton>
  </header>
}
