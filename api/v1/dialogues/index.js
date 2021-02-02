import express from 'express';
import fs from 'fs';
import _ from 'lodash';
import jwt from 'jsonwebtoken';
import { updateObjekt } from '../../../db/controllers/objekts';
import { checkIfObjektExist, checkUploadPath, imageUpload, fileUpload, dir } from '../../../db/controllers/dialogue';
import remote from '../../../constants';
import { verifyToken } from '../../../constants/helpers';

const router = express.Router();

const { secretkey } = remote;

router
  .post('/image/:id', verifyToken, checkIfObjektExist, checkUploadPath, imageUpload.single('file'), (req, res) => {
    if (!req.file) return res.status(400).json({ message: 'Data is not correct' });
    jwt.verify(req.token, secretkey, (err) => {
      if (err) return res.status(403).json({ message: 'Token is not correct' });
      let { avatarId, images } = req.objekt;
      if (!Array.isArray(images)) images = [];
      if (req.body.isAvatar) avatarId = req.file.path; else images.push(req.file.path);
      updateObjekt({ images, avatarId, _id: req.params.id })
        .then(objekt => res.status(200).json({ objekt }));
    });
  })

  .delete('/image/:objektId/:imageId', verifyToken, checkIfObjektExist, (req, res) => {
    jwt.verify(req.token, secretkey, (err) => {
      if (err) return res.status(403).json({ message: 'Token is not correct' });
      fs.unlink(`./${dir}/${req.params.objektId}/${req.params.imageId}.jpeg`, (error) => {
        if (error) return res.status(400).json({ message: 'Image does not exist' });
        _.remove(req.objekt.dialogueId || [], e => e === `${dir}/${req.params.objektId}/${req.params.imageId}.jpeg`);
        updateObjekt(req.objekt)
          .then(() => res.status(200).json({ message: 'Image removed' }));
      });
    });
  })

  .post('/:id', verifyToken, checkIfObjektExist, checkUploadPath, fileUpload.single('file'), (req, res) => {
    if (!req.file) return res.status(400).json({ message: 'Data is not correct' });
    jwt.verify(req.token, secretkey, (err) => {
      if (err) return res.status(403).json({ message: 'Token is not correct' });
      updateObjekt({ dialogueId: req.file.path, _id: req.params.id })
        .then(objekt => res.status(200).json({ objekt }));
    });
  });


export default router;
