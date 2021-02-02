import mongoose, { Schema } from 'mongoose';

const CharacterSchema = new Schema({
  name: { type: String },
  description: { type: String },
  dialogueId: { type: String },
  images: [{ type: String }],
  avatarId: { type: String },
}, {
  versionKey: false,
  collection: 'CharacterCollection',
});

export default mongoose.model('CharacterModel', CharacterSchema);
