import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Container } from '@mui/system';
import {
  Card,
  CardContent,
  CardActions,
  List,
  ListItem,
  Typography,
} from '@mui/material';
import NavBar from '../components/NavBar';

function AccountsScreen() {
  const [accounts, setAccounts] = useState('');

  useEffect(() => {
    async function getAccounts() {
      const { access } = JSON.parse(localStorage.getItem('userInfo'));
      const config = {
        headers: {
          Authorization: `Bearer ${access}`,
        },
      };
      const { data } = await axios.get('/api/users/accounts/', config);
      setAccounts(data.data.accounts);
    }

    getAccounts();
  }, []);

  return (
    <Container>
      <NavBar />
      {accounts.length < 1 ? (
        <h2>No accounts available</h2>
      ) : (
        <List>
          {accounts.map((a) => (
            <ListItem key={a.account_number}>
              <Card>
                <h3>Account Number</h3>
                <CardContent>
                  <Typography gutterBottom variant="h5" component="div">
                    {a.account_number}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Current Balance ${a.current_balance.toFixed(2)}
                  </Typography>
                </CardContent>
                <CardActions>
                  <Link to={`/transactions/${a.account_number}`}>
                    View Transactions
                  </Link>
                </CardActions>
              </Card>
            </ListItem>
          ))}
        </List>
      )}
    </Container>
  );
}

export default AccountsScreen;
