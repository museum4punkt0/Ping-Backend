import express from 'express';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { getUser, addUser } from '../../../db/controllers/users';
import remote from '../../../constants';
import { validateSignUp } from '../../../constants/helpers';

const router = express.Router();
const { expiresIn, secretkey } = remote;
const saltRounds = 12;

router
  .post('/', (req, res) => {
    if (validateSignUp(req.body)) {
      getUser(req.body.username)
        .then((usr) => {
          if (usr) return res.status(400).json({ message: 'User with this email already exists' });

          bcrypt.hash(req.body.password, saltRounds, (err, hash) => {
            req.body.password = hash;
            const { username, password } = req.body;

            addUser({ username, password, registeredAt: new Date() })
              .then((user) => {
                if (!user) return res.status(500).json({ message: 'User wasn\'t created' });

                const jwtUser = { id: user._id, username: user.username };
                jwt.sign(jwtUser, secretkey, { expiresIn }, (error, token) => {
                  if (error) return res.status(401).json({ message: error });

                  const userData = {
                    username: user.username,
                    id: user._id,
                    registeredAt: user.registeredAt,
                    token,
                  };

                  console.log('User created:', userData.username);
                  return res.status(200).json(userData);
                });
              });
          });
        });
    } else {
      res.status(400).json({ message: 'User data is not valid' });
    }
  });


export default router;
