import express from 'express';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { getUser } from '../../../db/controllers/users';
import remote from '../../../constants';

const router = express.Router();
const { expiresIn, secretkey } = remote;

router
  .post('/', (req, res) => {
    getUser(req.body.username)
      .then((user) => {
        if (!user) return res.status(401).json({ message: 'User not found' });
        const { _id, password, username, registeredAt } = user;

        bcrypt.compare(req.body.password, password, (err, bres) => {
          if (!bres || err) return res.status(401).json({ message: 'Password is not correct' });

          jwt.sign({ id: _id, username }, secretkey, { expiresIn }, (error, token) => {
            if (error) return res.status(401).json({ message: error });
            const userData = { username, id: _id, registeredAt, token };
            return res.status(200).json(userData);
          });
        });
      });
  });

export default router;
