import React from 'react';
import { Link } from 'react-router-dom';
import { List, ListItem } from '@mui/material';

function NavBar() {
  const { username } = JSON.parse(localStorage.getItem('userInfo'));
  return (
    <nav>
      <h1>Welcome, {username}!</h1>
      <List>
        <ListItem>
          <Link to="/accounts" underline="hover">
            Accounts
          </Link>
        </ListItem>
        <ListItem>
          <Link to="/transactions" underline="hover">
            Transactions
          </Link>
        </ListItem>
      </List>
    </nav>
  );
}

export default NavBar;
