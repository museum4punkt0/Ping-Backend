import mongoose, { Schema } from 'mongoose';

const DialoguesSchema = new Schema({
  text: { type: String },
  objektId: { type: String },
}, {
  versionKey: false,
  collection: 'DialoguesCollection',
});

export default mongoose.model('DialoguesModel', DialoguesSchema);
