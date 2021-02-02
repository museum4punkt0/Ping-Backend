import express from 'express';
import jwt from 'jsonwebtoken';
import rimraf from 'rimraf';
import remote from '../../../constants';
import { verifyToken } from '../../../constants/helpers';
import { addObjekt, getObjekts, updateObjekt, deleteObjekt } from '../../../db/controllers/objekts';
import { checkIfCharacterExist } from '../../../db/controllers/character';
import { dir } from '../../../db/controllers/dialogue';

const router = express.Router();
const { secretkey } = remote;

router
  .get('/', (req, res) => {
    getObjekts()
      .then(objekts => res.json(200, objekts));
  })

  .post('/:id', verifyToken, checkIfCharacterExist, (req, res) => {
    jwt.verify(req.token, secretkey, (err, authData) => {
      if (err) return res.status(403).json({ message: 'Token is not correct' });
      const { name, banner, category, room, description, details } = req.body;
      const { id } = req.params;
      if (!name || !banner || !category) return res.status(400).json({ message: 'Data is not valid' });

      addObjekt({ name, banner, category, room, description, details, characterId: id })
        .then(objekt => res.status(200).json({ authData, objekt }));
    });
  })

  .put('/:id', verifyToken, (req, res) => {
    jwt.verify(req.token, secretkey, (err, authData) => {
      if (err) return res.status(403).json({ message: 'Token is not correct' });
      const { dialogueId, avatarId, images } = req.body;
      if (dialogueId || avatarId || images) {
        return updateObjekt({ dialogueId, avatarId, images, _id: req.params.id })
          .then(objekt => res.status(200).json({ authData, objekt }));
      }
      return res.status(400).json({ message: 'Data is not valid' });
    });
  })

  .delete('/:id', verifyToken, (req, res) => {
    jwt.verify(req.token, secretkey, (err) => {
      if (err) return res.status(403).json({ message: 'Token is not correct' });
      deleteObjekt({ id: req.params.id })
        .then(() => {
          rimraf(`./${dir}/${req.params.id}`, (error) => {
            if (error) console.error('Remove assets dir error:', error);
            res.status(200).json({ message: 'Objekt removed' });
          });
        })
        .catch(() => res.status(404).json({ message: 'Objekt not found' }));
    });
  });


export default router;
