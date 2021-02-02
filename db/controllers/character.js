import rimraf from 'rimraf';
import Character from '../models/character';
import Objekts from '../models/objekts';
import { dir } from './dialogue';

export const addCharacter = data => new Promise((resolve, reject) => {
  const character = new Character(data);
  character.save((err, results) => {
    if (!err) return resolve(results);
    console.error('Create character error:', err);
    reject(err);
  });
});

export const findCharacter = id => new Promise((resolve, reject) => {
  Character
    .findById(id, (err, character) => {
      if (err) return reject(err);
      return resolve(character);
    });
});

export const checkIfCharacterExist = (req, res, next) => {
  findCharacter(req.params.id)
    .then((character) => {
      if (!character) return res.json(404, { message: 'Character does not exist' });
      req.character = character;
      next();
    })
    .catch(() => res.json(404, { message: 'Character does not exist' }));
};

export const updateCharacter = data => new Promise((resolve, reject) => {
  Character.findByIdAndUpdate(data._id, data, (error, objekt) => {
    if (!error) return resolve(objekt);
    console.error('Update character error:', error);
    reject(error);
  });
});

export const getCharacter = () => new Promise((resolve, reject) => {
  Character
    .find({})
    .lean()
    .exec((err, character) => {
      if (err) reject(err);
      else resolve(character);
    });
});

export const deleteCharacter = data => new Promise((resolve, reject) => {
  Character.findOneAndRemove({ _id: data.id })
    .exec((error, character) => {
      if (!error && character.deletedCount !== 0) {
        return Objekts
          // .deleteMany({ characterId: data.id })
          .find({ characterId: data.id }, (err, objekts) => {
            if (err) return reject(error);
            if (objekts.length === 0) return resolve(objekts);
            objekts.forEach((obj) => {
              rimraf(`./${dir}/${obj._id}`, (rmerr) => {
                if (rmerr) return reject(error);
              });
            });
          })
          .deleteMany()
          .exec((err, objekt) => {
            if (!err) return resolve(objekt);
            console.error('Delete objekt error:', error);
            reject(error);
          });
      }

      console.error('Delete character error:', error);
      reject(error);
    });
});
