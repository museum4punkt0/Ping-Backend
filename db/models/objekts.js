import mongoose, { Schema } from 'mongoose';

const ObjektSchema = new Schema({
  name: { type: String },
  banner: { type: String },
  category: { type: String },
  room: { type: Number },
  description: { type: String },
  details: { type: String },
  dialogueId: { type: String },
  images: [{ type: String }],
  avatarId: { type: String },
  characterId: { type: String },
}, {
  versionKey: false,
  collection: 'ObjektCollection',
});

export default mongoose.model('ObjektModel', ObjektSchema);
