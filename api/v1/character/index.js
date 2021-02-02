import express from 'express';
import jwt from 'jsonwebtoken';
import rimraf from 'rimraf';
import remote from '../../../constants';
import { verifyToken } from '../../../constants/helpers';
import { addCharacter, getCharacter, deleteCharacter, updateCharacter, checkIfCharacterExist } from '../../../db/controllers/character';
import { checkUploadPath, imageUpload, fileUpload, dir } from '../../../db/controllers/dialogue';

const router = express.Router();
const { secretkey } = remote;

router
  .get('/', (req, res) => {
    getCharacter()
      .then(characters => res.json(200, characters));
  })

  .post('/', verifyToken, (req, res) => {
    jwt.verify(req.token, secretkey, (err, authData) => {
      if (err) return res.status(403).json({ message: 'Token is not correct' });
      const { name, description } = req.body;
      if (!name || !description) return res.status(400).json({ message: 'Data is not valid' });

      addCharacter({ name, description })
        .then(character => res.status(200).json({ authData, character }))
        .catch(() => res.json(502, { message: 'Can not create character' }));
    });
  })

  .delete('/:id', verifyToken, (req, res) => {
    jwt.verify(req.token, secretkey, (err) => {
      if (err) return res.status(403).json({ message: 'Token is not correct' });
      deleteCharacter({ id: req.params.id })
        .then(() => {
          rimraf(`./${dir}/${req.params.id}`, (error) => {
            if (!error) return res.status(200).json({ message: 'Character removed' });
            console.error('Remove character assets dir error:', error);
            res.status(502).json({ message: `Remove character assets dir error:${error}` });
          });
        })
        .catch(() => res.status(404).json({ message: 'Character not found' }));
    });
  })

  .post('/image/:id', verifyToken, checkIfCharacterExist, checkUploadPath, imageUpload.single('file'), (req, res) => {
    if (!req.file) return res.status(400).json({ message: 'Data is not correct' });
    jwt.verify(req.token, secretkey, (err) => {
      if (err) return res.status(403).json({ message: 'Token is not correct' });
      let { avatarId, images } = req.character;
      if (!Array.isArray(images)) images = [];
      if (req.body.isAvatar) avatarId = req.file.path; else images.push(req.file.path);
      updateCharacter({ images, avatarId, _id: req.params.id })
        .then(character => res.status(200).json({ character }));
    });
  })

  .post('/dialogue/:id', verifyToken, checkIfCharacterExist, checkUploadPath, fileUpload.single('file'), (req, res) => {
    if (!req.file) return res.status(400).json({ message: 'Data is not correct' });
    jwt.verify(req.token, secretkey, (err) => {
      if (err) return res.status(403).json({ message: 'Token is not correct' });
      updateCharacter({ dialogueId: req.file.path, _id: req.params.id })
        .then(character => res.status(200).json({ character }));
    });
  });

export default router;
