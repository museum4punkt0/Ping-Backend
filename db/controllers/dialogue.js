import fs from 'fs';
import uuid from 'uuid';
import multer from 'multer';
import { findObjekts } from './objekts';

export const dir = 'assets';
const storage = multer.diskStorage({
  destination(req, file, next) { next(null, `./${dir}/${req.params.id}`); },
  filename(req, file, next) {
    const nameArr = file.originalname.split('.');
    let filename = `${uuid().split('-').join('')}.${nameArr[nameArr.length - 1]}`;
    if (file.mimetype === 'text/plain') filename = `dialogue.${nameArr[nameArr.length - 1]}`;
    if (req.isAvatar) filename = `avatar.${nameArr[nameArr.length - 1]}`;
    next(null, filename);
  },
});

const photoFilter = (req, file, next) => {
  if (file.mimetype === 'image/jpeg' || file.mimetype === 'image/png') return next(null, true);
  next(null, false);
};

const fileFilter = (req, file, next) => {
  if (file.mimetype === 'text/plain') return next(null, true);
  next(null, false);
};

export const imageUpload = multer({ storage, fileFilter: photoFilter });
export const fileUpload = multer({ storage, fileFilter });

export const checkUploadPath = (req, res, next) => {
  fs.exists(`./${dir}/${req.params.id}`, (exists) => {
    if (exists) return next();
    fs.mkdir(`./${dir}/${req.params.id}`, (err) => {
      if (!err) return next();
      console.error('Error in folder creation');
      return res.json(500, { message: 'Error in folder creation' });
    });
  });
};

export const checkIfObjektExist = (req, res, next) => {
  findObjekts(req.params.id)
    .then((objekt) => {
      if (!objekt) return res.json(404, { message: 'Objekt does not exist' });
      req.objekt = objekt;
      next();
    })
    .catch(() => res.json(404, { message: 'Objekt does not exist' }));
};
