import _ from 'lodash';
import User from '../models/users';

export const addUser = (data) => {
  const { username, password } = data;
  const user = new User({ username, password });

  return new Promise((resolve, reject) => {
    user.save((err, results) => {
      console.log('Save message');
      if (err) {
        console.log('Error:', err);
        reject(err);
      } else {
        console.log('User saved.');
        resolve(results);
      }
    });
  });
};

export const getUser = username => new Promise((resolve, reject) => {
  User.findOne({ username: { $regex: _.escapeRegExp(username), $options: 'i' } })
    .lean()
    .exec((err, user) => {
      if (err) reject(err);
      else resolve(user);
    });
});
