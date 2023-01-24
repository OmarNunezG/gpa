import axios from 'axios';
import React, { useEffect, useState } from 'react';
import {
  Table,
  Container,
  TableCell,
  TableBody,
  TableRow,
  TableHead,
} from '@mui/material';
import NavBar from '../components/NavBar';
import { useParams } from 'react-router-dom';

function TransactionsScreen() {
  const { accountNumber } = useParams();
  const [transactions, setTransactions] = useState('');

  useEffect(() => {
    async function getTransactions() {
      const { access } = JSON.parse(localStorage.getItem('userInfo'));
      const config = {
        headers: {
          Authorization: `Bearer ${access}`,
        },
      };
      const { data } = accountNumber
        ? await axios.get(
            `/api/accounts/${accountNumber}/transactions/`,
            config
          )
        : await axios.get('api/users/transactions/', config);
      setTransactions(data.data.transactions);
    }

    getTransactions();
  }, [accountNumber]);

  return (
    <Container>
      <NavBar />
      {transactions.length < 1 ? (
        <h2>No transactions available</h2>
      ) : (
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Date</TableCell>
              <TableCell>Transaction Type</TableCell>
              <TableCell>Account Number</TableCell>
              <TableCell>Note</TableCell>
              <TableCell>Amount</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {transactions.map((t) => (
              <TableRow key={t.ID}>
                <TableCell>{t.ID}</TableCell>
                <TableCell>{t.date}</TableCell>
                <TableCell>{t.transaction_type}</TableCell>
                <TableCell>***{t.account.substring(12, 16)}</TableCell>
                <TableCell>{t.note}</TableCell>
                <TableCell>
                  {t.transaction_type === 'DEBIT' ? '-' : '+'}
                  {t.amount}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
    </Container>
  );
}

export default TransactionsScreen;
