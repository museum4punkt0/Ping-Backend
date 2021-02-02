import Objekts from '../models/objekts';

export const addObjekt = data => new Promise((resolve, reject) => {
  const objekt = new Objekts(data);
  objekt.save((err, results) => {
    if (err) {
      console.error('Save objekt error:', err);
      reject(err);
    } else resolve(results);
  });
});

export const updateObjekt = data => new Promise((resolve, reject) => {
  Objekts.findByIdAndUpdate(data._id, data, (error, objekt) => {
    if (!error) return resolve(objekt);
    console.error('Update objekt error:', error);
    reject(error);
  });
});

export const findObjekts = id => new Promise((resolve, reject) => {
  Objekts
    .findById(id, (err, user) => {
      if (err) return reject(err);
      return resolve(user);
    });
});

export const getObjekts = () => new Promise((resolve, reject) => {
  Objekts
    .find({})
    .lean()
    .exec((err, objekts) => {
      if (err) reject(err);
      else resolve(objekts);
    });
});

export const deleteObjekt = data => new Promise((resolve, reject) => {
  Objekts
    .findOneAndRemove({ _id: data.id })
    .exec((error, objekt) => {
      if (!error && objekt.deletedCount !== 0) return resolve(objekt);
      // if (!error) return resolve(objekt);
      console.error('Delete objekt error:', error);
      reject(error);
    });
});
