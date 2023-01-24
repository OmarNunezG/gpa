import axios from 'axios';
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Button, TextField } from '@mui/material';
import { Container } from '@mui/system';

function LoginScreen() {
  const navigate = useNavigate();
  async function handleSubmit(e) {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const username = formData.get('username');
    const password = formData.get('password');

    const { data } = await axios.post('/api/users/token/', {
      username: username,
      password: password,
    });
    navigate('/accounts');
    localStorage.setItem('userInfo', JSON.stringify(data));
  }

  return (
    <Container>
      <h1>GPA</h1>
      <Box component="form" onSubmit={handleSubmit}>
        <TextField label="Username" name="username" />
        <TextField label="Password" name="password" type="password" />
        <Button variant="contained" type="submit">
          Sign In
        </Button>
      </Box>
    </Container>
  );
}

export default LoginScreen;
